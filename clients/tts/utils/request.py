from typing import cast

from clients.genproto import tts_pb2

from .definitions import AUDIO_ENCODING, LANGUAGE_CODE, POSTPROCESSING_MODE
from .option_types import TTSVoiceStyle


def make_tts_request(
    text: str,
    is_ssml: bool,
    voice_name: str,
    rate: int,
    model_type: str | None,
    model_rate: int | None,
    voice_style: TTSVoiceStyle,
) -> tts_pb2.SynthesizeSpeechRequest:
    text_kwarg = {}
    if is_ssml:
        text_kwarg["ssml"] = text
    else:
        text_kwarg["text"] = text

    return tts_pb2.SynthesizeSpeechRequest(
        **text_kwarg,
        sample_rate_hertz=rate,
        voice_name=voice_name,
        encoding=AUDIO_ENCODING,
        language_code=LANGUAGE_CODE,
        synthesize_options=tts_pb2.SynthesizeOptions(
            model_type=cast(str, model_type),
            model_sample_rate_hertz=cast(int, model_rate),
            voice_style=voice_style.pb2_value,
            postprocessing_mode=POSTPROCESSING_MODE,
        ),
    )
