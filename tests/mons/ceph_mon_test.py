from distrax.mons.abstract_mon import AbstractMON
from distrax.mons.ceph_mon import CephMON


class TestCephMON:
    """
    Testing that the Mons created are subclasses and instances of the AbstractMON
    """

    def test_is_subclass_of_abstract_mon(self):
        assert issubclass(CephMON, AbstractMON)

    def test_instance_of_abstract_mon(self):
        assert issubclass(CephMON, AbstractMON)
