import pytest
from click.testing import CliRunner


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()
