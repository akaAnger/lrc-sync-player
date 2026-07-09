# LRC Sync Player

**LRC Sync Player** is a small Python terminal application for playing an audio file while displaying synchronized lyrics from an `.lrc` file.

The project is focused on a simple, readable implementation of timestamp-based lyric playback: audio is handled with `pygame`, while terminal output and text animation are handled with `rich`.

## Features

- Play local MP3 audio files.
- Parse `.lrc` lyrics with timestamps.
- Display the current lyric line in sync with playback.
- Animate lyrics with a configurable typewriter effect.
- Apply a manual sync offset when lyrics are slightly early or late.
- Render formatted terminal output with `rich`.

## Tech stack

- Python 3.7+
- pygame
- rich
- LRC timestamp format

## Installation

Clone the repository:

```bash
git clone https://github.com/akaAnger/1337-5yn6.git
cd 1337-5yn6
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place your files in the project directory:

```text
song.mp3
lyrics.lrc
```

Run the player:

```bash
python sync_player.py
```

## LRC format

```lrc
[00:15.30]First lyric line
[00:18.50]Second lyric line
[00:22.10]Third lyric line
```

## Configuration

The player supports the following runtime parameters in code:

| Parameter | Purpose |
| --- | --- |
| `audio_path` | Path to the local audio file. |
| `lrc_path` | Path to the `.lrc` lyrics file. |
| `offset_sec` | Manual sync offset in seconds. |
| `cps` | Typewriter animation speed in characters per second. |

## Project scope

This is a compact utility and learning project. It is useful as a reference for:

- parsing timestamped text files;
- synchronizing UI output with audio playback;
- building terminal interfaces with `rich`;
- working with local media playback in Python.

## Roadmap

- Add command-line arguments for file paths and offset.
- Add pause/resume controls.
- Add support for more audio formats where available through `pygame`.
- Add tests for LRC parsing and timestamp matching.
- Rename the repository to a clearer name, for example `lrc-sync-player`.

## License

MIT
