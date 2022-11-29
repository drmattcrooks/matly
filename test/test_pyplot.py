from unittest.mock import Mock
from unittest.mock import patch

import matly.pyplot as mplt

from fixtures.mock_functions import mock_class


@patch.object(mplt, 'figureHandle', return_value = Mock)
def test_figure_returns_handle(figure_handle_mock):
    assert mplt.figure() == figure_handle_mock()


def test_rows_and_cols():
    rows, cols = mplt._get_rows_and_columns()
    assert rows, cols == (1, 1)

    rows, cols = mplt._get_rows_and_columns(2)
    assert rows, cols == (2, 1)

    rows, cols = mplt._get_rows_and_columns(2, 3)
    assert rows, cols == (2, 3)


# @patch.object(mplt, 'make_subplots', return_value=Mock())
@patch.object(mplt, '_generate_axes')
@patch.object(mplt, '_create_subplots_layout')
@patch.object(mplt, '_create_subplot_figurehandle')
@patch.object(mplt, '_create_make_subplots_kwargs', return_value=(1, 2))
@patch.object(mplt, '_get_rows_and_columns', return_value=(1, 2))
def test_subplots(get_rows_and_columns_mock,
                  create_make_subplots_kwargs_mock,
                  figure_mock,
                  subplot_layout_mock,
                  generate_axes_mock):

    figure_mock_return = Mock()
    figure_mock.return_value = figure_mock_return

    subplot_layout_return = Mock()
    subplot_layout_mock.return_value = subplot_layout_return

    mplt.subplots(figsize=(12, 7))
    _, kwargs = generate_axes_mock.call_args

    generate_axes_mock.assert_called()
    assert kwargs['rows'] == 1
    assert kwargs['cols'] == 2
    assert kwargs['figsize'] == (12, 7)
    assert kwargs['figure'] == figure_mock_return
    assert kwargs['subplot_layout'] == subplot_layout_return


@patch.object(mplt, 'figureHandle')
@patch.object(mplt, 'make_subplots')
def test_create_subplots(make_subplots_mock, figureHandle_mock):
    subplot_figure_mock = mock_class(
        ['layout', '_grid_ref'], [{}, 'test_grid_ref'])
    make_subplots_mock.return_value = subplot_figure_mock

    figure_mock = mock_class(['_grid_ref'])
    figureHandle_mock.return_value = figure_mock

    returned_figure = mplt._create_subplot_figurehandle(1, 1, {})
    figureHandle_mock.assert_called
    _, kwargs = figureHandle_mock.call_args
    assert kwargs['layout'] == subplot_figure_mock.layout
    assert returned_figure._grid_ref == subplot_figure_mock._grid_ref


def test_create_subplots_layout():
    kwargs = {'sharex': True}
    expected_subplots_layout = {
        'sharedx': True,
        'sharedy': False,
        'rows': 1,
        'cols': 2
    }
    returned_subplots_layout = mplt._create_subplots_layout(
        kwargs, 1, 2)
    assert expected_subplots_layout == returned_subplots_layout


def test_create_make_subplots_kwargs():
    kwargs_returned = mplt._create_make_subplots_kwargs(sharex=True)
    assert kwargs_returned == {'shared_xaxes': True, 'shared_yaxes': False}

    kwargs_returned = mplt._create_make_subplots_kwargs(sharey=True)
    assert kwargs_returned == {'shared_xaxes': False, 'shared_yaxes': True}


@patch.object(mplt, 'Matly', return_value=Mock())
def test_generate_axes_single(matly_mock):
    figure_mock = Mock()
    figsize_mock = Mock()
    subplot_layout_mock = Mock()
    figure, axes = mplt._generate_axes(rows=1,
                                       cols=1,
                                       figure=figure_mock,
                                       figsize=figsize_mock,
                                       subplot_layout=subplot_layout_mock)
    _, called_kwargs = matly_mock.call_args

    matly_mock.assert_called
    assert called_kwargs['row'] == 1
    assert called_kwargs['col'] == 1
    assert called_kwargs['figure'] == figure_mock
    assert called_kwargs['figsize'] == figsize_mock
    assert called_kwargs['subplot_layout'] == subplot_layout_mock
    assert figure == figure_mock


@patch.object(mplt, 'Matly', return_value=Mock())
def test_generate_axes_2col(matly_mock):
    figure_mock = Mock()
    figsize_mock = Mock()
    subplot_layout_mock = Mock()
    figure, axes = mplt._generate_axes(rows=1,
                                       cols=2,
                                       figure=figure_mock,
                                       figsize=figsize_mock,
                                       subplot_layout=subplot_layout_mock)
    _, called_kwargs = matly_mock.call_args

    matly_mock.assert_called
    assert matly_mock.call_count == 2
    assert called_kwargs['row'] == 1
    assert called_kwargs['col'] == 2
    assert called_kwargs['figure'] == figure_mock
    assert called_kwargs['figsize'] == figsize_mock
    assert called_kwargs['subplot_layout'] == subplot_layout_mock
    assert figure == figure_mock
    assert axes.shape == (2, )


@patch.object(mplt, 'Matly', return_value=Mock())
def test_generate_axes_2row(matly_mock):
    figure_mock = Mock()
    figsize_mock = Mock()
    subplot_layout_mock = Mock()
    figure, axes = mplt._generate_axes(rows=2,
                                       cols=1,
                                       figure=figure_mock,
                                       figsize=figsize_mock,
                                       subplot_layout=subplot_layout_mock)
    _, called_kwargs = matly_mock.call_args

    matly_mock.assert_called
    assert matly_mock.call_count == 2
    assert called_kwargs['row'] == 2
    assert called_kwargs['col'] == 1
    assert called_kwargs['figure'] == figure_mock
    assert called_kwargs['figsize'] == figsize_mock
    assert called_kwargs['subplot_layout'] == subplot_layout_mock
    assert figure == figure_mock
    assert axes.shape == (2,)


@patch.object(mplt, 'Matly', return_value=Mock())
def test_generate_axes_grid(matly_mock):
    figure_mock = Mock()
    figsize_mock = Mock()
    subplot_layout_mock = Mock()
    figure, axes = mplt._generate_axes(rows=2,
                                       cols=3,
                                       figure=figure_mock,
                                       figsize=figsize_mock,
                                       subplot_layout=subplot_layout_mock)
    _, called_kwargs = matly_mock.call_args

    matly_mock.assert_called
    assert matly_mock.call_count == 6
    assert called_kwargs['row'] == 2
    assert called_kwargs['col'] == 3
    assert called_kwargs['figure'] == figure_mock
    assert called_kwargs['figsize'] == figsize_mock
    assert called_kwargs['subplot_layout'] == subplot_layout_mock
    assert figure == figure_mock
    assert axes.shape == (2, 3)
