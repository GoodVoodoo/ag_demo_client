import csv
import os
from datetime import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from typing import List
import sys
import click
from google.protobuf.duration_pb2 import Duration

from audiogram_client.genproto import stt_pb2
from tabulate import tabulate


@dataclass
class TranscriptionEntry:
    start_time_ms: int
    end_time_ms: int
    transcript: str
    channel: int | None
    is_final: bool

    def __str__(self) -> str:
        channel_info = f"Channel {self.channel}: " if self.channel is not None else ""
        return f"{channel_info}{self.transcript}"


# Global list to store all transcriptions
all_transcriptions: List[TranscriptionEntry] = []

# Global counter for result numbering
result_counter = 0


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
    text_file_output: bool = False,
    text_file_path: str | None = None,
    channel: int | None = None,
) -> None:
    transcript = None
    if hypothesis.normalized_transcript:  # Just check if the field has a value
        transcript = hypothesis.normalized_transcript
    elif hypothesis.transcript:  # Just check if the field has a value
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

        # Add to global transcriptions list if it's a final result
        if text_file_output:  # Changed condition to collect all transcriptions
            click.echo(f"\tAdding transcription to list: Channel {channel}, Text: {transcript}")
            entry = TranscriptionEntry(
                start_time_ms=hypothesis.start_time_ms,
                end_time_ms=hypothesis.end_time_ms,
                transcript=transcript,
                channel=channel,
                is_final=is_final
            )
            all_transcriptions.append(entry)

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


def print_recognize_response(response, is_file_response=False, text_file_output=False, audio_file=None):
    global result_counter
    
    # If text file output is enabled, prepare the output file path
    text_file_path = None
    current_channel = None
    if response.channel:
        current_channel = response.channel
        
    if text_file_output and audio_file:
        try:
            # Get the base name of the audio file without extension
            base_name = os.path.splitext(audio_file)[0]
            text_file_path = f"{base_name}.txt"
            
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(text_file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Clear the file and reset counter only on the first response
            if hasattr(response, 'header') and response.header:
                if os.path.exists(text_file_path):
                    os.remove(text_file_path)
                result_counter = 0  # Reset counter at start
        except Exception as e:
            click.echo(f"\nError handling text file: {str(e)}")
            text_file_path = None

    # Print header information if available
    if hasattr(response, 'header') and response.header:
        click.echo("Response header:")
        click.echo(f"  Request ID: {response.header.request_id}")
        click.echo(f"  Status: {response.header.status}")
        if response.header.error_message:
            click.echo(f"  Error message: {response.header.error_message}")
        click.echo("")
    
    if current_channel:
        click.echo(f"\tChannel: {current_channel}")

    if response.HasField("speaker_info") and response.speaker_info.speaker_id:
        click.echo(f"\tSpeaker ID: {response.speaker_info.speaker_id}")

    if response.HasField("hypothesis"):
        is_final = response.is_final
        transcript = None
        if response.hypothesis.normalized_transcript:
            transcript = response.hypothesis.normalized_transcript
        elif response.hypothesis.transcript:
            transcript = response.hypothesis.transcript

        # Define time_info for display
        time_info = f"({response.hypothesis.start_time_ms/1000:05.2f}s-{response.hypothesis.end_time_ms/1000:05.2f}s)"
        
        if transcript and text_file_output and text_file_path:
            try:
                result_counter += 1  # Increment counter for each result
                with open(text_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"Result {result_counter}:\n")
                    f.write(f"        Channel: {current_channel}\n")
                    f.write(f'        Hypothesis {time_info}: "{transcript}" is_final: {is_final}\n\n')
            except Exception as e:
                click.echo(f"\nError writing to file: {str(e)}")

        msg = f'\tHypothesis{time_info}: "{transcript}" is_final: {is_final}'
        if is_final:
            msg += f", confidence: {response.hypothesis.confidence:.4g}"
        click.echo(msg)

        words = response.hypothesis.normalized_words or response.hypothesis.words
        for word in words:
            click.echo(
                f"\t\t{word.start_time_ms / 1000:05.2f}s - "
                f'{word.end_time_ms / 1000:05.2f}s: "{word.word}" '
                f"confidence: {word.confidence:.4g}"
            )

    if response.va_marks:
        print_va_marks(response.va_marks)

    if response.HasField("genderage"):
        print_genderage_result(response.genderage)

    if response.spoofing_result:
        print_spoofing_results(response.spoofing_result)

    # Write sorted transcriptions to file only on the last response of the sequence
    if text_file_output and text_file_path and is_file_response and not response.HasField("hypothesis"):
        try:
            click.echo(f"\nPreparing to write {len(all_transcriptions)} transcriptions to file")
            # Sort all transcriptions by start time, using end time as secondary sort for 0-start entries
            sorted_transcriptions = sorted(all_transcriptions, key=lambda x: (x.start_time_ms if x.start_time_ms > 0 else x.end_time_ms))
            
            # Write to file
            with open(text_file_path, 'w', encoding='utf-8') as f:
                # Write results in the expected format
                for idx, entry in enumerate(sorted_transcriptions, 1):
                    if entry.transcript.strip():  # Only write non-empty transcripts
                        click.echo(f"\nWriting Result {idx} to file")
                        f.write(f"Result {idx}:\n")
                        f.write(f"        Channel: {entry.channel}\n")
                        time_info = f"({entry.start_time_ms/1000:05.2f}s-{entry.end_time_ms/1000:05.2f}s)"
                        f.write(f'        Hypothesis {time_info}: "{entry.transcript}" is_final: {entry.is_final}\n\n')
                
            click.echo(f"\nFinished writing to {text_file_path}")
            # Clear the list after writing the final results
            all_transcriptions = []
        except Exception as e:
            click.echo(f"\nError writing sorted transcriptions to file: {str(e)}")
