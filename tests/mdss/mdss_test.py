import distrax.mdss as mdss
from distrax.mdss.abstract_mds import AbstractMDS


class TestMDSs:
    """
    Testing that the MDSs created are subclasses and instances of the AbstractMDS
    """

    def test_is_subclass_of_abstract_mds(self):
        for mds in mdss.AVAILABLE:
            mdss.use_mds(mds)
            manager = mdss.get_mds(mds)
            assert issubclass(manager.MDS, AbstractMDS)

    def test_instance_of_abstract_mds(self):
        for mds in mdss.AVAILABLE:
            mdss.use_mds(mds)
            manager = mdss.get_mds(mds)
            assert isinstance(manager.MDS(), AbstractMDS)
