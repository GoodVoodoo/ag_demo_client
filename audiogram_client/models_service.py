from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

import click
import grpc
from tabulate import tabulate

from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import stt_pb2, stt_pb2_grpc, tts_pb2, tts_pb2_grpc


class ModelServiceType(Enum):
    ASR = auto()
    TTS = auto()


@dataclass
class ModelInfo:
    service: ModelServiceType
    name: str
    language: str
    sample_rate: int
    type: str
    details: dict = field(default_factory=dict)


class ModelService:
    def __init__(self, settings: SettingsProtocol):
        self._settings = settings
        self._auth_metadata = get_auth_metadata(
            settings.sso_url,
            settings.realm,
            settings.client_id,
            settings.client_secret,
            settings.iam_account,
            settings.iam_workspace,
            settings.verify_sso,
        )

    def get_models(self) -> List[ModelInfo]:
        with open_grpc_channel(
            self._settings.api_address,
            ssl_creds_from_settings(self._settings),
        ) as channel:
            asr_stub = stt_pb2_grpc.STTStub(channel)
            tts_stub = tts_pb2_grpc.TTSStub(channel)

            asr_models = self._get_asr_models(asr_stub)
            tts_models = self._get_tts_models(tts_stub)

        return asr_models + tts_models

    def _get_asr_models(self, stub: stt_pb2_grpc.STTStub) -> List[ModelInfo]:
        request = stt_pb2.GetModelsInfoRequest()
        try:
            response: stt_pb2.ModelsInfo = stub.GetModelsInfo(
                request,
                metadata=self._auth_metadata,
                timeout=self._settings.timeout,
            )
            return [
                ModelInfo(
                    service=ModelServiceType.ASR,
                    name=model.name,
                    language=model.language_code,
                    sample_rate=model.sample_rate_hertz,
                    type="ASR",
                    details={"dictionaries": list(model.dictionary_name)},
                )
                for model in response.models
            ]
        except grpc.RpcError as e:
            click.echo(f"Error fetching ASR models: {e.details()}", err=True)
            return []

    def _get_tts_models(self, stub: tts_pb2_grpc.TTSStub) -> List[ModelInfo]:
        request = tts_pb2.GetModelsInfoRequest()
        try:
            response: tts_pb2.ModelsInfo = stub.GetModelsInfo(
                request,
                metadata=self._auth_metadata,
                timeout=self._settings.timeout,
            )
            return [
                ModelInfo(
                    service=ModelServiceType.TTS,
                    name=model.name,
                    language=model.language_code or "ru",
                    sample_rate=model.sample_rate_hertz,
                    type=model.type,
                )
                for model in response.models
            ]
        except grpc.RpcError as e:
            click.echo(f"Error fetching TTS models: {e.details()}", err=True)
            return []


@click.command(help="Get a comprehensive list of all available ASR and TTS models.")
@errors_handler
@common_options_in_settings
def models_info(settings: SettingsProtocol):
    service = ModelService(settings)
    models = service.get_models()

    if not models:
        click.echo("No models found.")
        return

    table = [
        {
            "Service": model.service.name,
            "Name": model.name,
            "Language": model.language,
            "Sample Rate (Hz)": model.sample_rate,
            "Type": model.type,
        }
        for model in sorted(models, key=lambda m: (m.service.name, m.name))
    ]

    click.echo("Available Models:")
    click.echo(tabulate(table, headers="keys", tablefmt="grid"))
