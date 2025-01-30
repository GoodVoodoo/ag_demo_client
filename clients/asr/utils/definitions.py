from typing import Final

from clients.genproto import stt_pb2

# --- Config Defaults ---
# DEP is only stream, no need to split defaults
DEFAULT_DEP_SMOOTHED_WINDOW_THRESHOLD: Final = 0.754
DEFAULT_DEP_SMOOTHED_WINDOW_MS: Final = 970

# VAD defaults for file recognition
DEFAULT_VAD_F_THRESHOLD: Final = 0.1
DEFAULT_VAD_F_MIN_SILENCE_MS: Final = 500
DEFAULT_VAD_F_SPEECH_PAD_MS: Final = 300
DEFAULT_VAD_F_MIN_SPEECH_MS: Final = 250

# VAD defaults for stream recognition
DEFAULT_VAD_S_THRESHOLD: Final = 0.9
DEFAULT_VAD_S_MIN_SILENCE_MS: Final = 1000
DEFAULT_VAD_S_SPEECH_PAD_MS: Final = 0  # ignored in stream
DEFAULT_VAD_S_MIN_SPEECH_MS: Final = 0  # ignored in stream

# --- Static Configuration ---
AUDIO_ENCODING: Final = stt_pb2.AudioEncoding.LINEAR_PCM
LANGUAGE_CODE: Final = "ru"
MAX_ALTERNATIVES: Final = 1
CHUNK_LEN_MS: Final = 1000
