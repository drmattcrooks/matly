import os
from matly.rc_params import (
    INCLUDED_STYLESHEETS, INCLUDED_STYLESHEET_FOLDER,
    convert_stylesheet_to_dict
)
from matly import rcParams


def use(stylesheet_path):
    if stylesheet_path in INCLUDED_STYLESHEETS:
        _set_environ_stylesheet(f"{INCLUDED_STYLESHEET_FOLDER}/{stylesheet_path}.mplstyle")
    else:
        _set_environ_stylesheet(stylesheet_path)

    _update_rcparams_dict()


def _set_environ_stylesheet(path):
    os.environ['matly_stylesheet'] = path


def _update_rcparams_dict():
    new_rcParams = convert_stylesheet_to_dict()
    for key, value in new_rcParams.items():
        rcParams[key] = value