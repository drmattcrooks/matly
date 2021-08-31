import plotly.graph_objects as go
import tempfile
from pdf2image import convert_from_path, convert_from_bytes
import os


class mattsplotlib:
    def __init__(self):
        pass

class figureHandle(go.Figure):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', ())
        layout = kwargs.get('layout', None)
        go.Figure.__init__(self, data=data, layout=layout)

    def savefig(self, filename):
        if filename[-4:] in ['.pdf', '.jpg']:
            self.write_image(filename)
        elif filename[-4:] == '.png':
            with tempfile.TemporaryDirectory() as path:
                self.write_image(f"{filename[:-4]}.pdf")
                #     images_from_path = convert_from_path('figures/bubble_plot_example.pdf', output_folder=path)
                image = convert_from_bytes(open(f"{filename[:-4]}.pdf", 'rb').read())
                image[0].save(filename)
            os.remove(f"{filename[:-4]}.pdf")
        else:
            raise ValueError(f"Unrecognised file format in filename: {filename}")