from distrax.osds.abstract_osd import AbstractOSD

import pytest


class NotSubclassAbstractOSD:
    def __init__(self):
        pass


class CanNotCreateAbstractOSD(AbstractOSD):
    """
    Test AbstractOSD without implemented functions
    """

    def __init__(self):
        pass


class CanCreateAbstractOSD(AbstractOSD):
    """
    Test AbstractOSD with implemented functions
    """

    def __init__(self):
        pass

    def create_osds(self, size: str, number: str) -> bool:
        return True

    def remove_osds(self) -> bool:
        return True


class TestAbstractOSD:

    """
    Testing AbstractOSD
    """

    def test_instantiate_interface(self):
        """
        Testing that the abstract class can not be instantiated
        """
        with pytest.raises(TypeError) as excinfo:
            AbstractOSD()
        assert "Can't instantiate" in str(excinfo)

    def test_methods_not_implemented(self):
        """
        Testing that the create_osds and remove_osds abstract method
        has to be implemented
        """
        with pytest.raises(TypeError) as excinfo:
            CanNotCreateAbstractOSD()
        assert "Can't instantiate abstract class" in str(excinfo)

    def test_create_osds_is_implemented(self):
        """
        Testing that the create_osds abstract method has been implemented
        """
        tests = CanCreateAbstractOSD()
        assert tests.create_osds("4G", 1) is True

    def test_remove_osds_is_implemented(self):
        """
        Testing that the remove_osds abstract method has been implemented
        """
        tests = CanCreateAbstractOSD()
        assert tests.remove_osds() is True

    def test_can_create_abstract_osd_is_a_subclass(self):
        """
        Check that the that CanCreateAbstractOSD is a subclass of AbstractOSD
        """
        assert (AbstractOSD.__subclasshook__(CanCreateAbstractOSD)) is True

    def test_not_subclass_abstract_osd(self):
        """
        Check that the that NotSubclassAbstractOSD
        is not a subclass of AbstractOSD
        """
        assert (AbstractOSD.__subclasshook__(NotSubclassAbstractOSD)) is NotImplemented
