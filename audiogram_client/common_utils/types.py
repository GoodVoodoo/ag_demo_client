from enum import Enum, auto

from audiogram_client.common_utils.option_types import Pb2Enum
from audiogram_client.genproto import stt_pb2, tts_pb2

_VAEventsMode = stt_pb2.RecognitionConfig.VoiceActivityMarkEventsMode
_VADMode = stt_pb2.VADOptions.VoiceActivityDetectionMode
_VoiceStyle = tts_pb2.VoiceStyle


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


class ASAttackType(Enum):
    logical = auto()
    physical = auto()
    all_types = auto()


class TTSVoiceStyle(Pb2Enum):
    pb2_value: _VoiceStyle.ValueType
    neutral = ("neutral", _VoiceStyle.VOICE_STYLE_NEUTRAL)
    happy = ("happy", _VoiceStyle.VOICE_STYLE_HAPPY)
    angry = ("angry", _VoiceStyle.VOICE_STYLE_ANGRY)
    sad = ("sad", _VoiceStyle.VOICE_STYLE_SAD)
    surprised = ("surprised", _VoiceStyle.VOICE_STYLE_SURPRISED)
