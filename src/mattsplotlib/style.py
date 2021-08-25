import os
import stylesheets

INCLUDED_STYLESHEETS = ['mattsplotlib']
INCLUDED_STYLESHEET_FOLDER = f"{os.path.dirname(__file__)}/../stylesheets"
os.environ['mattsplotlib_stylesheet'] = 'mattsplotlib'
# CWD = os.

def use(stylesheet_path):
    if stylesheet_path in INCLUDED_STYLESHEETS:
        os.environ['mattsplotlib_stylesheet'] = f"{INCLUDED_STYLESHEET_FOLDER}/{stylesheet_path}.mplstyle"
    else:
        os.environ['mattsplotlib_stylesheet'] = stylesheet_path

    with open(os.environ['mattsplotlib_stylesheet']) as text:
        print(str(text.read()))

    os.environ['mattsplotlib_stylesheet'] = stylesheet_path
