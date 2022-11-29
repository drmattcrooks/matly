import plotly.graph_objects as go
import tempfile
from pdf2image import convert_from_path, convert_from_bytes
import os


class Matly:
    def __init__(self, *args, **kwargs):
        pass

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