import enum

from clients.common_utils.option_types import Pb2Enum
from clients.genproto import tts_pb2

_VoiceStyle = tts_pb2.VoiceStyle


@enum.unique
class TTSVoiceStyle(Pb2Enum):
    pb2_value: _VoiceStyle.ValueType
    neutral = ("neutral", _VoiceStyle.VOICE_STYLE_NEUTRAL)
    happy = ("happy", _VoiceStyle.VOICE_STYLE_HAPPY)
    angry = ("angry", _VoiceStyle.VOICE_STYLE_ANGRY)
    sad = ("sad", _VoiceStyle.VOICE_STYLE_SAD)
    surprised = ("surprised", _VoiceStyle.VOICE_STYLE_SURPRISED)
