from typing import Protocol, runtime_checkable


@runtime_checkable
class AbstractGateway(Protocol):
    """An interface for Gateway Classes.

    A Gateway is the cluster gateway daemon, this is often used to use to support S3
    buckets and similar

    This is designed such plugins of the Gateway can be made easily.
    The only methods publicly visible to the user should be create_gateway and
    remove_gateway
    """

    def create_gateway(self) -> None:
        """Create the gateway node."""
        ...

    def create_s3_user(self) -> None:
        """Create s3 user."""
        ...

    def remove_gateway(self) -> None:
        """Remove the gateway node."""
        ...
