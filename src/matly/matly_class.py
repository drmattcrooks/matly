import plotly.graph_objects as go
import tempfile
from pdf2image import convert_from_path, convert_from_bytes
import os
from matly import rcParams
from matly.style import use
from matly.rc_params import INCLUDED_STYLESHEETS, INCLUDED_STYLESHEET_FOLDER,\
    convert_stylesheet_to_dict


DEFAULT_STYLESHEET = 'matly'
PATH_TO_DEFAULT_RCPARAMS = f"{INCLUDED_STYLESHEET_FOLDER}/{DEFAULT_STYLESHEET}.mplstyle"
MATLY_RCPARAMS_DEFAULTS = convert_stylesheet_to_dict(
    path=PATH_TO_DEFAULT_RCPARAMS)


LINE_STYLE_DICT = {
    '--': 'dash',
    '-': None
}

class Matly:
    def __init__(self, *args, **kwargs):
        try:
            self.fig = kwargs['figure']
        except:
            raise KeyError("No figure handle passed when initiating Matly class")

        self.rcParams_layout = {
            'xaxis': {
                'tickfont': dict(),
                'title': {'font': dict()},
                'showgrid': None,
                'gridcolor': None,
                'zeroline': False,
                'linecolor': None,
                'linewidth': None,
                'mirror': None,
                'ticks': None,
                'ticklen': None,
                'tickwidth': None,
                'color': None,
                'tickfont': {'family': None, 'size': None},
                'side': None
            },
            'yaxis': {
                'tickfont': dict(),
                'title': {'font': dict()},
                'showgrid': None,
                'gridcolor': None,
                'zeroline': False,
                'linecolor': None,
                'linewidth': None,
                'mirror': None,
                'ticks': None,
                'ticklen': None,
                'tickwidth': None,
                'color': None,
                'tickfont': {'family': None, 'size': None},
                'side': None
            },
            'title': {'font': {'size': None, 'color': None}},
            'plot_bgcolor': None,
            'paper_bgcolor': None
        }

        self.rcparams_spines = {
            'bottom': None,
            'left': None,
            'right': None,
            'top': None
        }

        self.rcparams_lines = {
            'width': None,
            'dash': None,
            'color': None
        }

        self.rcparams_markers = {
            'line': {
                'color': None,
                'width': None
            },
            'symbol': None,
            'color': None,
            'size': None
        }

        self.rcparams_patch = {
            'linewidth': None,
            'facecolor': None,
            'edgecolor': None
        }

        self.rcparams_font = {
            'family': None,
            'weight': None,
            'size': None
        }

        self.rcparams_figsize = {
            'figsize': None
        }

        self.rcparams_legend = {
            'edgecolor': None,
            'facecolor': None,
            'fontsize': None,
            'frameon': None,
            'loc': None,
            'title_fontsize': None
        }

        # set layout from rcparams
        self._set_rcparams_layout()
        self.fig.layout = self.rcParams_layout

    def plot(self, *args):
        kwargs = {
            'x': None,
            'y': None
        }
        if len(args) == 1:
            kwargs['y'] = args[0]
            kwargs['x'] = list(range(len(args[0])))
        elif len(args) == 2:
            kwargs['x'] = args[0]
            kwargs['y'] = args[1]
        self._plot(**kwargs)

    def _plot(self, **kwargs):
        plot_trace = self._get_plot_defaults()
        plot_trace.update(
            x=kwargs['x'],
            y=kwargs['y']
        )
        self.fig.add_trace(plot_trace)

    def _get_plot_defaults(self):
        self._set_rcparams_lines()
        return go.Scatter(line=self.rcparams_lines, mode='lines')

    def _set_rcparams_layout_axis_color_and_width(self):
        self.rcParams_layout['xaxis']['linecolor'] = _get_rcparam_value('axes.edgecolor')
        self.rcParams_layout['xaxis']['linewidth'] = _get_rcparam_value('axes.linewidth')
        self.rcParams_layout['yaxis']['linecolor'] = _get_rcparam_value('axes.edgecolor')
        self.rcParams_layout['yaxis']['linewidth'] = _get_rcparam_value('axes.linewidth')

    def _set_rcparams_layout_background_color(self):
        self.rcParams_layout['plot_bgcolor'] = _get_rcparam_value('axes.facecolor')
        self.rcParams_layout['paper_bgcolor'] = _get_rcparam_value('axes.facecolor')

    def _set_rcparams_layout_axis_label_fonts(self):
        self.rcParams_layout['title']['font']['size'] = _get_rcparam_value('axes.labelsize')
        self.rcParams_layout['xaxis']['title']['font']['size'] = _get_rcparam_value('axes.labelsize')
        self.rcParams_layout['xaxis']['title']['font']['color'] = _get_rcparam_value('axes.labelcolor')
        self.rcParams_layout['yaxis']['title']['font']['size'] = _get_rcparam_value('axes.labelsize')
        self.rcParams_layout['yaxis']['title']['font']['color'] = _get_rcparam_value('axes.labelcolor')

    def _set_rcparams_layout_grid(self):
        if not _get_rcparam_value('axes.grid'):
            self.rcParams_layout['xaxis']['showgrid'] = False
            self.rcParams_layout['yaxis']['showgrid'] = False
        else:
            grid_type = _get_rcparam_value('axes.grid.axis')
            if grid_type == 'x':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = False
                self.rcParams_layout['xaxis']['gridcolor'] = _get_rcparam_value('grid.color')
                self.rcParams_layout['xaxis']['gridwidth'] = _get_rcparam_value('grid.linewidth')
            elif grid_type == 'y':
                self.rcParams_layout['xaxis']['showgrid'] = False
                self.rcParams_layout['yaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['gridcolor'] = _get_rcparam_value('grid.color')
                self.rcParams_layout['yaxis']['gridwidth'] = _get_rcparam_value('grid.linewidth')
            elif grid_type == 'both':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = True
                self.rcParams_layout['xaxis']['gridcolor'] = _get_rcparam_value('grid.color')
                self.rcParams_layout['xaxis']['gridwidth'] = _get_rcparam_value('grid.linewidth')
                self.rcParams_layout['yaxis']['gridcolor'] = _get_rcparam_value('grid.color')
                self.rcParams_layout['yaxis']['gridwidth'] = _get_rcparam_value('grid.linewidth')

    def _set_rcparams_layout_xticks(self):
        xtick_top = _get_rcparam_value('xtick.top')
        xtick_bottom = _get_rcparam_value('xtick.bottom')
        if xtick_bottom & (not xtick_top):
            self.rcParams_layout['xaxis']['side'] = 'bottom'
        elif xtick_top & (not xtick_bottom):
            self.rcParams_layout['xaxis']['side'] = 'top'
        elif xtick_bottom & xtick_top:
            self.rcParams_layout['xaxis']['side'] = 'bottom'
            self.rcParams_layout['xaxis']['mirror'] = 'allticks'

    def _set_rcparams_layout_yticks(self):
        ytick_left = _get_rcparam_value('ytick.left')
        ytick_right = _get_rcparam_value('ytick.right')
        if ytick_right & (not ytick_left):
            self.rcParams_layout['yaxis']['side'] = 'right'
        elif ytick_left & (not ytick_right):
            self.rcParams_layout['yaxis']['side'] = 'left'
        elif ytick_right & ytick_left:
            self.rcParams_layout['yaxis']['side'] = 'left'
            self.rcParams_layout['yaxis']['mirror'] = 'allticks'

    def _set_rcparams_layout_ticks_inside_out(self):
        if _get_rcparam_value('xtick.direction') == 'in':
            self.rcParams_layout['xaxis']['ticks'] = 'inside'
        elif _get_rcparam_value('xtick.direction') == 'out':
            self.rcParams_layout['xaxis']['ticks'] = 'outside'

        if _get_rcparam_value('ytick.direction') == 'in':
            self.rcParams_layout['yaxis']['ticks'] = 'inside'
        elif _get_rcparam_value('ytick.direction') == 'out':
            self.rcParams_layout['yaxis']['ticks'] = 'outside'

    def _set_rcparams_layout_tick_size(self):
        self.rcParams_layout['xaxis']['ticklen'] = _get_rcparam_value('xtick.major.size')
        self.rcParams_layout['yaxis']['ticklen'] = _get_rcparam_value('ytick.major.size')
        self.rcParams_layout['xaxis']['tickwidth'] = _get_rcparam_value('xtick.major.width')
        self.rcParams_layout['yaxis']['tickwidth'] = _get_rcparam_value('ytick.major.width')

    def _set_rcparams_layout_tick_color(self):
        self.rcParams_layout['xaxis']['color'] = _get_rcparam_value('xtick.color')
        self.rcParams_layout['yaxis']['color'] = _get_rcparam_value('ytick.color')

    def _set_rcparams_layout(self):
        # Set values of layout parameters
        self._set_rcparams_layout_axis_color_and_width()

        # Set background color
        self._set_rcparams_layout_background_color()

        # Axis label fonts
        self._set_rcparams_layout_axis_label_fonts()

        # Grids
        self._set_rcparams_layout_grid()

        # -----------
        # -- Ticks --
        # -----------

        # Turn on / off xticks
        self._set_rcparams_layout_xticks()

        # Turn on / off yticks
        self._set_rcparams_layout_yticks()

        # Set ticks inside or outside axes
        self._set_rcparams_layout_ticks_inside_out()

        # Set ticks size
        self._set_rcparams_layout_tick_size()

        # Set ticks color
        self._set_rcparams_layout_tick_color()

    def _set_rcparams_spines(self):
        self.rcParams_spines = {
            label: SpineClass(
                label,
                _get_rcparam_value(f"axes.spines.{label}"),
                _get_rcparam_value('axes.edgecolor'),
            )
            for label in ['top', 'left', 'bottom', 'right']
        }

    def _set_rcparams_lines(self):
        self.rcparams_lines['width'] = _get_rcparam_value('lines.linewidth')
        self.rcparams_lines['dash'] = LINE_STYLE_DICT[
            _get_rcparam_value('lines.linestyle')]
        self.rcparams_lines['color'] = _get_rcparam_value('lines.color')

    def _set_rcparams_markers(self):
        self.rcparams_markers['symbol'] = _get_rcparam_value('lines.marker')
        self.rcparams_markers['color'] = _get_rcparam_value('lines.markerfacecolor')
        self.rcparams_markers['size'] = _get_rcparam_value('lines.markersize')
        self.rcparams_markers['line']['color'] = _get_rcparam_value('lines.markeredgecolor')
        self.rcparams_markers['line']['width'] = _get_rcparam_value('lines.markeredgewidth')

    def _set_rcparams_patch(self):
        self.rcparams_patch['linewidth'] = _get_rcparam_value('patch.linewidth')
        self.rcparams_patch['facecolor'] = _get_rcparam_value('patch.facecolor')
        self.rcparams_patch['edgecolor'] = _get_rcparam_value('patch.edgecolor')

    def _set_rcparams_font(self):
        self.rcparams_font['family'] = _get_rcparam_value('font.family')
        self.rcparams_font['weight'] = _get_rcparam_value('font.weight')
        self.rcparams_font['size'] = _get_rcparam_value('font.size')

    def _set_rcparams_figsize(self):
        self.rcparams_figsize['figsize'] = _get_rcparam_value('figure.figsize')

    def _set_rcparams_legend(self):
        self.rcparams_legend['edgecolor'] = _get_rcparam_value('legend.edgecolor')
        self.rcparams_legend['facecolor'] = _get_rcparam_value('legend.facecolor')
        self.rcparams_legend['fontsize'] = _get_rcparam_value('legend.fontsize')
        self.rcparams_legend['frameon'] = _get_rcparam_value('legend.frameon')
        self.rcparams_legend['loc'] = _get_rcparam_value('legend.loc')
        self.rcparams_legend['title_fontsize'] = _get_rcparam_value('legend.title_fontsize')


class figureHandle(go.Figure):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', ())
        layout = kwargs.get('layout', None)
        super().__init__(data=data, layout=layout)

    def savefig(self, filename):
        if filename[-4:] in ['.pdf', '.jpg', '.png']:
            self.write_image(filename)
        else:
            raise ValueError(f"Unrecognised file format in filename: {filename}")


class SpineClass:
    def __init__(self, label, visible, color):
        self.spine = {
            'visible': visible,
            'color': color
        }
        self.label = label


def _get_rcparam_value(parameter):
    return rcParams.get(
        parameter,
        MATLY_RCPARAMS_DEFAULTS[parameter]
    )
