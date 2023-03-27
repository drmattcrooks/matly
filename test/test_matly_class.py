from unittest.mock import patch, mock_open, Mock, call
from pdf2image import convert_from_bytes

from matly.matly_class import Matly, figureHandle
import matly.matly_class
from fixtures.mock_functions import mock_image

TEST_FIGURE_PATH = "test/fixtures/test_figure.pdf"
MOCKED_OPEN_FILE = open(TEST_FIGURE_PATH, 'rb')
MOCKED_TEMP_SAVED_PDF = open(TEST_FIGURE_PATH, 'rb').read()
MOCKED_CONVERTED = convert_from_bytes(open(TEST_FIGURE_PATH, 'rb').read())
MOCKED_UPLOT_KWARGS = {'x': [0, 1, 2], 'y': [3, 4, 5]}
MOCKED_MATLY_INIT_KWARGS = {'figure': Mock()}
MOCKED_PLOT_STYLE_DICT = {
    'line': dict(),
    'marker': {'line': dict()},
    'marker_symbol': None,
    'mode': 'lines'
}
MOCKED_RCPARAMS_LAYOUT_DICT = {
    'axes.edgecolor': 'mockGrey',
    'axes.linewidth': 2.123456,
    'axes.labelsize': 10.1111111,
    'axes.labelcolor': 'mockRed',
    'axes.facecolor': 'mockGrey',
    'axes.grid': False,
    'axes.grid.axis': 'x',
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.bottom': True,
    'xtick.top': False,
    'ytick.left': True,
    'ytick.right': False,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'xtick.major.size': 2,
    'ytick.major.size': 2,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    'xtick.color': 'Mockgrey',
    'ytick.color': 'Mockred',
    'lines.linewidth': 1.5
}
MOCKED_RCPARAMS_LAYOUT_DICT_NONE = {
    'axes.edgecolor': None,
    'axes.linewidth': None,
    'axes.labelsize': None,
    'axes.labelcolor': None,
    'axes.facecolor': None,
    'axes.grid': None,
    'axes.grid.axis': None,
    'axes.spines.left': None,
    'axes.spines.bottom': None,
    'axes.spines.top': None,
    'axes.spines.right': None,
    'xtick.bottom': None,
    'xtick.top': None,
    'ytick.left': None,
    'ytick.right': None,
    'xtick.direction': None,
    'ytick.direction': None,
    'xtick.major.size': None,
    'ytick.major.size': None,
    'xtick.major.width': None,
    'ytick.major.width': None,
    'xtick.color': None,
    'ytick.color': None,
    'lines.linewidth': None
}


def test_matly_is_class():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    assert ax.__class__.__name__ == 'Matly'
    assert ax.fig == MOCKED_MATLY_INIT_KWARGS['figure']


def test_matly_kwarg_errors():
    try:
        ax = Matly(
            **{
                k: v for k, v in MOCKED_MATLY_INIT_KWARGS.items()
                if k != 'figure'
            }
        )
    except Exception as error:
        assert error.__class__.__name__ == 'KeyError'
        assert str(error) == "'No figure handle passed when initiating Matly class'"


@patch.object(matly.matly_class, 'super')
def test_figure_handle_initiate(super_mock):
    fig = figureHandle()
    assert fig.__class__.__name__ == 'figureHandle'
    super_mock.assert_called()


def test_save_fig_pdf_jpeg():
    fig = figureHandle()
    fig.write_image = Mock()

    fig.savefig('filename.pdf')
    fig.write_image.assert_called_with('filename.pdf')

    fig.savefig('filename.jpg')
    fig.write_image.assert_called_with('filename.jpg')


def test_save_fig_png():
    fig = figureHandle()
    fig.save_png = Mock()
    filename = 'filename.png'
    fig.savefig(filename)
    fig.save_png.assert_called_with(filename)


def test_save_fig_error():
    fig = figureHandle()
    fig.save_png = Mock()
    filename = 'filename.xml'
    try:
        fig.savefig(filename)
    except Exception as error:
        assert error.__class__.__name__ == 'ValueError'
        assert str(error) == f"Unrecognised file format in filename: {filename}"


@patch.object(matly.matly_class.os, 'remove')
@patch.object(matly.matly_class, 'open',
              return_value = MOCKED_OPEN_FILE)
@patch.object(matly.matly_class, 'convert_from_bytes')
def test_save_png(convert_mock, open_mock, remove_mock):
    mocked_image = mock_image()
    convert_mock.return_value = [mocked_image]

    fig = figureHandle()
    fig.write_image = Mock()

    fig.savefig('filename.png')
    fig.write_image.assert_called_with('filename.pdf')
    open_mock.assert_called()
    args, _ = open_mock.call_args
    assert args[0] == 'filename.pdf'
    assert args[1] == 'rb'
    convert_mock.assert_called_with(MOCKED_TEMP_SAVED_PDF)
    mocked_image.save.assert_called()
    mocked_image.save.assert_called_with('filename.png')
    remove_mock.assert_called()
    remove_mock.assert_called_with('filename.pdf')


@patch.object(Matly, '_plot', side_effect=Mock())
def test_plot_function_exists_and_returns_none(_):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    assert 'plot' in dir(ax)
    assert ax.plot() is None


@patch.object(Matly, '_get_plot_defaults', side_effect=Mock())
def test_uplot_function_exists_and_returns_none(mocked_plot_trace):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    mocked_plot_trace.update = Mock()
    assert '_plot' in dir(ax)
    assert ax._plot(**MOCKED_UPLOT_KWARGS) is None


@patch.object(Matly, '_plot', side_effect=Mock())
def test_plot_calls_uplot(mocked_uplot):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax.plot()
    mocked_uplot.assert_called()


@patch.object(Matly, '_plot', side_effect=Mock())
def test_plot_takes_2_args(mocked_uplot):
    x = MOCKED_UPLOT_KWARGS['x']
    y = MOCKED_UPLOT_KWARGS['y']
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax.plot(x, y)
    _, called_kwargs = mocked_uplot.call_args
    assert called_kwargs == MOCKED_UPLOT_KWARGS


@patch.object(Matly, '_plot', side_effect=Mock())
def test_plot_takes_1_args(mocked_uplot):
    y = MOCKED_UPLOT_KWARGS['y']
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax.plot(y)
    _, called_kwargs = mocked_uplot.call_args
    assert called_kwargs == MOCKED_UPLOT_KWARGS


def test_get_plot_defaults_initiated_from_uplot():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._get_plot_defaults = Mock()
    ax._get_plot_defaults().update = Mock()
    ax._plot(**MOCKED_UPLOT_KWARGS)
    ax._get_plot_defaults.assert_called()


@patch.object(matly.matly_class.go, 'Scatter', side_effect=Mock())
def test_get_plot_defaults_returns_scatter(mocked_scatter):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    returned_trace = ax._get_plot_defaults()
    assert returned_trace == mocked_scatter()


def test_plot_update_trace():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._get_plot_defaults = Mock()
    ax._get_plot_defaults().update = Mock()
    ax._plot(**MOCKED_UPLOT_KWARGS)
    ax._get_plot_defaults().update.assert_called()
    _, kwargs = ax._get_plot_defaults().update.call_args
    expected_kwargs = dict(MOCKED_PLOT_STYLE_DICT)
    for k, v in MOCKED_UPLOT_KWARGS.items():
        expected_kwargs[k] = v

    assert kwargs == expected_kwargs


def test_plot_add_trace():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._get_plot_defaults = Mock()
    ax.fig.add_trace = Mock()
    ax._plot(**MOCKED_UPLOT_KWARGS)
    ax.fig.add_trace.assert_called()


def test_get_rcparam_value_returns_rcparam_value():
    matly.matly_class.rcParams = {'p1': 'v1'}
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = {'p1': 'v2'}

    assert matly.matly_class._get_rcparam_value('p1') == 'v1'


def test_get_rcparam_value_returns_rcparam_value():
    matly.matly_class.rcParams = dict()
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = {'p1': 'v2'}

    assert matly.matly_class._get_rcparam_value('p1') == 'v2'


def test_set_rcparams_layout_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ## Check for xaxis parameters
    assert 'xaxis' in ax.rcParams_layout.keys()
    assert type(ax.rcParams_layout['xaxis']) == dict
    assert 'tickfont' in ax.rcParams_layout['xaxis']
    assert 'title' in ax.rcParams_layout['xaxis']

    ## Check for yaxis parameters
    assert 'yaxis' in ax.rcParams_layout.keys()
    assert type(ax.rcParams_layout['yaxis']) == dict
    assert 'tickfont' in ax.rcParams_layout['yaxis']

    ## Check for title parameters
    assert 'title' in ax.rcParams_layout['yaxis']
    assert 'title' in ax.rcParams_layout.keys()
    assert type(ax.rcParams_layout['title']) == dict

    ## Check for background colour
    assert 'plot_bgcolor' in ax.rcParams_layout
    assert 'paper_bgcolor' in ax.rcParams_layout

    # Check axis line color and width
    assert 'linecolor' in ax.rcParams_layout['xaxis']
    assert 'linewidth' in ax.rcParams_layout['xaxis']
    assert 'linecolor' in ax.rcParams_layout['yaxis']
    assert 'linewidth' in ax.rcParams_layout['yaxis']

    # Show grid lines
    assert 'showgrid' in ax.rcParams_layout['xaxis']
    assert 'showgrid' in ax.rcParams_layout['yaxis']

    # zero lines
    assert 'zeroline' in ax.rcParams_layout['xaxis']
    assert 'zeroline' in ax.rcParams_layout['yaxis']

    # title text size
    assert 'font' in ax.rcParams_layout['title']
    assert 'font' in ax.rcParams_layout['xaxis']['title']
    assert 'font' in ax.rcParams_layout['yaxis']['title']


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_layout_axis_color_and_width(rcparams_mock):
    rcparams_mock_returns = [Mock(), Mock(), Mock(), Mock()]
    rcparams_mock.side_effect = tuple(rcparams_mock_returns)

    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_axis_color_and_width()

    assert rcparams_mock.call_count == 4
    assert rcparams_mock.call_args_list == [
        call('axes.edgecolor'), call('axes.linewidth'),
        call('axes.edgecolor'), call('axes.linewidth')
    ]
    assert ax.rcParams_layout['xaxis']['linecolor'] == rcparams_mock_returns[0]
    assert ax.rcParams_layout['xaxis']['linewidth'] == rcparams_mock_returns[1]
    assert ax.rcParams_layout['yaxis']['linecolor'] == rcparams_mock_returns[2]
    assert ax.rcParams_layout['yaxis']['linewidth'] == rcparams_mock_returns[3]


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_layout_background_color(rcparams_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_background_color()

    assert rcparams_mock.call_count == 2
    assert rcparams_mock.call_args_list == [
        call('axes.facecolor'), call('axes.facecolor')
    ]
    assert ax.rcParams_layout['plot_bgcolor'] == rcparams_mock.return_value
    assert ax.rcParams_layout['paper_bgcolor'] == rcparams_mock.return_value


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_layout_axis_label_fonts(rcparams_mock):
    size_mock = Mock()
    color_mock = Mock()
    rcparams_mock.side_effect = tuple([
        size_mock, size_mock, color_mock,
        size_mock, color_mock
    ])

    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_axis_label_fonts()

    assert rcparams_mock.call_count == 5
    assert rcparams_mock.call_args_list == [
        call('axes.labelsize'), call('axes.labelsize'),
        call('axes.labelcolor'), call('axes.labelsize'), call('axes.labelcolor')
    ]
    assert ax.rcParams_layout['title']['font']['size'] == size_mock
    assert ax.rcParams_layout['xaxis']['title']['font']['size'] == size_mock
    assert ax.rcParams_layout['xaxis']['title']['font']['color'] == color_mock
    assert ax.rcParams_layout['yaxis']['title']['font']['size'] == size_mock
    assert ax.rcParams_layout['yaxis']['title']['font']['color'] == color_mock


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[False])
def test_set_rcparams_layout_grid_none(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_grid()

    assert params_mock.call_count == 1
    params_mock.assert_called_with('axes.grid')
    ax.rcParams_layout['xaxis']['showgrid'] == False
    ax.rcParams_layout['yaxis']['showgrid'] == False


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, 'x'])
def test_set_rcparams_layout_grid_x(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_grid()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('axes.grid'), call('axes.grid.axis')]
    ax.rcParams_layout['xaxis']['showgrid'] == True
    ax.rcParams_layout['yaxis']['showgrid'] == False


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, 'y'])
def test_set_rcparams_layout_grid_y(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_grid()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('axes.grid'), call('axes.grid.axis')]
    ax.rcParams_layout['xaxis']['showgrid'] == False
    ax.rcParams_layout['yaxis']['showgrid'] == True


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, 'both'])
def test_set_rcparams_layout_grid_both(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_grid()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('axes.grid'), call('axes.grid.axis')]
    ax.rcParams_layout['xaxis']['showgrid'] == True
    ax.rcParams_layout['yaxis']['showgrid'] == True


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[False, True])
def test_set_rcparams_layout_xticks_bottom(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_xticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('xtick.top'), call('xtick.bottom')]
    ax.rcParams_layout['xaxis']['side'] == 'bottom'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, False])
def test_set_rcparams_layout_xticks_top(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_xticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('xtick.top'), call('xtick.bottom')]
    ax.rcParams_layout['xaxis']['side'] == 'top'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, True])
def test_set_rcparams_layout_xticks_both(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_xticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('xtick.top'), call('xtick.bottom')]
    ax.rcParams_layout['xaxis']['side'] == 'bottom'
    ax.rcParams_layout['xaxis']['mirror'] == 'allticks'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, False])
def test_set_rcparams_layout_yticks_left(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_yticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('ytick.left'), call('ytick.right')]
    ax.rcParams_layout['yaxis']['side'] == 'left'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[False, True])
def test_set_rcparams_layout_yticks_right(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_yticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('ytick.left'), call('ytick.right')]
    ax.rcParams_layout['yaxis']['side'] == 'right'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=[True, True])
def test_set_rcparams_layout_yticks_both(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_yticks()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('ytick.left'), call('ytick.right')]
    ax.rcParams_layout['yaxis']['side'] == 'left'
    ax.rcParams_layout['yaxis']['mirror'] == 'allticks'


@patch.object(matly.matly_class, '_get_rcparam_value', side_effect=['in', 'in'])
def test_set_rcparams_layout_ticks_inside_out_in(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_ticks_inside_out()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('xtick.direction'), call('ytick.direction')]
    ax.rcParams_layout['xaxis']['ticks'] = 'inside'
    ax.rcParams_layout['yaxis']['ticks'] = 'inside'


@patch.object(matly.matly_class, '_get_rcparam_value', return_value='out')
def test_set_rcparams_layout_ticks_inside_out_out(params_mock):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_ticks_inside_out()

    assert params_mock.call_count == 4
    params_mock.call_args_list == [
        call('xtick.direction'), call('xtick.direction'),
        call('ytick.direction'), call('ytick.direction')
    ]
    ax.rcParams_layout['xaxis']['ticks'] = 'outside'
    ax.rcParams_layout['yaxis']['ticks'] = 'outside'


@patch.object(matly.matly_class, '_get_rcparam_value')
def test_set_rcparams_layout_tick_size(params_mock):
    params_return_values = [Mock(), Mock(), Mock(), Mock()]
    params_mock.side_effect = params_return_values

    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_tick_size()

    assert params_mock.call_count == 4
    params_mock.call_args_list == [
        call('xtick.major.size'), call('xtick.major.width'),
        call('ytick.major.size'), call('ytick.major.width')
    ]
    ax.rcParams_layout['xaxis']['ticklen'] == params_return_values[0]
    ax.rcParams_layout['yaxis']['ticklen'] == params_return_values[1]
    ax.rcParams_layout['xaxis']['tickwidth'] == params_return_values[2]
    ax.rcParams_layout['yaxis']['tickwidth'] == params_return_values[3]


@patch.object(matly.matly_class, '_get_rcparam_value')
def test_set_rcparams_layout_tick_color(params_mock):
    params_return_values = [Mock(), Mock()]
    params_mock.side_effect = params_return_values

    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout_tick_color()

    assert params_mock.call_count == 2
    params_mock.call_args_list == [call('xtick.color'), call('ytick.color')]
    ax.rcParams_layout['xaxis']['color'] == params_return_values[0]
    ax.rcParams_layout['yaxis']['color'] == params_return_values[1]


@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_xticks',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_yticks',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_ticks_inside_out',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_tick_size',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_tick_color',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_grid',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_axis_label_fonts',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_background_color',
    return_value=Mock()
)
@patch.object(
    matly.matly_class.Matly,
    '_set_rcparams_layout_axis_color_and_width',
    return_value=Mock()
)
def test_set_rcparams_layout(
        color_width_mock, background_mock, axis_label_mock, grid_mock,
        tick_color_mock, tick_size_mock, inout_mock, ytick_mock, xtick_mock
):
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()

    color_width_mock.assert_called()
    background_mock.assert_called()
    axis_label_mock.assert_called()
    grid_mock.assert_called()
    tick_color_mock.assert_called()
    tick_size_mock.assert_called()
    inout_mock.assert_called()
    ytick_mock.assert_called()
    xtick_mock.assert_called()


def test_set_rcparams_layout_ticks_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ## Check for tick parameters
    assert 'ticks' in ax.rcParams_layout['xaxis']
    assert 'ticks' in ax.rcParams_layout['yaxis']

    ## Check for ticklen parameters
    assert 'ticklen' in ax.rcParams_layout['xaxis']
    assert 'ticklen' in ax.rcParams_layout['yaxis']

    ## Check for tickwidth parameters
    assert 'tickwidth' in ax.rcParams_layout['xaxis']
    assert 'tickwidth' in ax.rcParams_layout['yaxis']

    ## Check for tick color parameters
    assert 'color' in ax.rcParams_layout['xaxis']
    assert 'color' in ax.rcParams_layout['yaxis']

    ## Check for tick font parameters
    assert 'family' in ax.rcParams_layout['xaxis']['tickfont']
    assert 'family' in ax.rcParams_layout['yaxis']['tickfont']
    assert 'size' in ax.rcParams_layout['xaxis']['tickfont']
    assert 'size' in ax.rcParams_layout['yaxis']['tickfont']

    # Check for mirror in parameters
    assert 'mirror' in ax.rcParams_layout['xaxis']
    assert 'mirror' in ax.rcParams_layout['yaxis']

    # Check for side in parameters
    assert 'side' in ax.rcParams_layout['xaxis']
    assert 'side' in ax.rcParams_layout['yaxis']

    # Check for direction in parameters
    assert 'ticks' in ax.rcParams_layout['xaxis']
    assert 'ticks' in ax.rcParams_layout['yaxis']


def test_rcparams_spines_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    assert sorted(list(ax.rcparams_spines.keys())) == sorted(['bottom', 'left', 'right', 'top'])


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
@patch.object(matly.matly_class, 'SpineClass', return_value=Mock())
def test_set_rcparams_spines(spine_mock, rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ax._set_rcparams_spines()

    assert spine_mock.call_count == 4
    assert rcparam_mock.call_count == 8
    args_list = spine_mock.call_args_list
    assert args_list[0][0] == ('top', rcparam_returns[0], rcparam_returns[1])
    assert args_list[1][0] == ('left', rcparam_returns[2], rcparam_returns[3])
    assert args_list[2][0] == ('bottom', rcparam_returns[4], rcparam_returns[5])
    assert args_list[3][0] == ('right', rcparam_returns[6], rcparam_returns[7])
    assert ax.rcParams_spines == {
        'top': spine_mock.return_value,
        'left': spine_mock.return_value,
        'right': spine_mock.return_value,
        'bottom': spine_mock.return_value
    }


def test_set_rcparams_lines_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    assert 'rcparams_lines' in dir(ax)
    assert type(ax.rcparams_lines) == dict
    assert 'width' in list(ax.rcparams_lines)
    assert 'dash' in list(ax.rcparams_lines)
    assert 'color' in list(ax.rcparams_lines)


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_lines(rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ax._set_rcparams_lines()

    assert rcparam_mock.call_count == 3
    args_list = rcparam_mock.call_args_list
    assert args_list == [call('lines.linewidth'), call('lines.linestyle'), call('lines.color')]
    assert ax.rcparams_lines['width'] == rcparam_returns[0]
    assert ax.rcparams_lines['dash'] == rcparam_returns[1]
    assert ax.rcparams_lines['color'] == rcparam_returns[2]


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_markers(rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ax._set_rcparams_markers()

    assert rcparam_mock.call_count == 5
    assert ax.rcparams_markers['symbol'] == rcparam_returns[0]
    assert ax.rcparams_markers['color'] == rcparam_returns[1]
    assert ax.rcparams_markers['size'] == rcparam_returns[2]
    assert ax.rcparams_markers['line']['color'] == rcparam_returns[3]
    assert ax.rcparams_markers['line']['width'] == rcparam_returns[4]


def test_rcparams_patch_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    assert 'rcparams_patch' in dir(ax)
    assert type(ax.rcparams_patch) == dict
    assert ax.rcparams_patch == {
        'linewidth': None,
        'facecolor': None,
        'edgecolor': None
    }


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_patch(rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ax._set_rcparams_patch()

    assert rcparam_mock.call_count == 3
    assert ax.rcparams_patch['linewidth'] == rcparam_returns[0]
    assert ax.rcparams_patch['facecolor'] == rcparam_returns[1]
    assert ax.rcparams_patch['edgecolor'] == rcparam_returns[2]


def test_rcparams_font_structure():
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    assert 'rcparams_font' in dir(ax)
    assert type(ax.rcparams_font) == dict
    assert ax.rcparams_font == {
        'family': None,
        'weight': None,
        'size': None
    }


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_set_rcparams_font(rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    ax._set_rcparams_font()

    assert rcparam_mock.call_count == 3
    assert ax.rcparams_font['family'] == rcparam_returns[0]
    assert ax.rcparams_font['weight'] == rcparam_returns[1]
    assert ax.rcparams_font['size'] == rcparam_returns[2]


@patch.object(matly.matly_class, '_get_rcparam_value', return_value=Mock())
def test_figsize(rcparam_mock):
    rcparam_returns = [Mock(), Mock(), Mock()]
    rcparam_mock.side_effect = tuple(rcparam_returns)
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    assert ax.rcparams_figsize == {'figsize': None}

    ax._set_rcparams_figsize()

    assert rcparam_mock.call_count == 1
    args_list = rcparam_mock.call_args_list
    assert args_list == [call('figure.figsize')]
    assert ax.rcparams_figsize['figsize'] == rcparam_returns[0]
