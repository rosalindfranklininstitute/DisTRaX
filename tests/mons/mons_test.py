import distrax.mons as mons
from distrax.mons.abstract_mon import AbstractMON


class TestMONs:
    """
    Testing that the Mons created are subclasses and instances of the AbstractMON
    """

    def test_is_subclass_of_abstract_mon(self):
        for mon in mons.AVAILABLE:
            mons.use_mon(mon)
            monitor = mons.get_mon(mon)
            assert issubclass(monitor.MON, AbstractMON)

    def test_instance_of_abstract_mon(self):
        for mon in mons.AVAILABLE:
            mons.use_mon(mon)
            monitor = mons.get_mon(mon)
            assert isinstance(monitor.MON(), AbstractMON)
