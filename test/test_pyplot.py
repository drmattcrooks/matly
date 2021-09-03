from unittest.mock import Mock
from unittest.mock import patch

import mattsplotlib.pyplot as mplt


@patch.object(mplt, 'figureHandle', return_value = Mock)
def test_figure_returns_handle(figure_handle_mock):
    assert mplt.figure() == figure_handle_mock()