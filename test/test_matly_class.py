from unittest.mock import patch, mock_open, Mock
from pdf2image import convert_from_bytes

from matly.matly_class import Matly, figureHandle
import matly.matly_class
from fixtures.mock_functions import mock_image

TEST_FIGURE_PATH = "test/fixtures/test_figure.pdf"
MOCKED_OPEN_FILE = open(TEST_FIGURE_PATH, 'rb')
MOCKED_TEMP_SAVED_PDF = open(TEST_FIGURE_PATH, 'rb').read()
MOCKED_CONVERTED = convert_from_bytes(open(TEST_FIGURE_PATH, 'rb').read())

def test_matly_is_class():
    assert Matly().__class__.__name__ == 'Matly'


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

