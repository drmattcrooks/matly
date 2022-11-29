#    __   ___
#   /  |_/  / _   /_  /
#  / /|_// / __| /   /   /  /
# /_/   /_/ /_///__ /__ /__/
#                       __/



import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from matly.matly_class import Matly, figureHandle
from matly import style


def figure():
    return figureHandle()


def _get_rows_and_columns(*args):
    if len(args) == 0:
        rows = 1
        cols = 1
    elif len(args) == 1:
        rows = args[0]
        cols = 1
    elif len(args) == 2:
        rows = args[0]
        cols = args[1]
    return rows, cols


def _create_make_subplots_kwargs(**kwargs):
    make_subplots_kwargs = dict()
    make_subplots_kwargs['shared_yaxes'] = kwargs.get('sharey', False)
    make_subplots_kwargs['shared_xaxes'] = kwargs.get('sharex', False)
    return make_subplots_kwargs


def subplots(*args, **kwargs):
    rows, cols = _get_rows_and_columns(*args)
    make_subplots_kwargs = _create_make_subplots_kwargs(**kwargs)
    figure = _create_subplot_figurehandle(rows, cols, make_subplots_kwargs)

    figsize = kwargs.get('figsize', (10, 7))
    subplot_layout = _create_subplots_layout(kwargs, rows, cols)
    return _generate_axes(rows=rows, cols=cols, figure=figure,
                          figsize=figsize, subplot_layout=subplot_layout)


def _create_subplots_layout(kwargs, rows, cols):
    subplot_layout = {'rows': rows,
                      'cols': cols,
                      'sharedy': kwargs.get('sharey', False),
                      'sharedx': kwargs.get('sharex', False)}
    return subplot_layout


def _create_subplot_figurehandle(rows, cols, make_subplots_kwargs):
    subplot_figure = make_subplots(
        rows, cols, subplot_titles=tuple([' '] * (rows * cols)),
        **make_subplots_kwargs)
    figure = figureHandle(layout=subplot_figure.layout)
    figure._grid_ref = subplot_figure._grid_ref
    return figure


def _generate_axes(rows=None, cols=None, figure=None, figsize=None, subplot_layout=None):
    if rows * cols == 1:
        axes = Matly(figure=figure,
                     row=1,
                     col=1,
                     figsize=figsize,
                     subplot_layout=subplot_layout)

    elif rows == 1:
        axes = []
        for c in range(1, cols + 1):
            axes.append(Matly(figure=figure,
                              row=1,
                              col=c,
                              figsize=figsize,
                              subplot_layout=subplot_layout))
    elif cols == 1:
        axes = []
        for r in range(1, rows + 1):
            axes.append(Matly(figure=figure,
                              row=r,
                              col=1,
                              figsize=figsize,
                              subplot_layout=subplot_layout))
    else:
        axes = [[]]
        for r in range(1, rows + 1):
            if r > 1:
                axes.append([])
            for c in range(1, cols + 1):
                axes[r - 1] += [Matly(figure=figure,
                                      row=r,
                                      col=c,
                                      figsize=figsize,
                                      subplot_layout=subplot_layout)]
    return figure, np.array(axes)