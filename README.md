# LRC Sync Player

**LRC Sync Player** is a compact Python terminal app that plays local audio and displays synchronized lyrics from an `.lrc` file.

The project is intentionally small and readable: `pygame` handles audio playback, `rich` renders terminal output, and the LRC parser stays simple enough to use as a learning or reference implementation.

## Features

- Play local audio formats supported by `pygame`.
- Parse standard timestamped `.lrc` lyrics.
- Support multiple timestamps on one lyric line.
- Read UTF-8 and UTF-8 BOM lyric files.
- Show lyric lines in sync with playback.
- Adjust synchronization with a command-line offset.
- Enable or disable typewriter-style animation.
- Automatically speed up animation when the next lyric is close.
- Install and run as the `lrc-sync-player` command.
- Run automated tests on Python 3.10–3.13.

## Requirements

- Python 3.10+
- A working audio output device
- Audio files supported by the installed `pygame`/SDL build

## Installation

Clone and install the project:

```bash
git clone https://github.com/akaAnger/lrc-sync-player.git
cd lrc-sync-player
python -m pip install .
```

For local development, use an editable install:

```bash
python -m pip install -e .
```

Installing from `requirements.txt` and running the script directly is also supported:

```bash
python -m pip install -r requirements.txt
python sync_player.py
```

## Usage

After installation:

```bash
lrc-sync-player path/to/song.mp3 path/to/lyrics.lrc
```

Or run the Python file directly:

```bash
python sync_player.py path/to/song.mp3 path/to/lyrics.lrc
```

When no paths are supplied, the player looks for these files in the current directory:

```text
song.mp3
lyrics.lrc
```

Adjust lyric timing:

```bash
lrc-sync-player song.mp3 lyrics.lrc --offset -0.5
```

A negative offset shows lyrics earlier. A positive offset shows them later.

Disable typewriter animation for the most direct display:

```bash
lrc-sync-player song.mp3 lyrics.lrc --cps 0
```

Set a custom animation speed:

```bash
lrc-sync-player song.mp3 lyrics.lrc --cps 60
```

Show all options:

```bash
lrc-sync-player --help
```

## LRC example

```lrc
[00:00.00]LRC Sync Player example
[00:03.50]Put your own timestamped lyrics here
[00:07.00][00:20.00]This line appears twice
```

A sample file is included in `examples/lyrics.lrc`.

Supported timestamps include:

```text
[mm:ss]
[mm:ss.xx]
[mm:ss.xxx]
[mm:ss:xx]
```

Metadata lines such as `[ar:Artist]` are ignored.

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite against Python 3.10, 3.11, 3.12, and 3.13 for every pull request.

## Current scope

This is a focused terminal utility rather than a full media player. It does not currently provide pause/resume controls, seeking, playlists, embedded lyric downloading, or Enhanced LRC word-level timestamps.

It is useful as a reference for:

- parsing timestamped text files;
- synchronizing terminal output with local audio;
- building small command-line applications;
- packaging a single-module Python tool.

## Roadmap

- Add pause/resume and seek controls.
- Add a terminal progress indicator.
- Add optional Enhanced LRC word-level timing.
- Add integration tests for playback lifecycle handling.

## License

MIT
