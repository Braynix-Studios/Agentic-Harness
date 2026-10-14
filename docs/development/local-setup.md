# Local Setup

## Requirements

- Python 3.11 or newer
- Git

## Environment

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Checks

```bash
ruff check .
pytest
```

The initial scaffold contains no working agent service. Select dependencies and runtime entry points through reviewed implementation work rather than installing a broad framework stack by default.
