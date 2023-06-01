from distrax.mdss.abstract_mds import AbstractMDS
from distrax.mdss.ceph_mds import CephMDS


class TestCephMDS:
    """
    Testing that the MDS created are subclasses and instances of the AbstractMDS
    """

    def test_is_subclass_of_abstract_mds(self):
        assert issubclass(CephMDS, AbstractMDS)

    def test_instance_of_abstract_mds(self):
        assert issubclass(CephMDS, AbstractMDS)
