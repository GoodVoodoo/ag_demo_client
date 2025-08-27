from pathlib import Path


def save_file_dir(
    client_id: str,
    request_id: str,
    trace_id: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
) -> Path:
    if not root:
        root = Path("./request_data/")

    path = root / client_id

    if trace_id:
        path = path / trace_id
    elif session_id:
        path = path / session_id

    path = path / request_id

    return path
