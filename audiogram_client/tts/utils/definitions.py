from typing import Final

from audiogram_client.genproto import tts_pb2

# --- Static Configuration ---
AUDIO_ENCODING: Final = tts_pb2.AudioEncoding.LINEAR_PCM
POSTPROCESSING_MODE: Final = tts_pb2.SynthesizeOptions.PostprocessingMode.POST_PROCESSING_DISABLE
LANGUAGE_CODE: Final = "ru"
AUDIO_SAVE_SAMPLE_WIDTH: int = 2  # bytes, 16 bit
AUDIO_SAVE_CHANNELS: int = 1  # mono
