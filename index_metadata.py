import copy
from cmn_name_helper import tokenize_fun_name

class IndexMetadata:

    _name_abbr_dict = {}

    #
    # [
    #   {
    #     name: FUNCTION_NAME
    #     package: 'common.poi.Address'
    #     tests: '//@:'
    #     body: '{}'
    #     type: 'function' #Could be omitted if it's function
    #     class: 2 #Could be omitted if has no class,
    #            number refer to the class index in _funMetaList
    #     memberFunctions: [4, 5, 6] #Could be omitted if it's not class,
    #            array refers to indices of member functions belong to the class
    #   },
    #   { ... }
    # ]
    #
    _fun_meta_list = []

    #
    # {
    #   token1: [0, 4, 98] #Array of indics refered to in _fun_meta_list
    #   token2: [1, 53, 34, 98] #Array of indics refered to in _fun_meta_list
    #   ...
    # }
    #
    _fun_invert_index = {}

    _IF_FUN_NAME_AS_TOKEN = True

    def set_name_abbr(self, name_abbr_dict):
        self._name_abbr_dict = name_abbr_dict

    def set_pkg_codes(self, pkg_dict):
        _fun_meta_list = []
        _fun_invert_index = {}
        self._translate_pkg_codes(copy.deepcopy(pkg_dict))

    def get_fun_meta_by_tokens(self, tokens, is_union = False):
        meta_indices_lists = []
        for token in tokens:
            token = token.lower().strip()
            if token in self._fun_invert_index:
                meta_indices_lists.append(self._fun_invert_index[token])
        if len(meta_indices_lists) is 0:
            return []
        result_metadata = meta_indices_lists[0]
        for meta_index_set in meta_indices_lists[1:]:
            if is_union:
                result_metadata = result_metadata.union(meta_index_set)
            else:
                result_metadata = result_metadata.intersection(meta_index_set)
        return map(lambda index: copy.deepcopy(self._fun_meta_list[index]), sorted(result_metadata))

#
# Private
#

    def _translate_pkg_codes(self, pkg_dict):
        for pkg_name, fun_dicts in pkg_dict.iteritems():
            for fun_name, fun_dict in fun_dicts.iteritems():
                self._set_function(fun_name, pkg_name, fun_dict)

    def _set_function(self, name, pkg, opt = {}):
        name = name.strip()
        pkg = pkg.strip()
        meta_dict = opt
        meta_dict['name'] = name
        meta_dict['package'] = pkg
        name_tokens = tokenize_fun_name(name)
        if self._IF_FUN_NAME_AS_TOKEN:
            name_tokens.add(name.lower())
        self._fun_meta_list.append(meta_dict)
        self._set_fun_invert_index(name_tokens, len(self._fun_meta_list) - 1)

    def _set_fun_invert_index(self, name_tokens, meta_list_index):
        for token in name_tokens:
            for name in self._get_name_and_abbr_set(token):
                if name not in self._fun_invert_index:
                    self._fun_invert_index[name] = set()
                self._fun_invert_index[name].add(meta_list_index)

    def _get_name_and_abbr_set(self, name):
        result_set = {name}
        result_set.update(self._name_abbr_dict.get(name, {}))
        return result_set

