class ColorStr:

    _HEADER = '\033[95m'
    _OKBLUE = '\033[94m'
    _OKGREEN = '\033[92m'
    _WARNING = '\033[93m'
    _FAIL = '\033[91m'
    _ENDC = '\033[0m'
    _BOLD = '\033[1m'
    _UNDERLINE = '\033[4m'

    @staticmethod
    def color_fun_name(fun):
        return ColorStr._UNDERLINE + ColorStr._BOLD + ColorStr._OKBLUE + fun + ColorStr._ENDC

    @staticmethod
    def color_pkg_name(pkg):
        return ColorStr._HEADER + pkg + ColorStr._ENDC


