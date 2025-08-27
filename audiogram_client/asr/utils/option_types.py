from enum import Enum


class VADAlgo(Enum):
    VAD = "vad"
    DEP = "dep"
    ENHANCED_VAD = "enhanced_vad"
    TARGET_SPEECH_VAD = "target_speech_vad"
    NO_VAD = "no_vad"


class VAResponseMode(Enum):
    DISABLE = "disable"
    ENABLE = "enable"
    ENABLE_ASYNC = "enable_async"


class VADMode(Enum):
    DEFAULT = "default"
    SPLIT_BY_PAUSES = "split_by_pauses"
    ONLY_SPEECH = "only_speech"


class ASAttackType(Enum):
    FAR = "far"
    FRR = "frr"

