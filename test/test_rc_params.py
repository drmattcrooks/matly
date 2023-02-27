from unittest.mock import patch, Mock
import matly.rc_params

MOCK_STYLESHEET = [
    '## See https://matplotlib.org/api/axis_api.html#matplotlib.axis.Tick\n',
    'xtick.top           : False   ## draw ticks on the top side\n',
    '\n',
    'xtick.bottom        : True    ## draw ticks on the bottom side',
    'figure.figsize      : (10, 7)',
    'figure.facecolor    : white'
]


def test_split_stylesheet_line_with_comment():
    line = 'key    : value #####'
    key, value = matly.rc_params._split_stylesheet_line(line)
    assert key == 'key'
    assert value == 'value'


@patch.object(matly.rc_params, '_read_stylesheet_from_os', return_value=MOCK_STYLESHEET)
@patch.object(matly.rc_params, '_read_stylesheet_from_path')
@patch.object(matly.rc_params, '_try_eval')
def test_convert_stylesheet_to_dict_from_os(
        mock_try_eval, mock_read_from_path, mock_read_from_os):
    mock_try_eval.side_effect = [
        False, True, (10, 7), 'white'
    ]
    rcparams = matly.rc_params.convert_stylesheet_to_dict()
    assert rcparams == {
        'xtick.top': False,
        'xtick.bottom': True,
        'figure.figsize': (10, 7),
        'figure.facecolor': 'white'
    }
    mock_read_from_os.assert_called()
    mock_read_from_path.assert_not_called()


@patch.object(matly.rc_params, '_read_stylesheet_from_os')
@patch.object(matly.rc_params, '_read_stylesheet_from_path', return_value=MOCK_STYLESHEET)
@patch.object(matly.rc_params, '_try_eval')
def test_convert_stylesheet_to_dict_from_path(
        mock_try_eval, mock_read_from_path, mock_read_from_os):
    mock_try_eval.side_effect = [
        False, True, (10, 7), 'white'
    ]
    rcparams = matly.rc_params.convert_stylesheet_to_dict('path')
    assert rcparams == {
        'xtick.top': False,
        'xtick.bottom': True,
        'figure.figsize': (10, 7),
        'figure.facecolor': 'white'
    }
    mock_read_from_os.assert_not_called()
    mock_read_from_path.assert_called()
    mock_read_from_path.assert_called_with('path')


@patch.object(matly.rc_params, 'eval', return_value=True)
def test_try_eval_works(_):
    assert matly.rc_params._try_eval('True') == True


@patch.object(matly.rc_params, 'eval', return_value='white')
def test_try_eval_nameerror(mock_eval):
    response = matly.rc_params._try_eval('white')
    mock_eval.assert_called
    assert response == 'white'


@patch.object(matly.rc_params, '_read_stylesheet_from_path', return_value=['some lines'])
@patch.object(matly.rc_params.os.environ, 'get', return_value='matly_path')
def test_read_stylesheet_from_os(mock_os, read_mock):
    matly.rc_params._read_stylesheet_from_os()
    mock_os.assert_called()
    read_mock.assert_called()
    read_mock.assert_called_with('matly_path')


def test_read_stylesheet_from_path():
    read_lines = matly.rc_params._read_stylesheet_from_path(
        f"test/fixtures/stylesheet1.mplstyle")
    expected_lines = [
        'This is line 1 of style sheet 1\n',
        'This is line 2 of style sheet 1'
    ]
    assert read_lines == expected_lines