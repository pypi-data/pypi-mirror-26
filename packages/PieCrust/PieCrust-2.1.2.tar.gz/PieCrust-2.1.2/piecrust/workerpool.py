import io
import os
import sys
import time
import zlib
import queue
import logging
import itertools
import threading
import multiprocessing
from piecrust import fastpickle


logger = logging.getLogger(__name__)

use_fastqueue = True


class IWorker(object):
    def initialize(self):
        raise NotImplementedError()

    def process(self, job):
        raise NotImplementedError()

    def getReport(self, pool_reports):
        return None

    def shutdown(self):
        pass


TASK_JOB = 0
TASK_BATCH = 1
TASK_END = 2


def worker_func(params):
    if params.is_profiling:
        try:
            import cProfile as profile
        except ImportError:
            import profile

        params.is_profiling = False
        name = params.worker_class.__name__
        profile.runctx('_real_worker_func(params)',
                       globals(), locals(),
                       filename='%s-%d.prof' % (name, params.wid))
    else:
        _real_worker_func(params)


def _real_worker_func(params):
    # In a context where `multiprocessing` is using the `spawn` forking model,
    # the new process doesn't inherit anything, so we lost all our logging
    # configuration here. Let's set it up again.
    if (hasattr(multiprocessing, 'get_start_method') and
            multiprocessing.get_start_method() == 'spawn'):
        from piecrust.main import _pre_parse_chef_args
        _pre_parse_chef_args(sys.argv[1:])

    wid = params.wid
    logger.debug("Worker %d initializing..." % wid)

    # We don't need those.
    params.inqueue._writer.close()
    params.outqueue._reader.close()

    # Initialize the underlying worker class.
    w = params.worker_class(*params.initargs)
    w.wid = wid
    try:
        w.initialize()
    except Exception as ex:
        logger.error("Working failed to initialize:")
        logger.exception(ex)
        params.outqueue.put(None)
        return

    use_threads = False
    if use_threads:
        # Create threads to read/write the jobs and results from/to the
        # main arbitrator process.
        local_job_queue = queue.Queue()
        reader_thread = threading.Thread(
                target=_job_queue_reader,
                args=(params.inqueue.get, local_job_queue),
                name="JobQueueReaderThread")
        reader_thread.start()

        local_result_queue = queue.Queue()
        writer_thread = threading.Thread(
                target=_job_results_writer,
                args=(local_result_queue, params.outqueue.put),
                name="JobResultWriterThread")
        writer_thread.start()

        get = local_job_queue.get
        put = local_result_queue.put_nowait
    else:
        get = params.inqueue.get
        put = params.outqueue.put

    # Start pumping!
    completed = 0
    time_in_get = 0
    time_in_put = 0
    while True:
        get_start_time = time.perf_counter()
        task = get()
        time_in_get += (time.perf_counter() - get_start_time)

        task_type, task_data = task
        if task_type == TASK_END:
            logger.debug("Worker %d got end task, exiting." % wid)
            wprep = {
                    'WorkerTaskGet': time_in_get,
                    'WorkerResultPut': time_in_put}
            try:
                rep = (task_type, True, wid, (wid, w.getReport(wprep)))
            except Exception as e:
                logger.debug("Error getting report: %s" % e)
                if params.wrap_exception:
                    e = multiprocessing.ExceptionWithTraceback(
                            e, e.__traceback__)
                rep = (task_type, False, wid, (wid, e))
            put(rep)
            break

        if task_type == TASK_JOB:
            task_data = (task_data,)

        for t in task_data:
            try:
                res = (TASK_JOB, True, wid, w.process(t))
            except Exception as e:
                if params.wrap_exception:
                    e = multiprocessing.ExceptionWithTraceback(
                            e, e.__traceback__)
                res = (TASK_JOB, False, wid, e)

            put_start_time = time.perf_counter()
            put(res)
            time_in_put += (time.perf_counter() - put_start_time)

            completed += 1

    if use_threads:
        logger.debug("Worker %d waiting for reader/writer threads." % wid)
        local_result_queue.put_nowait(None)
        reader_thread.join()
        writer_thread.join()

    w.shutdown()

    logger.debug("Worker %d completed %d tasks." % (wid, completed))


def _job_queue_reader(getter, out_queue):
    while True:
        try:
            task = getter()
        except (EOFError, OSError):
            logger.debug("Worker encountered connection problem.")
            break

        out_queue.put_nowait(task)

        if task[0] == TASK_END:
            # Done reading jobs from the main process.
            logger.debug("Got end task, exiting task queue reader thread.")
            break


def _job_results_writer(in_queue, putter):
    while True:
        res = in_queue.get()
        if res is not None:
            putter(res)
            in_queue.task_done()
        else:
            # Got sentinel. Exit.
            in_queue.task_done()
            break
    logger.debug("Exiting result queue writer thread.")


class _WorkerParams(object):
    def __init__(self, wid, inqueue, outqueue, worker_class, initargs=(),
                 wrap_exception=False, is_profiling=False):
        self.wid = wid
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.worker_class = worker_class
        self.initargs = initargs
        self.wrap_exception = wrap_exception
        self.is_profiling = is_profiling


class WorkerPool(object):
    def __init__(self, worker_class, initargs=(),
                 worker_count=None, batch_size=None,
                 wrap_exception=False):
        worker_count = worker_count or os.cpu_count() or 1

        if use_fastqueue:
            self._task_queue = FastQueue()
            self._result_queue = FastQueue()
            self._quick_put = self._task_queue.put
            self._quick_get = self._result_queue.get
        else:
            self._task_queue = multiprocessing.SimpleQueue()
            self._result_queue = multiprocessing.SimpleQueue()
            self._quick_put = self._task_queue._writer.send
            self._quick_get = self._result_queue._reader.recv

        self._batch_size = batch_size
        self._callback = None
        self._error_callback = None
        self._listener = None

        main_module = sys.modules['__main__']
        is_profiling = os.path.basename(main_module.__file__) in [
                'profile.py', 'cProfile.py']

        self._pool = []
        for i in range(worker_count):
            worker_params = _WorkerParams(
                    i, self._task_queue, self._result_queue,
                    worker_class, initargs,
                    wrap_exception=wrap_exception,
                    is_profiling=is_profiling)
            w = multiprocessing.Process(target=worker_func,
                                        args=(worker_params,))
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            self._pool.append(w)

        self._result_handler = threading.Thread(
                target=WorkerPool._handleResults,
                args=(self,))
        self._result_handler.daemon = True
        self._result_handler.start()

        self._closed = False

    def setHandler(self, callback=None, error_callback=None):
        self._callback = callback
        self._error_callback = error_callback

    def queueJobs(self, jobs, handler=None, chunk_size=None):
        if self._closed:
            raise Exception("This worker pool has been closed.")
        if self._listener is not None:
            raise Exception("A previous job queue has not finished yet.")

        if any([not p.is_alive() for p in self._pool]):
            raise Exception("Some workers have prematurely exited.")

        if handler is not None:
            self.setHandler(handler)

        if not hasattr(jobs, '__len__'):
            jobs = list(jobs)
        job_count = len(jobs)

        res = AsyncResult(self, job_count)
        if res._count == 0:
            res._event.set()
            return res

        self._listener = res

        if chunk_size is None:
            chunk_size = self._batch_size
        if chunk_size is None:
            chunk_size = max(1, job_count // 50)
            logger.debug("Using chunk size of %d" % chunk_size)

        if chunk_size is None or chunk_size == 1:
            for job in jobs:
                self._quick_put((TASK_JOB, job))
        else:
            it = iter(jobs)
            while True:
                batch = tuple([i for i in itertools.islice(it, chunk_size)])
                if not batch:
                    break
                self._quick_put((TASK_BATCH, batch))

        return res

    def close(self):
        if self._listener is not None:
            raise Exception("A previous job queue has not finished yet.")

        logger.debug("Closing worker pool...")
        handler = _ReportHandler(len(self._pool))
        self._callback = handler._handle
        for w in self._pool:
            self._quick_put((TASK_END, None))
        for w in self._pool:
            w.join()

        logger.debug("Waiting for reports...")
        if not handler.wait(2):
            missing = handler.reports.index(None)
            logger.warning(
                    "Didn't receive all worker reports before timeout. "
                    "Missing report from worker %d." % missing)

        logger.debug("Exiting result handler thread...")
        self._result_queue.put(None)
        self._result_handler.join()
        self._closed = True

        return handler.reports

    @staticmethod
    def _handleResults(pool):
        while True:
            try:
                res = pool._quick_get()
            except (EOFError, OSError):
                logger.debug("Result handler thread encountered connection "
                             "problem, exiting.")
                return

            if res is None:
                logger.debug("Result handler exiting.")
                break

            task_type, success, wid, data = res
            try:
                if success and pool._callback:
                    pool._callback(data)
                elif not success:
                    if pool._error_callback:
                        pool._error_callback(data)
                    else:
                        logger.error("Got error data:")
                        logger.error(data)
            except Exception as ex:
                logger.exception(ex)

            if task_type == TASK_JOB:
                pool._listener._onTaskDone()


class AsyncResult(object):
    def __init__(self, pool, count):
        self._pool = pool
        self._count = count
        self._event = threading.Event()

    def ready(self):
        return self._event.is_set()

    def wait(self, timeout=None):
        return self._event.wait(timeout)

    def _onTaskDone(self):
        self._count -= 1
        if self._count == 0:
            self._pool.setHandler(None)
            self._pool._listener = None
            self._event.set()


class _ReportHandler(object):
    def __init__(self, worker_count):
        self.reports = [None] * worker_count
        self._count = worker_count
        self._received = 0
        self._event = threading.Event()

    def wait(self, timeout=None):
        return self._event.wait(timeout)

    def _handle(self, res):
        wid, data = res
        if wid < 0 or wid > self._count:
            logger.error("Ignoring report from unknown worker %d." % wid)
            return

        self._received += 1
        self.reports[wid] = data

        if self._received == self._count:
            self._event.set()

    def _handleError(self, res):
        wid, data = res
        logger.error("Worker %d failed to send its report." % wid)
        logger.exception(data)


class FastQueue(object):
    def __init__(self):
        self._reader, self._writer = multiprocessing.Pipe(duplex=False)
        self._rlock = multiprocessing.Lock()
        self._wlock = multiprocessing.Lock()
        self._initBuffers()

    def _initBuffers(self):
        self._rbuf = io.BytesIO()
        self._rbuf.truncate(256)
        self._wbuf = io.BytesIO()
        self._wbuf.truncate(256)

    def __getstate__(self):
        return (self._reader, self._writer, self._rlock, self._wlock)

    def __setstate__(self, state):
        (self._reader, self._writer, self._rlock, self._wlock) = state
        self._initBuffers()

    def get(self):
        with self._rlock:
            try:
                with self._rbuf.getbuffer() as b:
                    bufsize = self._reader.recv_bytes_into(b)
            except multiprocessing.BufferTooShort as e:
                bufsize = len(e.args[0])
                self._rbuf.truncate(bufsize * 2)
                self._rbuf.seek(0)
                self._rbuf.write(e.args[0])

        self._rbuf.seek(0)
        return self._unpickle(self._rbuf, bufsize)

    def put(self, obj):
        self._wbuf.seek(0)
        self._pickle(obj, self._wbuf)
        size = self._wbuf.tell()

        self._wbuf.seek(0)
        with self._wlock:
            with self._wbuf.getbuffer() as b:
                self._writer.send_bytes(b, 0, size)

    def _pickle(self, obj, buf):
        fastpickle.pickle_intob(obj, buf)

    def _unpickle(self, buf, bufsize):
        return fastpickle.unpickle_fromb(buf, bufsize)

