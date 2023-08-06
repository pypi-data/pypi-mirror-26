import os
import os.path
import re
import time
import hashlib
import logging
import multiprocessing
from piecrust.chefutil import format_timed, format_timed_scope
from piecrust.environment import ExecutionStats
from piecrust.processing.base import PipelineContext
from piecrust.processing.records import (
        ProcessorPipelineRecordEntry, TransitionalProcessorPipelineRecord,
        FLAG_PROCESSED)
from piecrust.processing.worker import (
        ProcessingWorkerJob,
        get_filtered_processors)


logger = logging.getLogger(__name__)


class _ProcessingContext(object):
    def __init__(self, jobs, record, base_dir, mount_info):
        self.jobs = jobs
        self.record = record
        self.base_dir = base_dir
        self.mount_info = mount_info


class ProcessorPipeline(object):
    def __init__(self, app, out_dir, force=False,
                 applied_config_variant=None,
                 applied_config_values=None):
        assert app and out_dir
        self.app = app
        self.out_dir = out_dir
        self.force = force
        self.applied_config_variant = applied_config_variant
        self.applied_config_values = applied_config_values

        tmp_dir = app.cache_dir
        if not tmp_dir:
            import tempfile
            tmp_dir = os.path.join(tempfile.gettempdir(), 'piecrust')
        self.tmp_dir = os.path.join(tmp_dir, 'proc')

        baker_params = app.config.get('baker', {})

        mount_params = baker_params.get('assets_dirs', {})
        self.mounts = make_mount_infos(app, mount_params)

        self.num_workers = baker_params.get(
                'workers', multiprocessing.cpu_count())

        ignores = baker_params.get('ignore', [])
        ignores += [
                '_cache', '_counter',
                '.DS_Store', 'Thumbs.db',
                '.git*', '.hg*', '.svn']
        self.ignore_patterns = make_re(ignores)
        self.force_patterns = make_re(baker_params.get('force', []))

        # Those things are mostly for unit-testing.
        #
        # Note that additiona processors can't be passed as instances.
        # Instead, we need some factory functions because we need to create
        # one instance right away to use during the initialization phase, and
        # another instance to pass to the worker pool. The initialized one will
        # be tied to the PieCrust app instance, which can't be pickled across
        # processes.
        self.enabled_processors = None
        self.additional_processors_factories = None

    def addIgnorePatterns(self, patterns):
        self.ignore_patterns += make_re(patterns)

    def run(self, src_dir_or_file=None, *,
            delete=True, previous_record=None, save_record=True):
        start_time = time.perf_counter()

        # Get the list of processors for this run.
        processors = self.app.plugin_loader.getProcessors()
        if self.enabled_processors is not None:
            logger.debug("Filtering processors to: %s" %
                         self.enabled_processors)
            processors = get_filtered_processors(processors,
                                                 self.enabled_processors)
        if self.additional_processors_factories is not None:
            logger.debug("Adding %s additional processors." %
                         len(self.additional_processors_factories))
            for proc_fac in self.additional_processors_factories:
                proc = proc_fac()
                self.app.env.registerTimer(proc.__class__.__name__,
                                           raise_if_registered=False)
                proc.initialize(self.app)
                processors.append(proc)

        # Invoke pre-processors.
        pipeline_ctx = PipelineContext(-1, self.app, self.out_dir,
                                       self.tmp_dir, self.force)
        for proc in processors:
            proc.onPipelineStart(pipeline_ctx)

        # Pre-processors can define additional ignore patterns.
        self.ignore_patterns += make_re(
                pipeline_ctx._additional_ignore_patterns)

        # Create the pipeline record.
        record = TransitionalProcessorPipelineRecord()
        record_cache = self.app.cache.getCache('proc')
        record_name = (
                hashlib.md5(self.out_dir.encode('utf8')).hexdigest() +
                '.record')
        if previous_record:
            record.setPrevious(previous_record)
        elif not self.force and record_cache.has(record_name):
            with format_timed_scope(logger, 'loaded previous bake record',
                                    level=logging.DEBUG, colored=False):
                record.loadPrevious(record_cache.getCachePath(record_name))
        logger.debug("Got %d entries in process record." %
                     len(record.previous.entries))
        record.current.success = True
        record.current.processed_count = 0

        # Work!
        def _handler(res):
            entry = record.getCurrentEntry(res.path)
            assert entry is not None
            entry.flags = res.flags
            entry.proc_tree = res.proc_tree
            entry.rel_outputs = res.rel_outputs
            if entry.flags & FLAG_PROCESSED:
                record.current.processed_count += 1
            if res.errors:
                entry.errors += res.errors
                record.current.success = False

                rel_path = os.path.relpath(res.path, self.app.root_dir)
                logger.error("Errors found in %s:" % rel_path)
                for e in entry.errors:
                    logger.error("  " + e)

        jobs = []
        self._process(src_dir_or_file, record, jobs)
        pool = self._createWorkerPool()
        ar = pool.queueJobs(jobs, handler=_handler)
        ar.wait()

        # Shutdown the workers and get timing information from them.
        reports = pool.close()
        total_stats = ExecutionStats()
        record.current.stats['_Total'] = total_stats
        for i in range(len(reports)):
            worker_stats = reports[i]['data']
            if worker_stats is not None:
                worker_name = 'PipelineWorker_%d' % i
                record.current.stats[worker_name] = worker_stats
                total_stats.mergeStats(worker_stats)

        # Invoke post-processors.
        pipeline_ctx.record = record.current
        for proc in processors:
            proc.onPipelineEnd(pipeline_ctx)

        # Handle deletions.
        if delete:
            for path, reason in record.getDeletions():
                logger.debug("Removing '%s': %s" % (path, reason))
                record.current.deleted.append(path)
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass
                logger.info('[delete] %s' % path)

        # Finalize the process record.
        record.current.process_time = time.time()
        record.current.out_dir = self.out_dir
        record.collapseRecords()

        # Save the process record.
        if save_record:
            with format_timed_scope(logger, 'saved bake record',
                                    level=logging.DEBUG, colored=False):
                record.saveCurrent(record_cache.getCachePath(record_name))

        logger.info(format_timed(
                start_time,
                "processed %d assets." % record.current.processed_count))

        return record.detach()

    def _process(self, src_dir_or_file, record, jobs):
        if src_dir_or_file is not None:
            # Process only the given path.
            # Find out what mount point this is in.
            for path, info in self.mounts.items():
                if src_dir_or_file[:len(path)] == path:
                    base_dir = path
                    mount_info = info
                    break
            else:
                known_roots = list(self.mounts.keys())
                raise Exception("Input path '%s' is not part of any known "
                                "mount point: %s" %
                                (src_dir_or_file, known_roots))

            ctx = _ProcessingContext(jobs, record, base_dir, mount_info)
            logger.debug("Initiating processing pipeline on: %s" %
                         src_dir_or_file)
            if os.path.isdir(src_dir_or_file):
                self._processDirectory(ctx, src_dir_or_file)
            elif os.path.isfile(src_dir_or_file):
                self._processFile(ctx, src_dir_or_file)

        else:
            # Process everything.
            for path, info in self.mounts.items():
                ctx = _ProcessingContext(jobs, record, path, info)
                logger.debug("Initiating processing pipeline on: %s" % path)
                self._processDirectory(ctx, path)

    def _processDirectory(self, ctx, start_dir):
        for dirpath, dirnames, filenames in os.walk(start_dir):
            rel_dirpath = os.path.relpath(dirpath, start_dir)
            dirnames[:] = [d for d in dirnames
                           if not re_matchany(
                               d, self.ignore_patterns, rel_dirpath)]

            for filename in filenames:
                if re_matchany(filename, self.ignore_patterns, rel_dirpath):
                    continue
                self._processFile(ctx, os.path.join(dirpath, filename))

    def _processFile(self, ctx, path):
        # TODO: handle overrides between mount-points.

        entry = ProcessorPipelineRecordEntry(path)
        ctx.record.addEntry(entry)

        previous_entry = ctx.record.getPreviousEntry(path)
        force_this = (self.force or previous_entry is None or
                      not previous_entry.was_processed_successfully)

        job = ProcessingWorkerJob(ctx.base_dir, ctx.mount_info, path,
                                  force=force_this)
        ctx.jobs.append(job)

    def _createWorkerPool(self):
        from piecrust.app import PieCrustFactory
        from piecrust.workerpool import WorkerPool
        from piecrust.processing.worker import (
                ProcessingWorkerContext, ProcessingWorker)

        appfactory = PieCrustFactory(
                self.app.root_dir,
                cache=self.app.cache.enabled,
                cache_key=self.app.cache_key,
                config_variant=self.applied_config_variant,
                config_values=self.applied_config_values,
                debug=self.app.debug,
                theme_site=self.app.theme_site)

        ctx = ProcessingWorkerContext(
                appfactory,
                self.out_dir, self.tmp_dir,
                force=self.force)
        ctx.enabled_processors = self.enabled_processors
        if self.additional_processors_factories is not None:
            ctx.additional_processors = [
                    proc_fac()
                    for proc_fac in self.additional_processors_factories]

        pool = WorkerPool(
                worker_class=ProcessingWorker,
                initargs=(ctx,))
        return pool


def make_mount_infos(app, mount_params):
    mounts = {d: {} for d in app.assets_dirs}

    for name, cfg in mount_params.items():
        mdir = os.path.join(app.root_dir, name)
        mounts[mdir] = cfg

    for mdir, info in mounts.items():
        mname = os.path.basename(mdir)
        info_from_config = mount_params.get(mname)
        if info_from_config is not None:
            if not isinstance(info, dict):
                raise Exception("Asset directory info for '%s' is not a "
                                "dictionary." % mname)
            info.update(info_from_config)
        info.setdefault('processors', 'all -uglifyjs -cleancss')
        info['name'] = mname

    return mounts


def make_re(patterns):
    re_patterns = []
    for pat in patterns:
        if pat[0] == '/' and pat[-1] == '/' and len(pat) > 2:
            re_patterns.append(pat[1:-1])
        else:
            escaped_pat = (
                    re.escape(pat)
                    .replace(r'\*', r'[^/\\]*')
                    .replace(r'\?', r'[^/\\]'))
            re_patterns.append(escaped_pat)
    return [re.compile(p) for p in re_patterns]


def re_matchany(filename, patterns, dirname=None):
    if dirname and dirname != '.':
        filename = os.path.join(dirname, filename)

    # skip patterns use a forward slash regardless of the platform.
    filename = filename.replace('\\', '/')
    for pattern in patterns:
        if pattern.search(filename):
            return True
    return False

