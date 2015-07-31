import os
import re
import csv

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_NAME_ABBR_PATH = os.path.join(_SCRIPT_DIR, 'name_abbr.tab')
_CAPITAL_NUM_REGEX = re.compile('[0-9]+|[A-Z]+(?![^0-9A-Z])|[A-Z](?=[^0-9A-Z])')

def get_name_abbr_dict(name_abbr_path = _NAME_ABBR_PATH):
    name_abbr_dict = {}
    with open(name_abbr_path, 'r') as f:
        for line in csv.reader(f, delimiter = '\t'):
            abbr_set = set(map(lambda x: x.strip().lower(), line))
            for abbr in abbr_set:
                if abbr not in name_abbr_dict:
                    name_abbr_dict[abbr] = set()
                name_abbr_dict[abbr].update(abbr_set)
    return name_abbr_dict

def tokenize_fun_name(name):
    snake_tokens = _tokenize_snake_name(name)
    def camel_name_reduction(token_set, snake_name):
        token_set.update(set(map(lambda x: x.lower(),
            _tokenize_camel_name(snake_name))))
        return token_set
    return reduce(camel_name_reduction, snake_tokens, set())

#
# Private
#

def _tokenize_camel_name(name):
    name = name.strip()
    if len(name) == 0:
        return set()
    last_match_start = 0
    tokens = set()
    for match in _CAPITAL_NUM_REGEX.finditer(name):
        if match.start() <= last_match_start:
            continue
        tokens.add(name[last_match_start:match.start()])
        last_match_start = match.start()
    else:
        if last_match_start < len(name):
            tokens.add(name[last_match_start:len(name)])
    return tokens

def _tokenize_snake_name(name):
    return filter(_empty_str_filter, set(name.strip().split('_')))

def _empty_str_filter(st):
    return len(st.strip()) != 0

