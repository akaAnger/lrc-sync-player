# Quickstart

## Install

```bash
git clone https://github.com/akaAnger/lrc-sync-player.git
cd lrc-sync-player
pip install -r requirements.txt
```

## Run with default names

Put these files in the project root:

```text
song.mp3
lyrics.lrc
```

Then run:

```bash
python sync_player.py
```

## Run with custom files

```bash
python sync_player.py path/to/song.mp3 path/to/lyrics.lrc
```

## Fix timing

If lyrics appear too late, use a negative offset:

```bash
python sync_player.py song.mp3 lyrics.lrc --offset -0.5
```

If lyrics appear too early, use a positive offset:

```bash
python sync_player.py song.mp3 lyrics.lrc --offset 0.5
```

## Change animation speed

```bash
python sync_player.py song.mp3 lyrics.lrc --cps 20
```

Disable animation:

```bash
python sync_player.py song.mp3 lyrics.lrc --cps 0
```

## LRC format

```lrc
[00:15.30]First lyric line
[00:18.50]Second lyric line
[00:22.10]Third lyric line
```

A sample file is available at `examples/lyrics.lrc`.

## Run tests

```bash
python -m unittest discover -s tests
```
