import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    def __init__(self, inbox_path: Path, on_change):
        self._inbox_path = inbox_path
        self._on_change = on_change
        self._last_trigger = 0.0

    def _process(self):
        """Debounced trigger for the change callback."""
        now = time.monotonic()
        if now - self._last_trigger < 1.0:
            return
        self._last_trigger = now
        print(f"{self._inbox_path} updated, processing...")
        self._on_change()

    def on_modified(self, event):
        if not event.is_directory:
            self._process()

    def on_created(self, event):
        if not event.is_directory:
            self._process()

    def on_moved(self, event):
        if not event.is_directory:
            self._process()

