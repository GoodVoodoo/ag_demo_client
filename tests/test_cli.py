from click.testing import CliRunner

from clients.main import audiogram_cli


def test_audiogram_cli_help(runner: CliRunner):
    """Test the main audiogram command with --help flag."""
    result = runner.invoke(audiogram_cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: audiogram_cli [OPTIONS] COMMAND [ARGS]..." in result.output


def test_asr_group_help(runner: CliRunner):
    """Test the asr command group with --help flag."""
    result = runner.invoke(audiogram_cli, ["asr", "--help"])
    assert result.exit_code == 0
    assert "Usage: audiogram_cli asr [OPTIONS] COMMAND [ARGS]..." in result.output


def test_tts_group_help(runner: CliRunner):
    """Test the tts command group with --help flag."""
    result = runner.invoke(audiogram_cli, ["tts", "--help"])
    assert result.exit_code == 0
    assert "Usage: audiogram_cli tts [OPTIONS] COMMAND [ARGS]..." in result.output


def test_models_command_help(runner: CliRunner):
    """Test the models command with --help flag."""
    result = runner.invoke(audiogram_cli, ["models", "--help"])
    assert result.exit_code == 0
    assert "Usage: audiogram_cli models [OPTIONS]" in result.output
