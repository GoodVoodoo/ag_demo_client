import click
import grpc
import json
from google.protobuf.empty_pb2 import Empty
from tabulate import tabulate
from typing import Dict, Any, List

from clients.common_utils.arguments import common_options_in_settings
from clients.common_utils.auth import get_auth_metadata
from clients.common_utils.config import SettingsProtocol
from clients.common_utils.errors import errors_handler
from clients.common_utils.grpc import open_grpc_channel, print_metadata, ssl_creds_from_settings
from clients.genproto import tts_pb2, tts_pb2_grpc


@click.command(
    help="Get a list of available speech synthesis models and their parameters",
)
@click.option(
    "--output-format",
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format for model information",
)
@click.option(
    "--save-to",
    type=click.Path(),
    help="Save output to file (JSON format only)",
)
@click.option(
    "--filter-language",
    help="Filter models by language code (e.g., 'ru', 'en')",
)
@click.option(
    "--filter-type",
    help="Filter models by type (e.g., 'high_quality', 'eng voice')",
)
@click.option(
    "--filter-sample-rate",
    type=int,
    help="Filter models by sample rate (e.g., 8000, 22050, 44100)",
)
@click.option(
    "--group-by-voice",
    is_flag=True,
    help="Group results by voice name",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show additional technical details about models",
)
@errors_handler
@common_options_in_settings
def get_models_info(
    settings: SettingsProtocol,
    output_format: str,
    save_to: str,
    filter_language: str,
    filter_type: str,
    filter_sample_rate: int,
    group_by_voice: bool,
    verbose: bool,
) -> None:
    """Get detailed information about available TTS models."""
    
    auth_metadata = get_auth_metadata(
        settings.sso_url,
        settings.realm,
        settings.client_id,
        settings.client_secret,
        settings.iam_account,
        settings.iam_workspace,
        settings.verify_sso,
    )

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    try:
        with open_grpc_channel(
            settings.api_address,
            ssl_creds_from_settings(settings),
        ) as channel:
            stub = tts_pb2_grpc.TTSStub(channel)

            response: tts_pb2.ModelsInfo
            call: grpc.Call
            response, call = stub.GetModelsInfo.with_call(
                Empty(),
                metadata=auth_metadata,
                timeout=settings.timeout,
            )

            if verbose:
                click.echo("Response metadata:")
                print_metadata(call.initial_metadata())
                click.echo()

            # Print header information if available
            if hasattr(response, 'header') and response.header:
                if verbose:
                    click.echo("Response header:")
                    click.echo(f"  Request ID: {response.header.request_id}")
                    click.echo(f"  Status: {response.header.status}")
                    if response.header.error_message:
                        click.echo(f"  Error message: {response.header.error_message}")
                    click.echo()

            # Filter models
            models = response.models
            
            if filter_language:
                models = [m for m in models if m.language_code == filter_language]
            
            if filter_type:
                models = [m for m in models if filter_type.lower() in m.type.lower()]
            
            if filter_sample_rate:
                models = [m for m in models if m.sample_rate_hertz == filter_sample_rate]
            
            if not models:
                click.echo("No models found matching the specified filters.")
                return

            # Prepare model data
            model_data = []
            for model in models:
                model_info = {
                    "name": model.name,
                    "sample_rate_hertz": model.sample_rate_hertz,
                    "type": model.type,
                    "language_code": model.language_code or "ru",  # Default to Russian
                }
                model_data.append(model_info)

            # Sort models
            model_data = sorted(
                model_data,
                key=lambda x: (x["name"], x["sample_rate_hertz"], x["type"]),
            )

            # Output results
            if output_format.lower() == "json":
                output_data = {
                    "models": model_data,
                    "total_count": len(model_data),
                    "request_id": response.header.request_id if hasattr(response, 'header') and response.header else None,
                    "filters_applied": {
                        "language": filter_language,
                        "type": filter_type,
                        "sample_rate": filter_sample_rate,
                    },
                }
                
                json_output = json.dumps(output_data, indent=2, ensure_ascii=False)
                
                if save_to:
                    with open(save_to, 'w', encoding='utf-8') as f:
                        f.write(json_output)
                    click.echo(f"Model information saved to: {save_to}")
                else:
                    click.echo(json_output)
            else:
                # Table format
                if group_by_voice:
                    # Group by voice name
                    from collections import defaultdict
                    grouped = defaultdict(list)
                    for model in model_data:
                        grouped[model["name"]].append(model)
                    
                    for voice_name, voice_models in sorted(grouped.items()):
                        click.echo(f"\n🎤 Voice: {voice_name}")
                        click.echo("=" * (len(voice_name) + 10))
                        
                        model_table = []
                        for model in voice_models:
                            row = {
                                "Sample Rate (Hz)": model["sample_rate_hertz"],
                                "Type": model["type"],
                                "Language": model["language_code"],
                            }
                            model_table.append(row)
                        
                        click.echo(tabulate(model_table, headers="keys", tablefmt="simple"))
                else:
                    # Standard table format
                    model_table = []
                    for model in model_data:
                        row = {
                            "Name": model["name"],
                            "Sample Rate (Hz)": model["sample_rate_hertz"],
                            "Type": model["type"],
                            "Language": model["language_code"],
                        }
                        
                        if verbose:
                            # Add additional info for verbose mode
                            if "high_quality" in model["type"]:
                                row["Quality"] = "High"
                            elif "eng voice" in model["type"]:
                                row["Quality"] = "English"
                            else:
                                row["Quality"] = "Standard"
                        
                        model_table.append(row)

                    click.echo(f"Available TTS models ({len(model_table)} found):")
                    click.echo(tabulate(model_table, headers="keys", tablefmt="grid"))
                
                if verbose:
                    click.echo(f"\nSummary:")
                    click.echo(f"  Total models: {len(model_data)}")
                    
                    voices = set(m["name"] for m in model_data)
                    click.echo(f"  Unique voices: {len(voices)} ({', '.join(sorted(voices))})")
                    
                    types = set(m["type"] for m in model_data)
                    click.echo(f"  Model types: {', '.join(sorted(types))}")
                    
                    sample_rates = set(m["sample_rate_hertz"] for m in model_data)
                    click.echo(f"  Sample rates: {', '.join(str(sr) for sr in sorted(sample_rates))} Hz")
                    
                    languages = set(m["language_code"] for m in model_data)
                    click.echo(f"  Languages: {', '.join(sorted(languages))}")

    except grpc.RpcError as e:
        click.echo(f"gRPC Error: {e.code()} - {e.details()}", err=True)
        raise click.ClickException(f"Failed to retrieve model information: {e.details()}")
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        raise click.ClickException(f"Failed to retrieve model information: {str(e)}")
