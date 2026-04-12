import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    def __init__(self, inbox_path: Path, on_change):
        self._inbox_path = inbox_path
        self._on_change = on_change
        self._last_trigger = 0.0

    def _is_inbox(self, path: str) -> bool:
        p = Path(path)
        return p.name == self._inbox_path.name and p.parent == self._inbox_path.parent

    def _process(self):
        """Debounced trigger for the change callback."""
        now = time.monotonic()
        if now - self._last_trigger < 1.0:
            return
        self._last_trigger = now
        print(f"{self._inbox_path} updated, processing...")
        self._on_change()

    def on_modified(self, event):
        print(f"[watchdog] modified: {event.src_path}")
        if not event.is_directory and self._is_inbox(event.src_path):
            self._process()

    def on_created(self, event):
        print(f"[watchdog] created: {event.src_path}")
        if not event.is_directory and self._is_inbox(event.src_path):
            self._process()

    def on_moved(self, event):
        print(f"[watchdog] moved: {event.src_path} -> {event.dest_path}")
        if not event.is_directory and self._is_inbox(event.dest_path):
            self._process()

