import hashlib
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    def __init__(self, inbox_path: Path, on_change):
        self._inbox_path = inbox_path
        self._on_change = on_change
        self._last_trigger = 0.0
        # Seed with current content so startup doesn't reprocess an unchanged file.
        self._last_seen_hash = self._hash_inbox()

    def _hash_inbox(self) -> str | None:
        try:
            return hashlib.sha256(self._inbox_path.read_bytes()).hexdigest()
        except FileNotFoundError:
            return None

    def _is_inbox(self, path: str) -> bool:
        p = Path(path)
        return p.name == self._inbox_path.name and p.parent == self._inbox_path.parent

    def _process(self):
        """Debounced trigger for the change callback."""
        now = time.monotonic()
        if now - self._last_trigger < 1.0:
            return
        current_hash = self._hash_inbox()
        if current_hash is None or current_hash == self._last_seen_hash:
            return  # no real change, or we're looking at our own post-write state
        self._last_trigger = now
        print(f"{self._inbox_path} updated, processing...")
        self._on_change()
        # Capture the file state the bee just produced so the polling observer's
        # next tick doesn't re-trigger on our own write.
        self._last_seen_hash = self._hash_inbox()

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

