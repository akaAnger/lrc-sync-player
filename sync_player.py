from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple

import pygame
from rich.console import Console
from rich.text import Text

console = Console()
TIMESTAMP = re.compile(r"\[(\d{1,3}):([0-5]\d)(?:[.:](\d{1,3}))?\]")
OFFSET = re.compile(r"^\[offset:([+-]?\d+)\]$", re.IGNORECASE)


class PlayerError(RuntimeError):
    """Raised when the player cannot start with the provided input."""


def parse_lrc(path: Path) -> List[Tuple[float, str]]:
    """Parse an LRC file into sorted ``(time_seconds, lyric_line)`` pairs."""
    try:
        raw_lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        raise PlayerError(f"Could not read LRC file: {path}") from exc

    lines: List[Tuple[float, str]] = []
    offset_seconds = 0.0

    for raw in raw_lines:
        if offset_match := OFFSET.match(raw.strip()):
            offset_seconds = int(offset_match.group(1)) / 1000

    for raw in raw_lines:
        if OFFSET.match(raw.strip()):
            continue
        timestamps = []
        cursor = 0

        while match := TIMESTAMP.match(raw, cursor):
            timestamps.append(match)
            cursor = match.end()

        if not timestamps:
            continue

        # Empty timestamped lines are meaningful in LRC files: they clear or
        # visually separate the previously displayed lyric at an exact time.
        lyric = raw[cursor:].strip()

        for match in timestamps:
            minutes, seconds, fraction = match.groups()
            timestamp = (
                int(minutes) * 60
                + int(seconds)
                + _fraction_to_seconds(fraction)
            )
            lines.append((timestamp + offset_seconds, lyric))

    return sorted(lines, key=lambda item: item[0])


def _fraction_to_seconds(value: str | None) -> float:
    if not value:
        return 0.0

    if len(value) == 1:
        return int(value) / 10
    if len(value) == 2:
        return int(value) / 100
    return int(value[:3]) / 1000


def type_line(text: str, cps: float = 35, max_duration: float | None = None) -> None:
    """Print a lyric line without allowing animation to delay the next line."""
    if cps <= 0 or not text:
        console.print(Text(text, style="yellow"))
        return

    delay = 1.0 / cps
    if max_duration is not None:
        if max_duration <= 0:
            console.print(Text(text, style="yellow"))
            return
        delay = min(delay, max_duration / len(text))

    output = Text(style="yellow")

    for character in text:
        output.append(character)
        console.print(output, end="\r")
        time.sleep(delay)

    console.print()


def start_audio(audio_path: Path) -> float:
    """Start audio playback and return the matching monotonic start time."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(audio_path))
        pygame.mixer.music.play()
    except (pygame.error, OSError) as exc:
        stop_audio()
        raise PlayerError(f"Could not play audio file: {audio_path} ({exc})") from exc

    return time.perf_counter()


def stop_audio() -> None:
    """Stop playback and release the mixer when it is initialized."""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    except pygame.error:
        pass


def validate_inputs(audio_path: Path, lrc_path: Path) -> List[Tuple[float, str]]:
    if not audio_path.is_file():
        raise PlayerError(f"Audio file not found: {audio_path}")

    if not lrc_path.is_file():
        raise PlayerError(f"LRC file not found: {lrc_path}")

    lyrics = parse_lrc(lrc_path)
    if not lyrics:
        raise PlayerError("LRC file is empty or has no valid timestamped lines.")

    return lyrics


def clear_screen() -> None:
    console.clear()


def wait_until(target: float, started_at: float) -> None:
    """Wait for a timestamp while detecting unexpectedly ended playback."""
    while True:
        remaining = target - (time.perf_counter() - started_at)
        if remaining <= 0:
            return

        if not pygame.mixer.music.get_busy():
            raise PlayerError(
                "Audio playback ended before all lyric timestamps were reached."
            )

        time.sleep(min(0.01, remaining))


def run(audio_path: Path, lrc_path: Path, offset: float = 0.0, cps: float = 35) -> int:
    """Run synchronized audio and lyric playback."""
    try:
        lyrics = validate_inputs(audio_path, lrc_path)
    except PlayerError as exc:
        console.print(Text(str(exc), style="red"))
        return 1

    clear_screen()
    console.print("\n[bold bright_cyan]LRC Sync Player[/bold bright_cyan]")
    console.print("[dim]Starting playback...[/dim]\n")

    try:
        started_at = start_audio(audio_path)

        for index, (timestamp, line) in enumerate(lyrics):
            target = timestamp + offset
            wait_until(target, started_at)

            animation_window = None
            if index + 1 < len(lyrics):
                next_timestamp = lyrics[index + 1][0] + offset
                animation_window = max(0.0, next_timestamp - target - 0.02)

            type_line(line, cps=cps, max_duration=animation_window)

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        console.print("\n[bold bright_magenta]Playback finished.[/bold bright_magenta]\n")
        return 0

    except PlayerError as exc:
        console.print(Text(f"\n{exc}", style="red"))
        return 1
    except KeyboardInterrupt:
        console.print("\n[yellow]Playback interrupted by user.[/yellow]")
        return 130
    finally:
        stop_audio()


def finite_float(value: str) -> float:
    """Parse a finite floating-point CLI value."""
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"expected a number, got {value!r}") from exc

    if not math.isfinite(parsed):
        raise argparse.ArgumentTypeError("value must be finite")

    return parsed


def nonnegative_float(value: str) -> float:
    """Parse a finite floating-point CLI value greater than or equal to zero."""
    parsed = finite_float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be greater than or equal to zero")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Play local audio while showing synchronized lyrics from an LRC file."
    )
    parser.add_argument("audio", nargs="?", default="song.mp3", help="Path to the audio file.")
    parser.add_argument("lyrics", nargs="?", default="lyrics.lrc", help="Path to the LRC file.")
    parser.add_argument(
        "--offset",
        type=finite_float,
        default=0.0,
        help="Manual sync offset in seconds. Use negative values when lyrics are late.",
    )
    parser.add_argument(
        "--cps",
        type=nonnegative_float,
        default=35,
        help="Typewriter speed in characters per second. Use 0 to disable animation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run(Path(args.audio), Path(args.lyrics), offset=args.offset, cps=args.cps)


if __name__ == "__main__":
    sys.exit(main())
