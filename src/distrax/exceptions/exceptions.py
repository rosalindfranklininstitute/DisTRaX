class NotEnoughMemoryError(Exception):
    """
    Error for when more memory is requested than is available

    """

    def __init__(self, message: str):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DeviceCreationError(Exception):
    """
    When the creation of the Block device fails

    """

    def __init__(self, message: str):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
