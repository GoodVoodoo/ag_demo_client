from typing import Final

from clients.genproto import tts_pb2

# --- Static Configuration ---
AUDIO_ENCODING: Final = tts_pb2.AudioEncoding.LINEAR_PCM
POSTPROCESSING_MODE: Final = tts_pb2.SynthesizeOptions.PostprocessingMode.POST_PROCESSING_DISABLE
LANGUAGE_CODE: Final = "ru"
AUDIO_SAVE_CHANNELS: Final = 1
AUDIO_SAVE_SAMPLE_WIDTH: Final = 2  # In bytes
