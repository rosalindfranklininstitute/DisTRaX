from distrax.mgrs.abstract_mgr import AbstractMGR
from distrax.mgrs.ceph_mgr import CephMGR


class TestCephMGR:
    """
    Testing that the MGRs created are subclasses and instances of the AbstractMGR
    """

    def test_is_subclass_of_abstract_mgr(self):
        assert issubclass(CephMGR, AbstractMGR)

    def test_instance_of_abstract_mgr(self):
        assert issubclass(CephMGR, AbstractMGR)
