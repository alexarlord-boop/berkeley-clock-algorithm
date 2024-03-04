from enum import Enum, auto


class SlaveCodes(Enum):
    DEAD = b"DEAD"
    ALIVE = b"ALIVE"

    def to_bytes(self):
        return self.value


class MasterCodes(Enum):
    REQ_TIME = b"REQUEST_TIME"
    ADJ_TIME = b"ADJUST_TIME"
    REQ_STATUS = b"REQUEST_STATUS"

    def to_bytes(self):
        return self.value
