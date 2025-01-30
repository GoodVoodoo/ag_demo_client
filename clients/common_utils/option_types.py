from enum import Enum
from typing import Any, cast


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return cast(str, self.value)


class Pb2Enum(StrEnum):
    pb2_value: Any

    def __new__(cls, value: str, pb2_value: Any) -> Any:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.pb2_value = pb2_value
        return obj
