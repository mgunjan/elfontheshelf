---
title: Elf on the Shelf
emoji: 🎄
colorFrom: green
colorTo: red
sdk: static
pinned: false
license: apache-2.0
tags:
  - reachy_mini
  - reachy_mini_python_app
  - robot
  - christmas
  - elf
---

# Elf on the Shelf - Reachy Mini App

A Reachy Mini application that brings holiday magic to life!

## ✨ Features

- **Magic Elf Mode**: Reachy acts "Alive" (looks around, wiggles antennas, plays Jingle Bells) when no one is watching. If a face is detected, it freezes instantly with a "Surprise!" expression.
- **Face Detection**: Uses the robot's camera to detect when someone is watching.
- **Procedural Audio**: Plays sounds on the robot's speakers.

## 🚀 Installation

### From Hugging Face (Recommended)
1. Go to your Reachy Mini dashboard: `http://reachy-mini.local:8000`
2. Find "Elf on the Shelf" in the app store
3. Click "Install"

### Manual Installation
```bash
# SSH into your robot
ssh reachy@reachy-mini.local

# Clone and install
git clone https://github.com/yourusername/elfontheshelf.git
cd elfontheshelf
pip install .
```

## 🎮 Usage

### From Dashboard
1. Open `http://reachy-mini.local:8000`
2. Find "Elf on the Shelf" in "Applications"
3. Click "Run"

### Standalone Mode
```bash
python -m elf_on_shelf.main --host localhost
```

## 🎄 How It Works

When running, the elf will:
1. Look around randomly, as if checking if anyone is watching
2. Wiggle its antennas playfully
3. Occasionally hum "Jingle Bells"
4. If someone looks at it - **FREEZE!** With a surprised expression

## 📦 Publishing Updates

```bash
reachy-mini-app-assistant publish
```

## License

Apache 2.0
