from typing import Final

from audiogram_client.genproto import tts_pb2

# --- Static Configuration ---
AUDIO_ENCODING: Final = tts_pb2.AudioEncoding.LINEAR_PCM
AUDIO_SAVE_SAMPLE_WIDTH: Final = 2  # 16 bit / 8 = 2 bytes
AUDIO_SAVE_CHANNELS: int = 1  # mono

TEXT_ENCODING: Final = "utf-8"

POSTPROCESSING_MODE: Final = tts_pb2.PostprocessingMode.POST_PROCESSING_DISABLE

DEFAULT_VOICE: Final = "borisova"
DEFAULT_SAMPLE_RATE: Final = 48000

LANGUAGE_CODE: Final = "ru"
