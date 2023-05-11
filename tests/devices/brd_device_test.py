from distrax.devices.abstract_device import AbstractDevice
from distrax.devices.brd_device import BRDDevice


class TestCephDEVICE:

    """
    Testing CephDEVICE
    """

    def test_is_subclass_of_abstract_device(self):
        assert issubclass(BRDDevice, AbstractDevice)

    def test_instance_of_abstract_device(self):
        assert isinstance(BRDDevice(), AbstractDevice)
