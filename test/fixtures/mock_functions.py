from unittest.mock import Mock


def mock_image():
    mock_trans = Mock()
    trans_methods = {
        'save': Mock()
    }
    mock_trans.configure_mock(**trans_methods)
    return mock_trans


def mock_os_environ():
    mock_trans = Mock()
    trans_methods = {
        'environ': {}
    }
    mock_trans.configure_mock(**trans_methods)
    return mock_trans