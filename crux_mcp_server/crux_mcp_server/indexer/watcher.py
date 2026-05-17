"""Filesystem watcher for incremental memory index updates."""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

if TYPE_CHECKING:
    from crux_mcp_server.config import ServerConfig

logger = logging.getLogger(__name__)


class MemoryFileHandler(FileSystemEventHandler):
    """Triggers a rebuild callback when memory files change."""

    MEMORY_SUFFIXES = (".memory.md", ".memory.crux.md")

    def __init__(self, on_change: Callable[[], None], index_file: Path) -> None:
        super().__init__()
        self._on_change = on_change
        self._index_file = index_file
        self._debounce_timer: threading.Timer | None = None
        self._debounce_seconds = 1.0

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        src = str(getattr(event, "src_path", ""))

        is_memory = any(src.endswith(s) for s in self.MEMORY_SUFFIXES)
        is_index = Path(src).resolve() == self._index_file.resolve()

        if not (is_memory or is_index):
            return

        if self._debounce_timer is not None:
            self._debounce_timer.cancel()

        self._debounce_timer = threading.Timer(self._debounce_seconds, self._fire)
        self._debounce_timer.daemon = True
        self._debounce_timer.start()

    def _fire(self) -> None:
        logger.info("Memory files changed — rebuilding index")
        try:
            self._on_change()
        except Exception:
            logger.error("Error during index rebuild", exc_info=True)


class MemoryWatcher:
    """Watches memory directories for changes and triggers index rebuilds."""

    def __init__(self, config: ServerConfig, on_change: Callable[[], None]) -> None:
        self._config = config
        self._on_change = on_change
        self._observer: Observer | None = None
        self._started = False

    def start(self) -> None:
        root = self._config.project_root
        index_file = root / self._config.memories.storage.index_file
        handler = MemoryFileHandler(self._on_change, index_file)

        self._observer = Observer()

        watch_dirs = [
            root / self._config.memories.storage.memories_dir,
            root / self._config.memories.storage.agent_memories_dir,
        ]

        index_dir = index_file.parent
        if index_dir.is_dir():
            watch_dirs.append(index_dir)

        for d in watch_dirs:
            if d.is_dir():
                self._observer.schedule(handler, str(d), recursive=True)
                logger.debug("Watching: %s", d)

        self._observer.daemon = True
        self._observer.start()
        self._started = True
        logger.info("File watcher started")

    def stop(self) -> None:
        if self._observer is not None:
            self._observer.stop()
            if self._started:
                self._observer.join(timeout=5)
            logger.info("File watcher stopped")
