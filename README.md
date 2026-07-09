# LRC Sync Player

**LRC Sync Player** is a small Python terminal app for playing local audio while showing synchronized lyrics from an `.lrc` file.

It is intentionally compact: audio playback is handled by `pygame`, terminal output by `rich`, and the LRC parser is kept readable enough to use as a learning/reference project.

## Features

- Play local audio files supported by `pygame`.
- Parse timestamped `.lrc` lyrics.
- Show lyric lines in sync with playback.
- Configure sync offset from the command line.
- Enable or disable typewriter-style lyric animation.
- Run parser tests with the standard Python test runner.

## Tech stack

- Python 3.7+
- pygame
- rich
- LRC timestamp format

## Installation

```bash
git clone https://github.com/akaAnger/lrc-sync-player.git
cd lrc-sync-player
pip install -r requirements.txt
```

## Usage

Default file names:

```bash
python sync_player.py
```

This expects:

```text
song.mp3
lyrics.lrc
```

Custom paths:

```bash
python sync_player.py path/to/song.mp3 path/to/lyrics.lrc
```

Adjust lyric timing:

```bash
python sync_player.py song.mp3 lyrics.lrc --offset -0.5
```

Disable typewriter animation:

```bash
python sync_player.py song.mp3 lyrics.lrc --cps 0
```

Show all options:

```bash
python sync_player.py --help
```

## LRC example

```lrc
[00:00.00]LRC Sync Player example
[00:03.50]Put your own timestamped lyrics here
[00:07.00]Run the player with your audio file
```

A sample file is included in `examples/lyrics.lrc`.

## Tests

```bash
python -m unittest discover -s tests
```

## Project scope

This is a compact utility and learning project. It is useful as a reference for:

- parsing timestamped text files;
- synchronizing terminal output with audio playback;
- building simple CLI tools;
- working with local media playback in Python.

## Roadmap

- Add pause/resume controls.
- Add a small terminal progress indicator.
- Add optional plain-text mode for environments without rich output.
- Add packaging metadata for installing as a console command.

## License

MIT
