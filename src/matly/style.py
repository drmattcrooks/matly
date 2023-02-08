import os
from matly.rc_params import INCLUDED_STYLESHEETS, INCLUDED_STYLESHEET_FOLDER


def use(stylesheet_path):
    if stylesheet_path in INCLUDED_STYLESHEETS:
        _set_environ_stylesheet(f"{INCLUDED_STYLESHEET_FOLDER}/{stylesheet_path}.mplstyle")
    else:
        _set_environ_stylesheet(stylesheet_path)


def _set_environ_stylesheet(path):
    os.environ['matly_stylesheet'] = path
