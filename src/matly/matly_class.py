import plotly.graph_objects as go
import tempfile
from pdf2image import convert_from_path, convert_from_bytes
import os


class Matly:
    def __init__(self, *args, **kwargs):
        try:
            self.fig = kwargs['figure']
        except:
            raise KeyError("No figure handle passed when initiating Matly class")


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