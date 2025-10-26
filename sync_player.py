# sync_player.py
from __future__ import annotations
import re, time, threading, os, sys
from pathlib import Path
from typing import List, Tuple
from rich.console import Console
from rich.text import Text
import pygame

console = Console()
TIMESTAMP = re.compile(r'\[(\d{1,2}):(\d{2})(?:\.(\d{1,3}))?\]\s*(.*)')

COLORS = [
    'bright_magenta', 'magenta', 'bright_blue', 'blue', 
    'bright_cyan', 'cyan', 'bright_green', 'green',
    'bright_yellow', 'yellow', 'bright_red', 'red'
]


def parse_lrc(p: Path) -> List[Tuple[float, str]]:
    """Парсинг LRC файла с временными метками лирики."""
    lines: List[Tuple[float, str]] = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        m = TIMESTAMP.match(raw)
        if not m:
            continue
        mm, ss, ms, text = m.groups()
        t = int(mm)*60 + int(ss) + (int(ms)/(100 if ms and len(ms)==2 else 1000) if ms else 0)
        if text.strip():
            lines.append((t, text.strip()))
    lines.sort(key=lambda x: x[0])
    return lines


def type_line(text: str, color_index: int = 0, cps: float = 30):
    """Анимированный вывод текста с эффектом печатания."""
    if cps <= 0:
        console.print(f"[yellow]{text}[/yellow]")
        return
    
    delay = 1.0 / cps
    line_text = Text()
    
    for i, char in enumerate(text):
        line_text.append(char, style="yellow")
        console.print(line_text, end="\r")
        time.sleep(delay)
    
    console.print()


def play_audio(audio_path: Path):
    """Воспроизведение аудио файла."""
    pygame.mixer.init()
    pygame.mixer.music.load(str(audio_path))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def run(audio_path: str, lrc_path: str, offset_sec: float = 0.0, cps: float = 35):
    """Основная функция запуска синхронизированного проигрывателя."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print("\n[bold bright_cyan]🎵 Music Lyrics Sync Player 🎵[/bold bright_cyan]")
    console.print("[dim]Loading...[/dim]\n")
    
    # Проверяем существование файлов
    if not Path(audio_path).exists():
        console.print(f"[red]Ошибка: Аудио файл не найден: {audio_path}[/red]")
        return
    
    if not Path(lrc_path).exists():
        console.print(f"[red]Ошибка: LRC файл не найден: {lrc_path}[/red]")
        return
    
    lrc = parse_lrc(Path(lrc_path))
    if not lrc:
        console.print("[red]Ошибка: LRC файл пуст или неверного формата[/red]")
        return
    
    # Запускаем аудио в отдельном потоке
    threading.Thread(target=play_audio, args=(Path(audio_path),), daemon=True).start()
    time.sleep(0.5)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    t0 = time.perf_counter()
    color_index = 0
    
    try:
        for t_abs, line in lrc:
            t_target = t_abs + offset_sec
            while (t_target - (time.perf_counter() - t0)) > 0:
                time.sleep(0.01)
            
            type_line(line, color_index, cps=cps)
            color_index += 1
        
        console.print("\n[bold bright_magenta]✨ Спасибо за прослушивание! ✨[/bold bright_magenta]\n")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Воспроизведение прервано пользователем[/yellow]")


if __name__ == "__main__":
    # Пример использования
    run(
        audio_path="song.mp3",
        lrc_path="lyrics.lrc",
        offset_sec=-0.5,
        cps=20
    )