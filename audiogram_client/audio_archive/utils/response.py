import click
from pydantic import ValidationError
from requests import Response


def process_response(response: Response, model):
    try:
        response.raise_for_status()
        data = model.parse_obj(response.json())
        return data
    except ValidationError as e:
        click.echo(f"Error validating response: {e}")
        raise click.Abort()
    except Exception as e:
        click.echo(f"An error occurred: {e}")
        raise click.Abort()
