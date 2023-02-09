from unittest.mock import patch, Mock
from matly import style


@patch.object(style, '_set_environ_stylesheet',
              return_value=Mock())
@patch.object(style, 'INCLUDED_STYLESHEET_FOLDER',
              return_value='test_path')
def test_use(test_path, set_mock):
    style_sheet = 'matly'
    style.use(style_sheet)
    set_mock.assert_called_with(
        f"{test_path}/matly.mplstyle")

    style_sheet = 'non-included/stylesheet/path'
    style.use(style_sheet)
    set_mock.assert_called_with("non-included/stylesheet/path")


@patch.object(style.os.environ, 'get', return_value='path')
def test_set(_):
    style._set_environ_stylesheet("path")
    assert style.os.environ.get('matly_stylesheet') == "path"
