import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    def __init__(self, inbox_path: Path, on_change):
        self._inbox_path = inbox_path
        self._on_change = on_change
        self._last_trigger = 0.0

    def on_modified(self, event):
        if Path(event.src_path).resolve() != self._inbox_path.resolve():
            return
        now = time.monotonic()
        if now - self._last_trigger < 1.0:
            return
        self._last_trigger = now
        self._on_change()
