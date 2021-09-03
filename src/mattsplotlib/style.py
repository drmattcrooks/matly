import os
import stylesheets

INCLUDED_STYLESHEETS = ['mattsplotlib']
INCLUDED_STYLESHEET_FOLDER = f"{os.path.dirname(__file__)}/../stylesheets"
os.environ['mattsplotlib_stylesheet'] = 'mattsplotlib'


def use(stylesheet_path):
    if stylesheet_path in INCLUDED_STYLESHEETS:
        _set_environ_stylesheet(f"{INCLUDED_STYLESHEET_FOLDER}/{stylesheet_path}.mplstyle")
    else:
        _set_environ_stylesheet(stylesheet_path)


def _set_environ_stylesheet(path):
    os.environ['mattsplotlib_stylesheet'] = path