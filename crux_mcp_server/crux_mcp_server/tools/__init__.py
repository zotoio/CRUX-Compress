"""Tool registration helpers.

Each subdirectory under ``tools/`` is a tool module.  A module is discovered
when it contains an ``__init__.py`` that exposes a ``register(server, registry)``
function.
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from crux_mcp_server.server import ProjectRegistry
    from fastmcp import FastMCP

logger = logging.getLogger(__name__)


def discover_and_register(server: FastMCP, registry: ProjectRegistry) -> list[str]:
    """Walk ``tools/`` sub-packages and call each ``register()``."""
    registered: list[str] = []
    package = importlib.import_module("crux_mcp_server.tools")

    for finder, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if not is_pkg:
            continue
        try:
            mod = importlib.import_module(name)
            if hasattr(mod, "register"):
                mod.register(server, registry)  # type: ignore[attr-defined]
                registered.append(name.split(".")[-1])
                logger.info("Registered tool module: %s", name)
        except Exception:
            logger.error("Failed to register tool module: %s", name, exc_info=True)

    return registered
