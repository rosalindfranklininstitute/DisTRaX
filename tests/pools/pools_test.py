import distrax.pools as pools
from distrax.pools.abstract_pool import AbstractPool


class TestPools:
    """
    Testing that the Pools created are subclasses and instances of the AbstractPool
    """

    def test_is_subclass_of_abstract_pool(self):
        for pool in pools.AVAILABLE:
            pools.set_pool(pool)
            set_pool = pools.get_pool(pool)
            assert issubclass(set_pool.POOL, AbstractPool)

    def test_instance_of_abstract_pool(self):
        for pool in pools.AVAILABLE:
            pools.set_pool(pool)
            set_pool = pools.get_pool(pool)
            assert isinstance(set_pool.POOL(), AbstractPool)
