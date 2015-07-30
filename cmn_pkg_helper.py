from os import walk, path
import re

_PKG_PATH_MATCHER = re.compile('\/scarecrow-rules\/packages\/?$', re.I)
_CMN_PKG_MATCHER = re.compile('\/scarecrow-rules\/packages\/common', re.I)
_VALID_PKG_FILE_MATCHERS = [re.compile('\.js$', re.I)]
_PKG_EXTRACTOR = re.compile('(?:scarecrow-rules\/packages\/)(.+)(?:\.[a-z]{2,3})$', re.I)
_FUN_EXTRACTOR = re.compile('^(?:function)\s+(\w+)', re.I | re.M | re.S)
_TESTS_EXTRACTOR_STR = '^\s*(\/\/@ %s:\s*(?:\n\s*\/\/@ [^\n]+)+)'
_FUNCTION_MATCHER_STR = '^function\s+%s\s*\('

def validate_cmn_pkg_path(pkg_path):
    pkg_path = path.abspath(path.expanduser(pkg_path))
    if not path.isdir(pkg_path) or not _PKG_PATH_MATCHER.search(pkg_path):
        return None
    return pkg_path

def get_cmn_pkg_fun_list(root_pkg_path):
    pkg_paths = _get_cmn_pkg_paths(root_pkg_path)
    def fun_list_reduction(reduction, pkg_path):
        with open(pkg_path) as f: reduction.extend(_get_codes_fun_list(f.read()))
        return reduction
    return reduce(fun_list_reduction, pkg_paths, [])

def get_cmn_pkg_dict(root_pkg_path, ifTests = True, ifBody = True):
    pkg_paths = _get_cmn_pkg_paths(root_pkg_path)
    pkg_dict = {}
    for pkg_path in pkg_paths:
        pkg_name = _get_pkg_name(pkg_path)
        with open(pkg_path, 'r') as f: codes = f.read()
        pkg_dict.update({pkg_name: _get_codes_fun_dict(codes, ifTests, ifBody)})
    return pkg_dict

def get_pkgs_by_fun(root_pkg_path, fun_name):
    result_pkg_names = []
    pkg_paths = _get_cmn_pkg_paths(root_pkg_path)
    fun_matcher = re.compile(_FUNCTION_MATCHER_STR % fun_name, re.I | re.M | re.S)
    for pkg_path in pkg_paths:
        pkg_name = _get_pkg_name(pkg_path)
        with open(pkg_path, 'r') as f: codes = f.read()
        if fun_matcher.search(codes):
            result_pkg_names.append(pkg_name)
    return result_pkg_names

#
# Private
#

def _get_cmn_pkg_paths(root_pkg_path):
    root_pkg_path = root_pkg_path.strip()
    all_cmn_pkg_paths = []
    for root, dirnames, filenames in walk(root_pkg_path):
        dirnames[:] = (d for d in dirnames if _CMN_PKG_MATCHER.search(path.join(root,d)))
        filenames = map(lambda p: path.join(root, p), filenames)
        filenames = filter(lambda f: _CMN_PKG_MATCHER.search(f), filenames)
        filenames = filter(lambda f: any(r.search(f) for r in _VALID_PKG_FILE_MATCHERS),
                filenames)
        all_cmn_pkg_paths.extend(filenames)
    return all_cmn_pkg_paths

def _get_pkg_name(pkg_path):
    return _PKG_EXTRACTOR.search(pkg_path).group(1).replace('/', '.')

def _get_codes_fun_list(codes):
    return _FUN_EXTRACTOR.findall(codes)

def _get_codes_fun_dict(codes, ifTests, ifBody):
    fun_dict = {}
    for name in _get_codes_fun_list(codes):
        fun_dict[name] = {}
        if ifTests:
            tests_matcher = re.compile(_TESTS_EXTRACTOR_STR % name,
                    re.I | re.M | re.S)
            tests = tests_matcher.search(codes)
            if tests:
                tests = tests.group(1)
            else:
                tests = ''
            fun_dict[name]['tests'] = tests
        if ifBody:
            fun_dict[name]['body'] = ''
    return fun_dict

