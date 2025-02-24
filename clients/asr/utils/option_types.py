from enum import Enum, auto

from clients.common_utils.option_types import Pb2Enum, StrEnum
from clients.genproto import stt_pb2

_VAEventsMode = stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode
_VADMode = stt_pb2.VADOptions.VoiceActivityDetectionMode


class VAResponseMode(Enum):
    disable = auto()
    enable = auto()
    enable_async = auto()

    @property
    def pb2_value(self) -> stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode:
        return {
            VAResponseMode.disable: stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode.VA_DISABLE,
            VAResponseMode.enable: stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode.VA_ENABLE,
            VAResponseMode.enable_async: stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode.VA_ENABLE_ASYNC,
        }[self]


class VADAlgo(Enum):
    none = auto()
    vad = auto()
    dep = auto()
    enhanced_vad = auto()
    target_speech_vad = auto()


class VADMode(Enum):
    default = auto()
    split_by_pauses = auto()
    only_speech = auto()

    @property
    def pb2_value(self) -> stt_pb2.VADOptions.VoiceActivityDetectionMode:
        return {
            VADMode.default: stt_pb2.VADOptions.VoiceActivityDetectionMode.VAD_MODE_DEFAULT,
            VADMode.split_by_pauses: stt_pb2.VADOptions.VoiceActivityDetectionMode.SPLIT_BY_PAUSES,
            VADMode.only_speech: stt_pb2.VADOptions.VoiceActivityDetectionMode.ONLY_SPEECH,
        }[self]


# Note: ASAttackType is no longer used in v3 but we'll keep it for backward compatibility
class ASAttackType(Enum):
    logical = auto()
    physical = auto()
    all_types = auto()
