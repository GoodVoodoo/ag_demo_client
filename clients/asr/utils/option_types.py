import enum

from clients.common_utils.option_types import Pb2Enum, StrEnum
from clients.genproto import stt_pb2

_VAEventsMode = stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode
_VADMode = stt_pb2.VADOptions.VoiceActivityDetectionMode


@enum.unique
class VAResponseMode(Pb2Enum):
    pb2_value: _VAEventsMode.ValueType
    disable = ("disable", _VAEventsMode.VA_DISABLE)
    enable = ("enable", _VAEventsMode.VA_ENABLE)
    enable_async = ("enable-async", _VAEventsMode.VA_ENABLE_ASYNC)


@enum.unique
class VADAlgo(StrEnum):
    vad = "vad"
    dep = "dep"
    disabled = "disable"


@enum.unique
class VADMode(Pb2Enum):
    pb2_value: _VADMode.ValueType
    default = ("default", _VADMode.VAD_MODE_DEFAULT)
    only_speech = ("only-speech", _VADMode.ONLY_SPEECH)
    split_by_pauses = ("split-by-pauses", _VADMode.SPLIT_BY_PAUSES)


@enum.unique
class ASAttackType(Pb2Enum):
    pb2_value: stt_pb2.AttackType.ValueType
    logical = ("logical", stt_pb2.AttackType.LOGICAL)
    physical = ("physical", stt_pb2.AttackType.PHYSICAL)
    all_types = ("all-types", stt_pb2.AttackType.ALL_TYPES)
