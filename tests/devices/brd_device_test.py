import distrax.devices as devices
from distrax.devices.abstract_device import AbstractDevice


class TestDevices:
    """
    Testing that the Devices created are subclasses and instances
    of the AbstractDevice
    """

    def test_is_subclass_of_abstract_device(self):
        for device in devices.AVAILABLE:
            devices.set_device(device)
            dev = devices.get_device(device)
            assert issubclass(dev.DEVICE, AbstractDevice)

    def test_instance_of_abstract_device(self):
        for device in devices.AVAILABLE:
            devices.set_device(device)
            dev = devices.get_device(device)
            assert isinstance(dev.DEVICE(), AbstractDevice)
