import copy
import os.path
import hashlib
import logging
from piecrust.records import Record, TransitionalRecord


logger = logging.getLogger(__name__)


def _get_transition_key(path, extra_key=None):
    key = path
    if extra_key:
        key += '+%s' % extra_key
    return hashlib.md5(key.encode('utf8')).hexdigest()


class BakeRecord(Record):
    RECORD_VERSION = 20

    def __init__(self):
        super(BakeRecord, self).__init__()
        self.out_dir = None
        self.bake_time = None
        self.baked_count = {}
        self.total_baked_count = {}
        self.deleted = []
        self.success = True


class SubPageBakeInfo(object):
    FLAG_NONE = 0
    FLAG_BAKED = 2**0
    FLAG_FORCED_BY_SOURCE = 2**1
    FLAG_FORCED_BY_NO_PREVIOUS = 2**2
    FLAG_FORCED_BY_PREVIOUS_ERRORS = 2**3
    FLAG_FORMATTING_INVALIDATED = 2**4

    def __init__(self, out_uri, out_path):
        self.out_uri = out_uri
        self.out_path = out_path
        self.flags = self.FLAG_NONE
        self.errors = []
        self.render_info = [None, None]  # Same length as RENDER_PASSES

    @property
    def was_clean(self):
        return (self.flags & self.FLAG_BAKED) == 0 and len(self.errors) == 0

    @property
    def was_baked(self):
        return (self.flags & self.FLAG_BAKED) != 0

    @property
    def was_baked_successfully(self):
        return self.was_baked and len(self.errors) == 0

    def anyPass(self, func):
        for pinfo in self.render_info:
            if pinfo and func(pinfo):
                return True
        return False

    def copyRenderInfo(self):
        return copy.deepcopy(self.render_info)


class BakeRecordEntry(object):
    """ An entry in the bake record.
    """
    FLAG_NONE = 0
    FLAG_NEW = 2**0
    FLAG_SOURCE_MODIFIED = 2**1
    FLAG_OVERRIDEN = 2**2

    def __init__(self, source_name, path, extra_key=None):
        self.source_name = source_name
        self.path = path
        self.extra_key = extra_key
        self.flags = self.FLAG_NONE
        self.config = None
        self.timestamp = None
        self.errors = []
        self.subs = []

    @property
    def path_mtime(self):
        return os.path.getmtime(self.path)

    @property
    def was_overriden(self):
        return (self.flags & self.FLAG_OVERRIDEN) != 0

    @property
    def num_subs(self):
        return len(self.subs)

    @property
    def was_any_sub_baked(self):
        for o in self.subs:
            if o.was_baked:
                return True
        return False

    @property
    def all_assets(self):
        for sub in self.subs:
            yield from sub.assets

    @property
    def all_out_paths(self):
        for sub in self.subs:
            yield sub.out_path

    @property
    def has_any_error(self):
        if len(self.errors) > 0:
            return True
        for o in self.subs:
            if len(o.errors) > 0:
                return True
        return False

    def getSub(self, sub_index):
        return self.subs[sub_index - 1]

    def getAllErrors(self):
        yield from self.errors
        for o in self.subs:
            yield from o.errors

    def getAllUsedSourceNames(self):
        res = set()
        for o in self.subs:
            for pinfo in o.render_info:
                if pinfo:
                    res |= pinfo.used_source_names
        return res


class TransitionalBakeRecord(TransitionalRecord):
    def __init__(self, previous_path=None):
        super(TransitionalBakeRecord, self).__init__(BakeRecord,
                                                     previous_path)
        self.dirty_source_names = set()

    def addEntry(self, entry):
        if (self.previous.bake_time and
                entry.path_mtime >= self.previous.bake_time):
            entry.flags |= BakeRecordEntry.FLAG_SOURCE_MODIFIED
            self.dirty_source_names.add(entry.source_name)
        super(TransitionalBakeRecord, self).addEntry(entry)

    def getTransitionKey(self, entry):
        return _get_transition_key(entry.path, entry.extra_key)

    def getPreviousAndCurrentEntries(self, path, extra_key=None):
        key = _get_transition_key(path, extra_key)
        pair = self.transitions.get(key)
        return pair

    def getOverrideEntry(self, path, uri):
        for pair in self.transitions.values():
            cur = pair[1]
            if cur and cur.path != path:
                for o in cur.subs:
                    if o.out_uri == uri:
                        return cur
        return None

    def getPreviousEntry(self, path, extra_key=None):
        pair = self.getPreviousAndCurrentEntries(path, extra_key)
        if pair is not None:
            return pair[0]
        return None

    def getCurrentEntry(self, path, extra_key=None):
        pair = self.getPreviousAndCurrentEntries(path, extra_key)
        if pair is not None:
            return pair[1]
        return None

    def collapseEntry(self, prev_entry):
        cur_entry = copy.deepcopy(prev_entry)
        cur_entry.flags = BakeRecordEntry.FLAG_NONE
        for o in cur_entry.subs:
            o.flags = SubPageBakeInfo.FLAG_NONE
        self.addEntry(cur_entry)

    def getDeletions(self):
        for prev, cur in self.transitions.values():
            if prev and not cur:
                for sub in prev.subs:
                    yield (sub.out_path, 'previous source file was removed')
            elif prev and cur:
                prev_out_paths = [o.out_path for o in prev.subs]
                cur_out_paths = [o.out_path for o in cur.subs]
                diff = set(prev_out_paths) - set(cur_out_paths)
                for p in diff:
                    yield (p, 'source file changed outputs')

    def _onNewEntryAdded(self, entry):
        entry.flags |= BakeRecordEntry.FLAG_NEW

