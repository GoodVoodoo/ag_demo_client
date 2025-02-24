from collections.abc import Iterable

import click
from google.protobuf.duration_pb2 import Duration

from clients.genproto import stt_pb2


def _duration_to_str(d: Duration) -> str:
    secs = d.ToMilliseconds() / 1000
    return f"{secs:05.2f}"


def print_va_marks(va_marks: Iterable[stt_pb2.VoiceActivityMark]) -> None:
    click.echo("\tVoice Activity Marks:")
    for mark_idx, mark in enumerate(va_marks, 1):
        mark_type_str = stt_pb2.VoiceActivityMark.VoiceActivityMarkType.Name(mark.mark_type)
        click.echo(
            f"\t\tmark #{mark_idx}: " f"mark_type: {mark_type_str}, " f"offset_ms: {mark.offset_ms}"
        )


def print_genderage_result(genderage: stt_pb2.SpeakerGenderAgePrediction) -> None:
    click.echo("\tGenderage result:")
    gender_name = stt_pb2.SpeakerGenderAgePrediction.GenderClass.Name(genderage.gender)
    click.echo(f"\t\tgender: {gender_name}")
    age_name = stt_pb2.SpeakerGenderAgePrediction.AgeClass.Name(genderage.age)
    click.echo(f"\t\tage: {age_name}")
    emotions = genderage.emotion
    click.echo(
        f"\t\temotion:\n"
        f"\t\t\tpositive={emotions.positive:.3f}\n"
        f"\t\t\tneutral={emotions.neutral:.3f}\n"
        f"\t\t\tnegative_angry={emotions.negative_angry:.3f}\n"
        f"\t\t\tnegative_sad={emotions.negative_sad:.3f}"
    )


def print_hypothesis(
    hypothesis: stt_pb2.SpeechRecognitionHypothesis,
    is_final: bool = True,
) -> None:
    transcript = None
    if hypothesis.normalized_transcript:
        transcript = hypothesis.normalized_transcript
    elif hypothesis.transcript:
        transcript = hypothesis.transcript

    if transcript:
        start_end_time = ""
        if hypothesis.start_time_ms or hypothesis.end_time_ms:
            start_end_time = (
                f" ({hypothesis.start_time_ms / 1000:05.2f}s-"
                f"{hypothesis.end_time_ms / 1000:05.2f}s)"
            )

        msg = f'\tHypothesis{start_end_time}: "{transcript}" is_final: {is_final}'

        if is_final:
            msg += f", confidence: {hypothesis.confidence:.4g}"

        click.echo(msg)

    words = hypothesis.normalized_words or hypothesis.words

    for word in words:
        click.echo(
            f"\t\t{word.start_time_ms / 1000:05.2f}s - "
            f'{word.end_time_ms / 1000:05.2f}s: "{word.word}" '
            f"confidence: {word.confidence:.4g}"
        )


def print_spoofing_results(results: Iterable[stt_pb2.SpoofingResult]) -> None:
    click.echo("\tSpoofing results:")
    for result in results:
        result_result = stt_pb2.SpoofingResult.AttackResult.Name(result.result)
        click.echo(
            f"\t\tResult: {result_result}\n"
            f"\t\tConfidence: {result.confidence:.4g}\n"
            f"\t\tInterval: {result.start_time_ms / 1000}s - {result.end_time_ms / 1000}s"
        )


def print_recognize_response(response, is_file_response=False):
    # Print header information if available
    if hasattr(response, 'header') and response.header:
        click.echo("Response header:")
        click.echo(f"  Request ID: {response.header.request_id}")
        click.echo(f"  Status: {response.header.status}")
        if response.header.error_message:
            click.echo(f"  Error message: {response.header.error_message}")
        click.echo("")
    
    if response.channel:
        click.echo(f"\tChannel: {response.channel}")

    if response.HasField("speaker_info") and response.speaker_info.speaker_id:
        click.echo(f"\tSpeaker ID: {response.speaker_info.speaker_id}")

    if response.HasField("hypothesis"):
        is_final = response.is_final
        print_hypothesis(response.hypothesis, is_final)

    if response.va_marks:
        print_va_marks(response.va_marks)

    if response.HasField("genderage"):
        print_genderage_result(response.genderage)

    if response.spoofing_result:
        print_spoofing_results(response.spoofing_result)
