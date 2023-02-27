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
                'mirror': None
            },
            'yaxis': {
                'tickfont': dict(),
                'title': {'font': dict()},
                'showgrid': None,
                'zeroline': False,
                'linecolor': None,
                'linewidth': None,
                'mirror': None
            },
            'title': {'font': {'size': None, 'color': None}},
            'plot_bgcolor': None,
            'paper_bgcolor': None
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