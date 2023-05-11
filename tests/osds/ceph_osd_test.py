from distrax.osds.abstract_osd import AbstractOSD
from distrax.osds.ceph_osd import CephOSD


class TestCephOSD:

    """
    Testing CephOSD
    """

    def test_is_subclass_of_abstract_osd(self):
        assert issubclass(CephOSD, AbstractOSD)

    def test_instance_of_abstract_osd(self):
        assert isinstance(CephOSD(), AbstractOSD)
