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
