import click
import pydantic
import requests
import os

from audiogram_client.genproto import stt_pb2
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.audio_archive.utils.response import process_response
from audiogram_client.audio_archive.utils.models import GetTranscriptResponse, GetVadResponse


def try_request(url: str) -> requests.Response:
    try:
        return requests.get(url)
    except requests.ConnectionError as e:
        click.echo(f"Connection error: {e}")
        context = click.get_current_context()
        context.exit(-1)


def fetch_trace_and_session_id(
    api_address: str,
    client_id: str,
    request_id: str,
) -> tuple[str | None, str | None]:
    url = "https://" + api_address + f"/clients/{client_id}/requests"

    resp = try_request(url)

    if resp.status_code != 200:
        click.echo("Unable to fetch session and trace ids for this request")
        return None, None

    resp_json = resp.json()

    try:
        req_list = RequestsList(**resp_json)
    except pydantic.ValidationError as e:
        click.echo(f"Unable to find session and trace ids for this request: {e.errors()}")
        return None, None

    for item in req_list.data:
        if item.request_id != request_id:
            continue

        return item.trace_id, item.session_id

    return None, None


def get_and_save_data(host, port, request_id, audio_id, data_type, file_name, file_dir):
    url = f"http://{host}:{port}/requests/{request_id}/audio/{audio_id}/{data_type}"
    
    if data_type == "audio":
        response = requests.get(url, stream=True)
        response.raise_for_status()
        if not file_name:
            file_name = f"{audio_id}.wav"
        
        file_path = os.path.join(file_dir, file_name)
        
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Audio saved to {file_path}")

    else:
        response = requests.get(url)
        if data_type == "transcript":
            data = process_response(response, GetTranscriptResponse)
            if not file_name:
                file_name = f"{audio_id}_transcript.txt"
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "w") as f:
                for item in data.transcript:
                    f.write(f"{item.start_time}-{item.end_time}: {item.transcript} (confidence: {item.confidence})\n")
            print(f"Transcript saved to {file_path}")

        elif data_type == "vad":
            data = process_response(response, GetVadResponse)
            if not file_name:
                file_name = f"{audio_id}_vad.txt"
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "w") as f:
                for item in data.vad:
                    f.write(f"{item.start_time}-{item.end_time}\n")
            print(f"VAD marks saved to {file_path}")
