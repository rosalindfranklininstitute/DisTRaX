class NotEnoughMemoryError(Exception):
    """Error for when more memory is requested than is available."""

    def __init__(self, message: str):
        """Call the base class constructor with the parameters it needs.

        Args:
            message: Message to display
        """
        super().__init__(message)


class DeviceCreationError(Exception):
    """When the creation of the Block device fails."""

    def __init__(self, message: str):
        """Call the base class constructor with the parameters it needs.

        Args:
            message: Message to display
        """
        super().__init__(message)


class ClusterExistsError(Exception):
    """When a Cluster Already Exists."""

    def __init__(self, message: str):
        """Call the base class constructor with the parameters it needs.

        Args:
            message: Message to display
        """
        super().__init__(message)


class DaemonNotStartedError(Exception):
    """When a Daemon Fails to Start."""

    def __init__(self, message: str):
        """Call the base class constructor with the parameters it needs.

        Args:
            message: Message to display
        """
        super().__init__(message)
