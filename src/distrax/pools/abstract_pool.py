from typing import Protocol, runtime_checkable


@runtime_checkable
class AbstractPool(Protocol):
    """An interface for Pool Classes.

    A Pool is a partition within the cluster used to store objects.
    """

    @staticmethod
    def create_pool(name: str = "distrax", percentage: float = 1.0) -> None:
        """Create the Pool to store objects.

        Args:
            name: The name of the pool
            percentage: The percentage of the cluster to allocate to the pool
            value expected between 0 and 1.
        """
        ...

    @staticmethod
    def remove_pools() -> None:
        """Remove and purge pool."""
        ...
