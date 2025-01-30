import time
from collections.abc import Iterable, Iterator
from itertools import islice

from clients.genproto import stt_pb2

from .definitions import AUDIO_ENCODING, LANGUAGE_CODE
from .option_types import ASAttackType, VADAlgo, VADMode, VAResponseMode

StreamRequestIterator = Iterator[stt_pb2.RecognizeRequest]


def make_va_config(
    vad_algo: VADAlgo,
    vad_mode: VADMode,
    vad_threshold: float,
    vad_min_silence_ms: int,
    vad_speech_pad_ms: int,
    vad_min_speech_ms: int,
    dep_smoothed_window_threshold: float,
    dep_smoothed_window_ms: int,
) -> stt_pb2.VoiceActivityConfig:
    vad_usage = stt_pb2.VoiceActivityConfig.VoiceActivityDetectionAlgorithmUsage
    match vad_algo:
        case VADAlgo.vad:
            vad_options = stt_pb2.VADOptions(
                threshold=vad_threshold,
                speech_pad_ms=vad_speech_pad_ms,
                min_silence_ms=vad_min_silence_ms,
                min_speech_ms=vad_min_speech_ms,
                mode=vad_mode.pb2_value,
            )
            return stt_pb2.VoiceActivityConfig(
                usage=vad_usage.USE_VAD,
                vad_options=vad_options,
            )
        case VADAlgo.dep:
            dep_options = stt_pb2.DEPOptions(
                smoothed_window_threshold=dep_smoothed_window_threshold,
                smoothed_window_ms=dep_smoothed_window_ms,
            )
            return stt_pb2.VoiceActivityConfig(
                usage=vad_usage.USE_DEP,
                dep_options=dep_options,
            )

    return stt_pb2.VoiceActivityConfig(
        usage=vad_usage.DO_NOT_PERFORM_VOICE_ACTIVITY,
    )


def make_antispoofing_config(
    enable: bool,
    attack_type: ASAttackType | None,
    false_acceptance_rate: float | None,
    false_rejection_rate: float | None,
    max_duration_for_analysis_ms: int | None,
) -> stt_pb2.AntiSpoofingConfig:
    kwargs = {
        "enable": enable,
        "FAR": false_acceptance_rate,
        "FRR": false_rejection_rate,
        "max_duration_for_analysis_ms": max_duration_for_analysis_ms,
    }
    if attack_type:
        kwargs["type"] = attack_type.pb2_value

    return stt_pb2.AntiSpoofingConfig(**kwargs)  # type: ignore


def make_speaker_labeling_config(
    enable: bool,
    max_speakers: int | None,
    num_speakers: int | None,
) -> stt_pb2.SpeakerLabelingConfig:
    kwargs = {
        "enable": enable,
        "max_speakers": max_speakers,
        "num_speakers": num_speakers,
    }

    return stt_pb2.SpeakerLabelingConfig(**kwargs)  # type: ignore


def make_context_dictionary_config(
    dictionary_name: str,
    weight: float,
) -> stt_pb2.ContextDictionaryConfig:
    return stt_pb2.ContextDictionaryConfig(
        dictionary_name=dictionary_name,
        weight=weight,
    )


def make_recognition_config(
    model: str,
    va_config: stt_pb2.VoiceActivityConfig,
    va_response_mode: VAResponseMode,
    sample_rate: int,
    channel_count: int,
    enable_genderage: bool,
    enable_word_time_offsets: bool,
    enable_punctuator: bool,
    enable_denormalization: bool,
    as_config: stt_pb2.AntiSpoofingConfig,
    sl_config: stt_pb2.SpeakerLabelingConfig,
    wfst_config: stt_pb2.ContextDictionaryConfig,
    split_by_channel: bool = False,
) -> stt_pb2.RecognitionConfig:
    ga_config = stt_pb2.GenderAgeEmotionConfig(enable=enable_genderage)
    punct_config = stt_pb2.PunctuationConfig(enable=enable_punctuator)
    denorm_config = stt_pb2.DenormalizationConfig(enable=enable_denormalization)
    result = stt_pb2.RecognitionConfig(
        encoding=AUDIO_ENCODING,
        language_code=LANGUAGE_CODE,
        model=model,
        sample_rate_hertz=sample_rate,
        audio_channel_count=channel_count,
        split_by_channel=split_by_channel,
        enable_word_time_offsets=enable_word_time_offsets,
        va_config=va_config,
        va_response_mode=va_response_mode.pb2_value,
        genderage_config=ga_config,
        punctuation_config=punct_config,
        denormalization_config=denorm_config,
        antispoofing_config=as_config,
        speaker_labeling_config=sl_config,
        context_dictionary=wfst_config,
    )

    return result


def stream_request_iterator(
    recognition_config: stt_pb2.StreamRecognitionConfig,
    audio_chunks: Iterable[bytes],
    wait_ms: int,
) -> StreamRequestIterator:
    yield stt_pb2.RecognizeRequest(config=recognition_config)

    for chunk in islice(audio_chunks, 1):
        yield stt_pb2.RecognizeRequest(audio=chunk)

    for chunk in audio_chunks:
        time.sleep(wait_ms / 1000)
        yield stt_pb2.RecognizeRequest(audio=chunk)
