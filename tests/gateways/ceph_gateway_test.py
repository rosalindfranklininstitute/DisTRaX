from distrax.gateways.abstract_gateway import AbstractGateway
from distrax.gateways.ceph_gateway import CephGateway


class TestCephGateway:

    """
    Testing CephGateway
    """

    def test_is_subclass_of_abstract_gateway(self):
        assert issubclass(CephGateway, AbstractGateway)

    def test_instance_of_abstract_gateway(self):
        assert isinstance(CephGateway(), AbstractGateway)
