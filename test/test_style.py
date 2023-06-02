from unittest.mock import patch, Mock
from matly import style

RCPARAMS_MOCK = {
    'key1': Mock(),
    'key2': Mock()
}


@patch.object(style, '_update_rcparams_dict')
@patch.object(style, '_set_environ_stylesheet',
              return_value=Mock())
@patch.object(style, 'INCLUDED_STYLESHEET_FOLDER',
              return_value='test_path')
def test_use(test_path, set_mock, update_mock):
    style_sheet = 'matly'
    style.use(style_sheet)
    set_mock.assert_called_with(
        f"{test_path}/matly.mplstyle")

    style_sheet = 'non-included/stylesheet/path'
    style.use(style_sheet)
    set_mock.assert_called_with("non-included/stylesheet/path")
    update_mock.assert_called()


@patch.object(style.os.environ, 'get', return_value='path')
def test_set(_):
    style._set_environ_stylesheet("path")
    assert style.os.environ.get('matly_stylesheet') == "path"



@patch('matly.style.rcParams', RCPARAMS_MOCK)
@patch.object(style, 'convert_stylesheet_to_dict')
def test_update_rcparams_dict(style_mock):
    new_rcparams_mock_dict = {
        'key2': Mock(),
        'key3': Mock()
    }
    style_mock.return_value = new_rcparams_mock_dict

    style._update_rcparams_dict()

    expected_rcparams_dict = {
        'key1': RCPARAMS_MOCK['key1'],
        'key2': new_rcparams_mock_dict['key2'],
        'key3': new_rcparams_mock_dict['key3'],
    }

    assert RCPARAMS_MOCK == expected_rcparams_dict
