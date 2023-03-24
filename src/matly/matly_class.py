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

        self.rcparams_lines = {
            'width': None,
            'dash': None,
            'color': None
        }


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
        plot_style_dict = {'line': dict(),
                           'marker': {'line': dict()},
                           'marker_symbol': None,
                           'mode': 'lines'}
        plot_trace.update(
            x = kwargs['x'],
            y = kwargs['y'],
            **plot_style_dict
        )
        self.fig.add_trace(plot_trace)

    def _get_plot_defaults(self):
        return go.Scatter()

    def _set_rcparams_layout(self):
        # Set values of layout parameters
        self.rcParams_layout['xaxis']['linecolor'] = rcParams.get(
            'axes.edgecolor', MATLY_RCPARAMS_DEFAULTS['axes.edgecolor'])
        self.rcParams_layout['xaxis']['linewidth'] = float(rcParams.get(
            'axes.linewidth', MATLY_RCPARAMS_DEFAULTS['axes.linewidth']))
        self.rcParams_layout['yaxis']['linecolor'] = rcParams.get(
            'axes.edgecolor', MATLY_RCPARAMS_DEFAULTS['axes.edgecolor'])
        self.rcParams_layout['yaxis']['linewidth'] = float(rcParams.get(
            'axes.linewidth', MATLY_RCPARAMS_DEFAULTS['axes.linewidth']))

        # Set background color
        self.rcParams_layout['plot_bgcolor'] = rcParams.get(
            'axes.facecolor', MATLY_RCPARAMS_DEFAULTS['axes.facecolor'])
        self.rcParams_layout['paper_bgcolor'] = rcParams.get(
            'axes.facecolor', MATLY_RCPARAMS_DEFAULTS['axes.facecolor'])

        # Axis label fonts
        self.rcParams_layout['title']['font']['size'] = rcParams.get(
            'axes.labelsize', MATLY_RCPARAMS_DEFAULTS['axes.labelsize'])
        self.rcParams_layout['xaxis']['title']['font']['size'] = rcParams.get(
            'axes.labelsize', MATLY_RCPARAMS_DEFAULTS['axes.labelsize'])
        self.rcParams_layout['xaxis']['title']['font']['color'] = rcParams.get(
            'axes.labelcolor', MATLY_RCPARAMS_DEFAULTS['axes.labelcolor'])
        self.rcParams_layout['yaxis']['title']['font']['size'] = rcParams.get(
            'axes.labelsize', MATLY_RCPARAMS_DEFAULTS['axes.labelsize'])
        self.rcParams_layout['yaxis']['title']['font']['color'] = rcParams.get(
            'axes.labelcolor', MATLY_RCPARAMS_DEFAULTS['axes.labelcolor'])

        # Grids
        if not rcParams.get('axes.grid', MATLY_RCPARAMS_DEFAULTS['axes.grid']):
            self.rcParams_layout['xaxis']['showgrid'] = False
            self.rcParams_layout['yaxis']['showgrid'] = False
        else:
            grid_type = rcParams.get('axes.grid.axis', MATLY_RCPARAMS_DEFAULTS['axes.grid.axis'])
            if grid_type == 'x':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = False
            elif grid_type == 'y':
                self.rcParams_layout['xaxis']['showgrid'] = False
                self.rcParams_layout['yaxis']['showgrid'] = True
            elif grid_type == 'both':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = True

        # -----------
        # -- Ticks --
        # -----------

        # Turn on / off xticks
        xtick_top = rcParams.get('xtick.top', MATLY_RCPARAMS_DEFAULTS['xtick.top'])
        xtick_bottom = rcParams.get('xtick.bottom', MATLY_RCPARAMS_DEFAULTS['xtick.bottom'])
        if xtick_bottom & (not xtick_top):
            self.rcParams_layout['xaxis']['side'] = 'bottom'
        elif xtick_top & (not xtick_bottom):
            self.rcParams_layout['xaxis']['side'] = 'top'
        elif xtick_bottom & xtick_top:
            self.rcParams_layout['xaxis']['side'] = 'bottom'
            self.rcParams_layout['xaxis']['mirror'] = 'allticks'

        # Turn on / off yticks
        ytick_left = rcParams.get('ytick.left', MATLY_RCPARAMS_DEFAULTS['ytick.left'])
        ytick_right = rcParams.get('ytick.right', MATLY_RCPARAMS_DEFAULTS['ytick.right'])
        if ytick_right & (not ytick_left):
            self.rcParams_layout['yaxis']['side'] = 'right'
        elif ytick_left & (not ytick_right):
            self.rcParams_layout['yaxis']['side'] = 'left'
        elif ytick_right & ytick_left:
            self.rcParams_layout['yaxis']['side'] = 'right'
            self.rcParams_layout['yaxis']['mirror'] = 'allticks'

        # Set ticks inside or outside axes
        if rcParams.get('xtick.direction', MATLY_RCPARAMS_DEFAULTS['xtick.direction']) == 'in':
            self.rcParams_layout['xaxis']['ticks'] = 'inside'
        elif rcParams.get('xtick.direction', MATLY_RCPARAMS_DEFAULTS['xtick.direction']) == 'out':
            self.rcParams_layout['xaxis']['ticks'] = 'outside'
        if rcParams.get('ytick.direction', MATLY_RCPARAMS_DEFAULTS['ytick.direction']) == 'in':
            self.rcParams_layout['yaxis']['ticks'] = 'inside'
        elif rcParams.get('ytick.direction', MATLY_RCPARAMS_DEFAULTS['ytick.direction']) == 'out':
            self.rcParams_layout['yaxis']['ticks'] = 'outside'

        # Set ticks size
        self.rcParams_layout['xaxis']['ticklen'] = rcParams.get(
            'xtick.major.size', MATLY_RCPARAMS_DEFAULTS['xtick.major.size'])
        self.rcParams_layout['yaxis']['ticklen'] = rcParams.get(
            'ytick.major.size', MATLY_RCPARAMS_DEFAULTS['ytick.major.size'])
        self.rcParams_layout['xaxis']['tickwidth'] = rcParams.get(
            'xtick.major.width', MATLY_RCPARAMS_DEFAULTS['xtick.major.width'])
        self.rcParams_layout['yaxis']['tickwidth'] = rcParams.get(
            'ytick.major.width', MATLY_RCPARAMS_DEFAULTS['ytick.major.width'])

        # Set ticks color
        self.rcParams_layout['xaxis']['color'] = rcParams.get(
            'xtick.color', MATLY_RCPARAMS_DEFAULTS['xtick.color'])
        self.rcParams_layout['yaxis']['color'] = rcParams.get(
            'ytick.color', MATLY_RCPARAMS_DEFAULTS['ytick.color'])

    def _set_rcparams_spines(self):
        self.rcParams_spines = {
            label: SpineClass(
                label,
                rcParams.get(
                    f"axes.spines.{label}",
                    MATLY_RCPARAMS_DEFAULTS[f"axes.spines.{label}"]
                ),
                rcParams.get(
                    'axes.edgecolor',
                    MATLY_RCPARAMS_DEFAULTS['axes.edgecolor']
                ),
            )
            for label in ['top', 'left', 'bottom', 'right']
        }

    def _set_rcparams_lines(self):
        self.rcparams_lines['width'] = _get_rcparam_value('lines.linewidth')
        self.rcparams_lines['dash'] = _get_rcparam_value('lines.linestyle')
        self.rcparams_lines['color'] = _get_rcparam_value('lines.color')


class figureHandle(go.Figure):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', ())
        layout = kwargs.get('layout', None)
        super().__init__(data=data, layout=layout)

    def savefig(self, filename):
        if filename[-4:] in ['.pdf', '.jpg']:
            self.write_image(filename)
        elif filename[-4:] == '.png':
            self.save_png(filename)
        else:
            raise ValueError(f"Unrecognised file format in filename: {filename}")

    def save_png(self, filename):
        with tempfile.TemporaryDirectory() as path:
            self.write_image(f"{filename[:-4]}.pdf")
            image = convert_from_bytes(open(f"{filename[:-4]}.pdf", 'rb').read())[0]
            image.save(filename)
        os.remove(f"{filename[:-4]}.pdf")


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
