from pathlib import Path
from typing import Final

_this_directory = Path(__file__).parent
SETTINGS_TEMPLATE: Final = _this_directory / "config_files" / "settings_template.ini"
