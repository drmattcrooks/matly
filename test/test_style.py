from unittest.mock import patch, Mock

from mattsplotlib import style

from fixtures.mock_functions import mock_os_environ


@patch.object(style, '_set_environ_stylesheet',
              return_value=Mock())
@patch.object(style, 'INCLUDED_STYLESHEET_FOLDER',
              return_value='test_path')
def test_use(test_path, set_mock):
    style_sheet = 'mattsplotlib'
    style.use(style_sheet)
    set_mock.assert_called_with(
        f"{test_path}/mattsplotlib.mplstyle")

    style_sheet = 'non-included/stylesheet/path'
    style.use(style_sheet)
    set_mock.assert_called_with("non-included/stylesheet/path")


def test_set():
    style.os = mock_os_environ()
    style._set_environ_stylesheet("path")
    assert style.os.environ['mattsplotlib_stylesheet'] == "path"