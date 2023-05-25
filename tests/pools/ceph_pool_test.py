from distrax.pools.abstract_pool import AbstractPool
from distrax.pools.ceph_pool import CephPool


class TestCephPool:

    """
    Testing CephOSD
    """

    def test_is_subclass_of_abstract_osd(self):
        assert issubclass(CephPool, AbstractPool)

    def test_instance_of_abstract_osd(self):
        assert isinstance(CephPool(), AbstractPool)
