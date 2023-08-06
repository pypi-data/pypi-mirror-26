import re
import os.path
import copy
import logging
from werkzeug.utils import cached_property
from piecrust.data.builder import (
        DataBuildingContext, build_page_data, build_layout_data)
from piecrust.data.filters import (
        PaginationFilter, SettingFilterClause, page_value_accessor)
from piecrust.fastpickle import _pickle_object, _unpickle_object
from piecrust.sources.base import PageSource
from piecrust.templating.base import TemplateNotFoundError, TemplatingError


logger = logging.getLogger(__name__)


content_abstract_re = re.compile(r'^<!--\s*(more|(page)?break)\s*-->\s*$',
                                 re.MULTILINE)


class PageRenderingError(Exception):
    pass


class TemplateEngineNotFound(Exception):
    pass


class QualifiedPage(object):
    def __init__(self, page, route, route_metadata):
        self.page = page
        self.route = route
        self.route_metadata = route_metadata

    def getUri(self, sub_num=1):
        return self.route.getUri(self.route_metadata, sub_num=sub_num)

    def __getattr__(self, name):
        return getattr(self.page, name)


class RenderedSegments(object):
    def __init__(self, segments, render_pass_info):
        self.segments = segments
        self.render_pass_info = render_pass_info


class RenderedLayout(object):
    def __init__(self, content, render_pass_info):
        self.content = content
        self.render_pass_info = render_pass_info


class RenderedPage(object):
    def __init__(self, page, uri, num=1):
        self.page = page
        self.uri = uri
        self.num = num
        self.data = None
        self.content = None
        self.render_info = [None, None]

    @property
    def app(self):
        return self.page.app

    def copyRenderInfo(self):
        return copy.deepcopy(self.render_info)


PASS_NONE = -1
PASS_FORMATTING = 0
PASS_RENDERING = 1


RENDER_PASSES = [PASS_FORMATTING, PASS_RENDERING]


class RenderPassInfo(object):
    def __init__(self):
        self.used_source_names = set()
        self.used_pagination = False
        self.pagination_has_more = False
        self.used_assets = False
        self._custom_info = {}

    def setCustomInfo(self, key, info):
        self._custom_info[key] = info

    def getCustomInfo(self, key, default=None, create_if_missing=False):
        if create_if_missing:
            return self._custom_info.setdefault(key, default)
        return self._custom_info.get(key, default)


class PageRenderingContext(object):
    def __init__(self, qualified_page, page_num=1,
                 force_render=False, is_from_request=False):
        self.page = qualified_page
        self.page_num = page_num
        self.force_render = force_render
        self.is_from_request = is_from_request
        self.pagination_source = None
        self.pagination_filter = None
        self.custom_data = {}
        self.render_passes = [None, None]  # Same length as RENDER_PASSES
        self._current_pass = PASS_NONE

    @property
    def app(self):
        return self.page.app

    @property
    def source_metadata(self):
        return self.page.source_metadata

    @cached_property
    def uri(self):
        return self.page.getUri(self.page_num)

    @property
    def current_pass_info(self):
        if self._current_pass != PASS_NONE:
            return self.render_passes[self._current_pass]
        return None

    def setCurrentPass(self, rdr_pass):
        if rdr_pass != PASS_NONE:
            self.render_passes[rdr_pass] = RenderPassInfo()
        self._current_pass = rdr_pass

    def setPagination(self, paginator):
        self._raiseIfNoCurrentPass()
        pass_info = self.current_pass_info
        if pass_info.used_pagination:
            raise Exception("Pagination has already been used.")
        assert paginator.is_loaded
        pass_info.used_pagination = True
        pass_info.pagination_has_more = paginator.has_more
        self.addUsedSource(paginator._source)

    def addUsedSource(self, source):
        self._raiseIfNoCurrentPass()
        if isinstance(source, PageSource):
            pass_info = self.current_pass_info
            pass_info.used_source_names.add(source.name)

    def _raiseIfNoCurrentPass(self):
        if self._current_pass == PASS_NONE:
            raise Exception("No rendering pass is currently active.")


def render_page(ctx):
    eis = ctx.app.env.exec_info_stack
    eis.pushPage(ctx.page, ctx)
    try:
        # Build the data for both segment and layout rendering.
        with ctx.app.env.timerScope("BuildRenderData"):
            page_data = _build_render_data(ctx)

        # Render content segments.
        ctx.setCurrentPass(PASS_FORMATTING)
        repo = ctx.app.env.rendered_segments_repository
        save_to_fs = True
        if ctx.app.env.fs_cache_only_for_main_page and not eis.is_main_page:
            save_to_fs = False
        with ctx.app.env.timerScope("PageRenderSegments"):
            if repo and not ctx.force_render:
                render_result = repo.get(
                        ctx.uri,
                        lambda: _do_render_page_segments(ctx.page, page_data),
                        fs_cache_time=ctx.page.path_mtime,
                        save_to_fs=save_to_fs)
            else:
                render_result = _do_render_page_segments(ctx.page, page_data)
                if repo:
                    repo.put(ctx.uri, render_result, save_to_fs)

        # Render layout.
        page = ctx.page
        ctx.setCurrentPass(PASS_RENDERING)
        layout_name = page.config.get('layout')
        if layout_name is None:
            layout_name = page.source.config.get('default_layout', 'default')
        null_names = ['', 'none', 'nil']
        if layout_name not in null_names:
            with ctx.app.env.timerScope("BuildRenderData"):
                build_layout_data(page, page_data, render_result['segments'])

            with ctx.app.env.timerScope("PageRenderLayout"):
                layout_result = _do_render_layout(layout_name, page, page_data)
        else:
            layout_result = {
                    'content': render_result['segments']['content'],
                    'pass_info': None}

        rp = RenderedPage(page, ctx.uri, ctx.page_num)
        rp.data = page_data
        rp.content = layout_result['content']
        rp.render_info[PASS_FORMATTING] = _unpickle_object(
                render_result['pass_info'])
        if layout_result['pass_info'] is not None:
            rp.render_info[PASS_RENDERING] = _unpickle_object(
                    layout_result['pass_info'])
        return rp
    except Exception as ex:
        if ctx.app.debug:
            raise
        logger.exception(ex)
        page_rel_path = os.path.relpath(ctx.page.path, ctx.app.root_dir)
        raise Exception("Error rendering page: %s" % page_rel_path) from ex
    finally:
        ctx.setCurrentPass(PASS_NONE)
        eis.popPage()


def render_page_segments(ctx):
    eis = ctx.app.env.exec_info_stack
    eis.pushPage(ctx.page, ctx)
    try:
        ctx.setCurrentPass(PASS_FORMATTING)
        repo = ctx.app.env.rendered_segments_repository
        save_to_fs = True
        if ctx.app.env.fs_cache_only_for_main_page and not eis.is_main_page:
            save_to_fs = False
        with ctx.app.env.timerScope("PageRenderSegments"):
            if repo and not ctx.force_render:
                render_result = repo.get(
                    ctx.uri,
                    lambda: _do_render_page_segments_from_ctx(ctx),
                    fs_cache_time=ctx.page.path_mtime,
                    save_to_fs=save_to_fs)
            else:
                render_result = _do_render_page_segments_from_ctx(ctx)
                if repo:
                    repo.put(ctx.uri, render_result, save_to_fs)
    finally:
        ctx.setCurrentPass(PASS_NONE)
        eis.popPage()

    rs = RenderedSegments(
            render_result['segments'],
            _unpickle_object(render_result['pass_info']))
    return rs


def _build_render_data(ctx):
    with ctx.app.env.timerScope("PageDataBuild"):
        data_ctx = DataBuildingContext(ctx.page, page_num=ctx.page_num)
        data_ctx.pagination_source = ctx.pagination_source
        data_ctx.pagination_filter = ctx.pagination_filter
        page_data = build_page_data(data_ctx)
        if ctx.custom_data:
            page_data._appendMapping(ctx.custom_data)
        return page_data


def _do_render_page_segments_from_ctx(ctx):
    page_data = _build_render_data(ctx)
    return _do_render_page_segments(ctx.page, page_data)


def _do_render_page_segments(page, page_data):
    app = page.app

    cpi = app.env.exec_info_stack.current_page_info
    assert cpi is not None
    assert cpi.page == page

    engine_name = page.config.get('template_engine')
    format_name = page.config.get('format')

    engine = get_template_engine(app, engine_name)

    formatted_segments = {}
    for seg_name, seg in page.segments.items():
        seg_text = ''
        for seg_part in seg.parts:
            part_format = seg_part.fmt or format_name
            try:
                with app.env.timerScope(
                        engine.__class__.__name__ + '_segment'):
                    part_text = engine.renderSegmentPart(
                            page.path, seg_part, page_data)
            except TemplatingError as err:
                err.lineno += seg_part.line
                raise err

            part_text = format_text(app, part_format, part_text)
            seg_text += part_text
        formatted_segments[seg_name] = seg_text

        if seg_name == 'content':
            m = content_abstract_re.search(seg_text)
            if m:
                offset = m.start()
                content_abstract = seg_text[:offset]
                formatted_segments['content.abstract'] = content_abstract

    pass_info = cpi.render_ctx.render_passes[PASS_FORMATTING]
    res = {
            'segments': formatted_segments,
            'pass_info': _pickle_object(pass_info)}
    return res


def _do_render_layout(layout_name, page, layout_data):
    cpi = page.app.env.exec_info_stack.current_page_info
    assert cpi is not None
    assert cpi.page == page

    names = layout_name.split(',')
    default_exts = page.app.env.default_layout_extensions
    full_names = []
    for name in names:
        if '.' not in name:
            for ext in default_exts:
                full_names.append(name + ext)
        else:
            full_names.append(name)

    _, engine_name = os.path.splitext(full_names[0])
    engine_name = engine_name.lstrip('.')
    engine = get_template_engine(page.app, engine_name)

    try:
        with page.app.env.timerScope(engine.__class__.__name__ + '_layout'):
            output = engine.renderFile(full_names, layout_data)
    except TemplateNotFoundError as ex:
        logger.exception(ex)
        msg = "Can't find template for page: %s\n" % page.path
        msg += "Looked for: %s" % ', '.join(full_names)
        raise Exception(msg) from ex

    pass_info = cpi.render_ctx.render_passes[PASS_RENDERING]
    res = {'content': output, 'pass_info': _pickle_object(pass_info)}
    return res


def get_template_engine(app, engine_name):
    if engine_name == 'html':
        engine_name = None
    engine_name = engine_name or app.config.get('site/default_template_engine')
    for engine in app.plugin_loader.getTemplateEngines():
        if engine_name in engine.ENGINE_NAMES:
            return engine
    raise TemplateEngineNotFound("No such template engine: %s" % engine_name)


def format_text(app, format_name, txt, exact_format=False):
    if exact_format and not format_name:
        raise Exception("You need to specify a format name.")

    format_count = 0
    format_name = format_name or app.config.get('site/default_format')
    for fmt in app.plugin_loader.getFormatters():
        if not fmt.enabled:
            continue
        if fmt.FORMAT_NAMES is None or format_name in fmt.FORMAT_NAMES:
            with app.env.timerScope(fmt.__class__.__name__):
                txt = fmt.render(format_name, txt)
            format_count += 1
            if fmt.OUTPUT_FORMAT is not None:
                format_name = fmt.OUTPUT_FORMAT
    if exact_format and format_count == 0:
        raise Exception("No such format: %s" % format_name)
    return txt

