from distrax.mons.abstract_mon import AbstractMON

import pytest


class NotSubclassAbstractMON:
    def __init__(self):
        pass


class CanNotCreateAbstractMON(AbstractMON):
    """
    Test AbstractMON without implemented functions
    """

    def __init__(self):
        pass


class CanCreateAbstractMON(AbstractMON):
    """
    Test AbstractMON with implemented functions
    """

    def __init__(self):
        pass

    def create_mon(self, interface: str, folder: str) -> bool:
        return True

    def remove_mon(self, folder: str) -> bool:
        return True


class TestAbstractMON:

    """
    Testing AbstractMON
    """

    def test_instantiate_interface(self):
        """
        Testing that the abstract class can not be instantiated
        """
        with pytest.raises(TypeError) as excinfo:
            AbstractMON()
        assert "Can't instantiate" in str(excinfo)

    def test_methods_not_implemented(self):
        """
        Testing that the create_mon and remove_mon abstract method has to be implemented
        """
        with pytest.raises(TypeError) as excinfo:
            CanNotCreateAbstractMON()
        assert "Can't instantiate abstract class" in str(excinfo)

    def test_create_mon_is_implemented(self):
        """
        Testing that the create_mon abstract method has been implemented
        """
        tests = CanCreateAbstractMON()
        assert tests.create_mon("eth0", "") is True

    def test_remove_mon_is_implemented(self):
        """
        Testing that the remove_mon abstract method has been implemented
        """
        tests = CanCreateAbstractMON()
        assert tests.remove_mon("eth0") is True

    def test_can_create_abstract_mon_is_a_subclass(self):
        """
        Check that the that CanCreateAbstractMON is a subclass of AbstractMON
        """
        assert (AbstractMON.__subclasshook__(CanCreateAbstractMON)) is True

    def test_not_subclass_abstract_mon(self):
        """
        Check that the that NotSubclassAbstractMON is not a subclass of AbstractMON
        """
        assert (AbstractMON.__subclasshook__(NotSubclassAbstractMON)) is NotImplemented
