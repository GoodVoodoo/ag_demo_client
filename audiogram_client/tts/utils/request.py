from typing import cast

from audiogram_client.common_utils.types import TTSVoiceStyle
from audiogram_client.genproto import tts_pb2

from .definitions import AUDIO_ENCODING, LANGUAGE_CODE, POSTPROCESSING_MODE


def make_tts_request(
    text: str,
    is_ssml: bool,
    voice_name: str,
    rate: int,
    model_type: str | None,
    model_rate: int | None,
    voice_style: TTSVoiceStyle,
    language_code: str | None = None,
    custom_options: dict[str, float | int | str | bool] | None = None,
) -> tts_pb2.SynthesizeSpeechRequest:
    text_kwarg = {}
    if is_ssml:
        text_kwarg["ssml"] = text
    else:
        text_kwarg["text"] = text

    synthesize_options = tts_pb2.SynthesizeOptions(
        model_type=cast(str, model_type),
        model_sample_rate_hertz=cast(int, model_rate),
        voice_style=voice_style.pb2_value,
        postprocessing_mode=POSTPROCESSING_MODE,
    )
    
    # Add custom options if provided
    if custom_options:
        for key, value in custom_options.items():
            option_value = tts_pb2.SynthesizeOptions.CustomSynthesizeOptionValue()
            if isinstance(value, bool):
                option_value.bool_value = value
            elif isinstance(value, int):
                option_value.int32_value = value
            elif isinstance(value, float):
                option_value.number_value = value
            elif isinstance(value, str):
                option_value.string_value = value
            synthesize_options.custom_options[key].CopyFrom(option_value)
    
    return tts_pb2.SynthesizeSpeechRequest(
        **text_kwarg,
        sample_rate_hertz=rate,
        voice_name=voice_name,
        encoding=AUDIO_ENCODING,
        language_code=LANGUAGE_CODE,
        synthesize_options=synthesize_options,
    )
