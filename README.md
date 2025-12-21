# Elf on the Shelf - Reachy Mini

A Reachy Mini application that brings holiday magic to life!

## Features
- **Sentry Scout Mode**: Reachy freezes when it sees a human face.
- **Naughty/Nice Scanner**: Uses voice commands to scan users and determine if they are on the Naughty or Nice list.

## Installation

### Prerequisites
- Python >= 3.11
- System dependencies (for PyAudio):
  - **macOS**: `brew install portaudio`
  - **Linux**: `sudo apt-get install libportaudio2`

### Using UV (Recommended)
This project is optimized for [uv](https://github.com/astral-sh/uv).

```bash
pip install uv
uv sync
```

### Using Pip (Fallback)
If you cannot use `uv`, you can install with standard pip:

```bash
pip install .
```

## Usage

### Run with UV
```bash
uv run python -m elf_on_shelf.main
```

### Run with Python (after pip install)
```bash
python -m elf_on_shelf.main
# Or check the connection to a robot:
python tests/test_connection.py --host reachy-mini.local
```
