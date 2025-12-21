# Elf on the Shelf - Reachy Mini

A Reachy Mini application that brings holiday magic to life!

## Features
- **Magic Elf Mode**: Reachy acts "Alive" (looks around, plays Jingle Bells) when no one is watching. If a face is detected, it freezes instantly with a "Surprise!" expression.
- **Procedural Audio**: Generates synthesized audio effects and music real-time without external asset files.

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
