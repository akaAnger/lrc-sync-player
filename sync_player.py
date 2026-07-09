from __future__ import annotations

import argparse
import os
import re
import sys
import threading
import time
from pathlib import Path
from typing import List, Tuple

import pygame
from rich.console import Console
from rich.text import Text

console = Console()
TIMESTAMP = re.compile(r"\[(\d{1,2}):(\d{2})(?:\.(\d{1,3}))?\]\s*(.*)")


class PlayerError(RuntimeError):
    """Raised when the player cannot start with the provided input."""


def parse_lrc(path: Path) -> List[Tuple[float, str]]:
    """Parse an LRC file into sorted ``(time_seconds, lyric_line)`` pairs."""
    lines: List[Tuple[float, str]] = []

    for raw in path.read_text(encoding="utf-8").splitlines():
        match = TIMESTAMP.match(raw)
        if not match:
            continue

        minutes, seconds, fraction, text = match.groups()
        milliseconds = _fraction_to_seconds(fraction)
        timestamp = int(minutes) * 60 + int(seconds) + milliseconds

        lyric = text.strip()
        if lyric:
            lines.append((timestamp, lyric))

    return sorted(lines, key=lambda item: item[0])


def _fraction_to_seconds(value: str | None) -> float:
    if not value:
        return 0.0

    if len(value) == 1:
        return int(value) / 10
    if len(value) == 2:
        return int(value) / 100
    return int(value[:3]) / 1000


def type_line(text: str, cps: float = 35) -> None:
    """Print a lyric line with a typewriter effect."""
    if cps <= 0:
        console.print(f"[yellow]{text}[/yellow]")
        return

    delay = 1.0 / cps
    output = Text(style="yellow")

    for character in text:
        output.append(character)
        console.print(output, end="\r")
        time.sleep(delay)

    console.print()


def play_audio(audio_path: Path) -> None:
    """Play a local audio file using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(str(audio_path))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def validate_inputs(audio_path: Path, lrc_path: Path) -> List[Tuple[float, str]]:
    if not audio_path.exists():
        raise PlayerError(f"Audio file not found: {audio_path}")

    if not lrc_path.exists():
        raise PlayerError(f"LRC file not found: {lrc_path}")

    lyrics = parse_lrc(lrc_path)
    if not lyrics:
        raise PlayerError("LRC file is empty or has no valid timestamped lines.")

    return lyrics


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def run(audio_path: Path, lrc_path: Path, offset: float = 0.0, cps: float = 35) -> int:
    """Run synchronized audio and lyric playback."""
    try:
        lyrics = validate_inputs(audio_path, lrc_path)
    except PlayerError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    clear_screen()
    console.print("\n[bold bright_cyan]LRC Sync Player[/bold bright_cyan]")
    console.print("[dim]Starting playback...[/dim]\n")

    audio_thread = threading.Thread(target=play_audio, args=(audio_path,), daemon=True)
    audio_thread.start()
    time.sleep(0.4)

    clear_screen()
    started_at = time.perf_counter()

    try:
        for timestamp, line in lyrics:
            target = timestamp + offset
            while target - (time.perf_counter() - started_at) > 0:
                time.sleep(0.01)

            type_line(line, cps=cps)

        console.print("\n[bold bright_magenta]Playback finished.[/bold bright_magenta]\n")
        return 0

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        console.print("\n[yellow]Playback interrupted by user.[/yellow]")
        return 130


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Play local audio while showing synchronized lyrics from an LRC file."
    )
    parser.add_argument("audio", nargs="?", default="song.mp3", help="Path to the audio file.")
    parser.add_argument("lyrics", nargs="?", default="lyrics.lrc", help="Path to the LRC file.")
    parser.add_argument(
        "--offset",
        type=float,
        default=0.0,
        help="Manual sync offset in seconds. Use negative values when lyrics are late.",
    )
    parser.add_argument(
        "--cps",
        type=float,
        default=35,
        help="Typewriter speed in characters per second. Use 0 to disable animation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run(Path(args.audio), Path(args.lyrics), offset=args.offset, cps=args.cps)


if __name__ == "__main__":
    sys.exit(main())
