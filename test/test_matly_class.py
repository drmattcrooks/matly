from unittest.mock import patch, mock_open, Mock
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
    'axes.spines.top': False
}
MOCKED_RCPARAMS_LAYOUT_DICT_NONE = {
    'axes.edgecolor': None,
    'axes.linewidth': None,
    'axes.labelsize': None,
    'axes.labelcolor': None,
    'axes.facecolor': None,
    'axes.grid': None,
    'axes.grid.axis': None,
    'axes.spines.top': None
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


def test_set_rcparams_layout_xaxis_value_defaults():
    matly.matly_class.rcParams = dict()
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['linecolor'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.edgecolor']
    assert ax.rcParams_layout['xaxis']['linewidth'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.linewidth']
    assert ax.rcParams_layout['xaxis']['title']['font']['size'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.labelsize']
    assert ax.rcParams_layout['xaxis']['title']['font']['color'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.labelcolor']


def test_set_rcparams_layout_xaxis_value_rcparams():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT_NONE
    matly.matly_class.rcParams = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['linecolor'] == \
           matly.matly_class.rcParams['axes.edgecolor']
    assert ax.rcParams_layout['xaxis']['linewidth'] == \
           matly.matly_class.rcParams['axes.linewidth']
    assert ax.rcParams_layout['xaxis']['title']['font']['size'] == \
           matly.matly_class.rcParams['axes.labelsize']
    assert ax.rcParams_layout['xaxis']['title']['font']['color'] == \
           matly.matly_class.rcParams['axes.labelcolor']


def test_set_rcparams_layout_yaxis_value_defaults():
    matly.matly_class.rcParams = dict()
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['yaxis']['linecolor'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.edgecolor']
    assert ax.rcParams_layout['yaxis']['linewidth'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.linewidth']
    assert ax.rcParams_layout['yaxis']['title']['font']['size'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.labelsize']
    assert ax.rcParams_layout['yaxis']['title']['font']['color'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.labelcolor']


def test_set_rcparams_layout_yaxis_value_rcparams():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT_NONE
    matly.matly_class.rcParams = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['yaxis']['linecolor'] == \
           matly.matly_class.rcParams['axes.edgecolor']
    assert ax.rcParams_layout['yaxis']['linewidth'] == \
           matly.matly_class.rcParams['axes.linewidth']
    assert ax.rcParams_layout['yaxis']['title']['font']['size'] == \
           matly.matly_class.rcParams['axes.labelsize']
    assert ax.rcParams_layout['yaxis']['title']['font']['color'] == \
           matly.matly_class.rcParams['axes.labelcolor']


def test_set_rcparams_layout_background_color_defaults():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT
    matly.matly_class.rcParams = dict()
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['plot_bgcolor'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.facecolor']
    assert ax.rcParams_layout['paper_bgcolor'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.facecolor']


def test_set_rcparams_layout_background_color_rcparams():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT_NONE
    matly.matly_class.rcParams = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['plot_bgcolor'] == \
           matly.matly_class.rcParams['axes.facecolor']
    assert ax.rcParams_layout['paper_bgcolor'] == \
           matly.matly_class.rcParams['axes.facecolor']


def test_set_rcparams_layout_title_fontsize_defaults():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT
    matly.matly_class.rcParams = dict()
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['title']['font']['size'] == \
           matly.matly_class.MATLY_RCPARAMS_DEFAULTS['axes.labelsize']


def test_set_rcparams_layout_title_fontsize_rcparams():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT_NONE
    matly.matly_class.rcParams = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['title']['font']['size'] == \
           matly.matly_class.rcParams['axes.labelsize']


def test_set_rcparams_layout_grid_defaults():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT
    matly.matly_class.rcParams = dict()
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    # Grid Off
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == False
    assert ax.rcParams_layout['yaxis']['showgrid'] == False

    # Grid On x
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'x'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == True
    assert ax.rcParams_layout['yaxis']['showgrid'] == False

    # Grid On y
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'y'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == False
    assert ax.rcParams_layout['yaxis']['showgrid'] == True

    # Grid On both
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'both'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == True
    assert ax.rcParams_layout['yaxis']['showgrid'] == True


def test_set_rcparams_layout_grid_rcparams():
    matly.matly_class.MATLY_RCPARAMS_DEFAULTS = MOCKED_RCPARAMS_LAYOUT_DICT_NONE
    matly.matly_class.rcParams = MOCKED_RCPARAMS_LAYOUT_DICT
    ax = Matly(**MOCKED_MATLY_INIT_KWARGS)

    # Grid Off
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = False
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == False
    assert ax.rcParams_layout['yaxis']['showgrid'] == False

    # Grid On x
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'x'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == True
    assert ax.rcParams_layout['yaxis']['showgrid'] == False

    # Grid On y
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'y'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == False
    assert ax.rcParams_layout['yaxis']['showgrid'] == True

    # Grid On both
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid'] = True
    MOCKED_RCPARAMS_LAYOUT_DICT['axes.grid.axis'] = 'both'
    ax._set_rcparams_layout()
    assert ax.rcParams_layout['xaxis']['showgrid'] == True
    assert ax.rcParams_layout['yaxis']['showgrid'] == True
