from uuid import UUID


class BackwardUUIDException(Exception):
    """Exception raised when backward UUID is generated."""

    def __init__(self, last_uuid: UUID, backward_uuid: UUID, *args) -> None:
        """Create a new BackwardUUIDException.

        Args:
            last_uuid (UUID): Last generated UUID.
            backward_uuid (UUID): Backward UUID.
        """
        super().__init__(*args)
        self.last_uuid = last_uuid
        self.backwarded_uuid = backward_uuid
