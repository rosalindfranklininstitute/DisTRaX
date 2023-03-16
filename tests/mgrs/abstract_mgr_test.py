from distrax.mgrs.abstract_mgr import AbstractMGR

import pytest


class NotSubclassAbstractMGR:
    def __init__(self):
        pass


class CanNotCreateAbstractMGR(AbstractMGR):
    """
    Test AbstractMGR without implemented functions
    """

    def __init__(self):
        pass


class CanCreateAbstractMGR(AbstractMGR):
    """
    Test AbstractMGR with implemented functions
    """

    def __init__(self):
        pass

    def create_mgr(self, interface: str, folder: str) -> bool:
        return True

    def remove_mgr(self, folder: str) -> bool:
        return True


class TestAbstractMGR:

    """
    Testing AbstractMGR
    """

    def test_instantiate_interface(self):
        """
        Testing that the abstract class can not be instantiated
        """
        with pytest.raises(TypeError) as excinfo:
            AbstractMGR()
        assert "Can't instantiate" in str(excinfo)

    def test_methods_not_implemented(self):
        """
        Testing that the create_mgr and remove_mgr abstract method has to be implemented
        """
        with pytest.raises(TypeError) as excinfo:
            CanNotCreateAbstractMGR()
        assert "Can't instantiate abstract class" in str(excinfo)

    def test_create_mgr_is_implemented(self):
        """
        Testing that the create_mgr abstract method has been implemented
        """
        tests = CanCreateAbstractMGR()
        assert tests.create_mgr("eth0", "") is True

    def test_remove_mgr_is_implemented(self):
        """
        Testing that the remove_mgr abstract method has been implemented
        """
        tests = CanCreateAbstractMGR()
        assert tests.remove_mgr("eth0") is True

    def test_can_create_abstract_mgr_is_a_subclass(self):
        """
        Check that the that CanCreateAbstractMGR is a subclass of AbstractMGR
        """
        assert (AbstractMGR.__subclasshook__(CanCreateAbstractMGR)) is True

    def test_not_subclass_abstract_mgr(self):
        """
        Check that the that NotSubclassAbstractMGR is not a subclass of AbstractMGR
        """
        assert (AbstractMGR.__subclasshook__(NotSubclassAbstractMGR)) is NotImplemented
