from uuid import UUID


class BackwardUUIDException(Exception):
    def __init__(self, last_uuid: UUID, backward_uuid: UUID, *args) -> None:
        super().__init__(*args)
        self.last_uuid = last_uuid
        self.backwarded_uuid = backward_uuid
