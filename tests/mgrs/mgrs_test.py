import distrax.mgrs as mgrs
from distrax.mgrs.abstract_mgr import AbstractMGR


class TestMGRs:
    """
    Testing that the MGRs created are subclasses and instances of the AbstractMGR
    """

    def test_is_subclass_of_abstract_mgr(self):
        for mgr in mgrs.AVAILABLE:
            mgrs.set_mgr(mgr)
            manager = mgrs.get_mgr(mgr)
            assert issubclass(manager.MGR, AbstractMGR)

    def test_instance_of_abstract_mgr(self):
        for mgr in mgrs.AVAILABLE:
            mgrs.set_mgr(mgr)
            manager = mgrs.get_mgr(mgr)
            assert isinstance(manager.MGR(), AbstractMGR)
