from distrax.devices.abstract_device import AbstractDevice

import pytest


class NotSubclassAbstractDevice:
    def __init__(self):
        pass


class CanNotCreateAbstractDevice(AbstractDevice):
    """
    Test AbstractDevice without implemented functions
    """

    def __init__(self):
        pass


class CanCreateAbstractDevice(AbstractDevice):
    """
    Test AbstractDevice with implemented functions
    """

    def __init__(self):
        pass

    def create_device(self, size: str, number: str) -> bool:
        return True

    def remove_device(self) -> bool:
        return True


class TestAbstractDevice:

    """
    Testing AbstractDevice
    """

    def test_instantiate_interface(self):
        """
        Testing that the abstract class can not be instantiated
        """
        with pytest.raises(TypeError) as excinfo:
            AbstractDevice()
        assert "Can't instantiate" in str(excinfo)

    def test_methods_not_implemented(self):
        """
        Testing that the create_device and remove_device abstract method
        has to be implemented
        """
        with pytest.raises(TypeError) as excinfo:
            CanNotCreateAbstractDevice()
        assert "Can't instantiate abstract class" in str(excinfo)

    def test_create_device_is_implemented(self):
        """
        Testing that the create_device abstract method has been implemented
        """
        tests = CanCreateAbstractDevice()
        assert tests.create_device("4G", 1) is True

    def test_remove_device_is_implemented(self):
        """
        Testing that the remove_device abstract method has been implemented
        """
        tests = CanCreateAbstractDevice()
        assert tests.remove_device() is True

    def test_can_create_abstract_device_is_a_subclass(self):
        """
        Check that the that CanCreateAbstractDevice is a subclass of AbstractDevice
        """
        assert (AbstractDevice.__subclasshook__(CanCreateAbstractDevice)) is True

    def test_not_subclass_abstract_device(self):
        """
        Check that the that NotSubclassAbstractDevice
        is not a subclass of AbstractDevice
        """
        assert (
            AbstractDevice.__subclasshook__(NotSubclassAbstractDevice)
        ) is NotImplemented
