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
@patch.object(matly.rc_params, '_try_eval')
def test_convert_stylesheet_to_dict(mock_try_eval, _):
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


@patch.object(matly.rc_params, 'eval', return_value=True)
def test_try_eval_works(_):
    assert matly.rc_params._try_eval('True') == True


@patch.object(matly.rc_params, 'eval', return_value='white')
def test_try_eval_nameerror(mock_eval):
    response = matly.rc_params._try_eval('white')
    mock_eval.assert_called
    assert response == 'white'

