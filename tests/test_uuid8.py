import newuuid
from newuuid import UUID


class TestUUID8:
    def test_uuid8(self):
        uuid = newuuid.uuid8(0x320C3D4DCC00, 0x75B, 0xEC932D5F69181C0)
        assert uuid.version == 8
        assert uuid.variant == newuuid.RFC_4122
        assert uuid == UUID("320C3D4D-CC00-875B-8EC9-32D5F69181C0")
