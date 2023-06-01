import distrax.gateways as gateways
from distrax.gateways.abstract_gateway import AbstractGateway


class TestGateway:
    """
    Testing that the Gateways created are subclasses and
    instances of the AbstractGateway
    """

    def test_is_subclass_of_abstract_gateway(self):
        for gateway in gateways.AVAILABLE:
            gateways.use_gateway(gateway)
            manager = gateways.get_gateway(gateway)
            assert issubclass(manager.GATEWAY, AbstractGateway)

    def test_instance_of_abstract_gateway(self):
        for gateway in gateways.AVAILABLE:
            gateways.use_gateway(gateway)
            manager = gateways.get_gateway(gateway)
            assert isinstance(manager.GATEWAY(), AbstractGateway)
