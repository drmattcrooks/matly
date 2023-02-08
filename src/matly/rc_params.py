import os
from builtins import eval


INCLUDED_STYLESHEETS = ['matly']
INCLUDED_STYLESHEET_FOLDER = f"{os.path.dirname(__file__)}/../stylesheets"
os.environ['matly_stylesheet'] = f"{INCLUDED_STYLESHEET_FOLDER}/matly.mplstyle"


def _read_stylesheet_from_os():
    path = os.environ.get('matly_stylesheet')
    with open(path, 'r') as file:
        lines = file.readlines()
    return lines


def _split_stylesheet_line(line):
    line = line.split('#')[0]
    key = line.split(':')[0].strip()
    value = line.split(':')[1].strip()
    return key, value


def _try_eval(value):
    try:
        return eval(value)
    except NameError:
        return value
    finally:
        raise ValueError(f"Unknown rcparam value: {value}")


def convert_stylesheet_to_dict():
    lines = _read_stylesheet_from_os()
    lines = [line for line in lines if line.strip() != '']
    lines = [line for line in lines if line[0] != '#']
    key_value_pairs = [_split_stylesheet_line(line) for line in lines]
    return {k: _try_eval(v) for k, v in key_value_pairs}
