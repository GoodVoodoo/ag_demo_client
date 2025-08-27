import functools
import wave
from typing import Callable, cast, ParamSpec

import click
import grpc
import keycloak
from dynaconf import ValidationError

P = ParamSpec("P")


def errors_handler(func: Callable[P, int | None]) -> Callable[P, int | None]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int | None:
        context = click.get_current_context()

        try:
            return func(*args, **kwargs)

        except ValidationError as err:
            context.fail(err.message)  # This will hint user to use --help

        except KeyboardInterrupt:
            click.echo("Interrupted!")
            context.exit(1)

        except FileNotFoundError as err:
            click.echo(err.strerror)
            context.exit(err.errno)

        except keycloak.KeycloakError as err:
            click.echo(f"Keycloak auth error: {err.error_message}")
            context.exit(1)

        except grpc.RpcError as err:
            # NB (k.zhovnovatiy): All RpcError subclasses inherit from grpc.Call as well
            err_call: grpc.Call = cast(grpc.Call, err)
            click.echo("gRPC call failed!")
            click.echo(f"code: {err_call.code()}")
            click.echo(f"details: {err_call.details()}")
            context.exit(1)

        except wave.Error as err:
            click.echo(f"Error while trying to open audio file: {err}")
            click.echo("This client only supports WAV files in PCM (int16le) format.")
            context.exit(1)

    return wrapper
