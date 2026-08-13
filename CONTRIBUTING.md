# Contributing

Thanks for helping improve LRC Sync Player. Keep changes focused, easy to review, and compatible with Python 3.10+.

## Local setup

1. Create and activate a virtual environment.
2. Install the project in editable mode:

```bash
python -m pip install -e .
```

3. Run the test suite before opening a pull request:

```bash
python -m unittest discover -s tests -v
```

## Pull requests

- Keep one logical change per pull request.
- Add or update tests when behavior changes.
- Avoid unrelated formatting or dependency changes.
- Preserve the command-line entry point: `lrc-sync-player`.
- Do not commit local audio files, virtual environments, caches, or generated build artifacts.

## Packaging checks

When changing `pyproject.toml`, packaging metadata, or the CLI entry point, also verify that the project builds and the distributions are valid:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

The GitHub Actions workflow repeats the supported-Python and package checks on pull requests.