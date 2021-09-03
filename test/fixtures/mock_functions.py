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


def _get_list_of_methods_and_values(*args):
    if len(args) == 1:
        list_of_methods = args[0]
        list_of_values = [{}] * len(list_of_methods)
    elif len(args) == 2:
        list_of_methods = args[0]
        list_of_values = args[1]
    return list_of_methods, list_of_values


def mock_class(*args):
    list_of_methods, list_of_values = _get_list_of_methods_and_values(*args)

    mock_trans = Mock()
    trans_methods = {method: value for method, value in zip(list_of_methods, list_of_values)}
    mock_trans.configure_mock(**trans_methods)
    return mock_trans