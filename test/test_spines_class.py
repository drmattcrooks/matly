from matly.matly_class import SpineClass


def test_spine_class_attributes_defaults():
    spine_class = SpineClass('label', False, 'grey')
    assert 'spine' in dir(spine_class)
    assert 'label' in dir(spine_class)
    assert spine_class.spine == {'visible': False, 'color': 'grey'}
    assert spine_class.label == 'label'
