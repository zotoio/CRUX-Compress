"""Entry point: ``python -m crux_mcp_server``."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="crux-mcp-server",
        description="CRUX Memory MCP Server",
    )
    parser.add_argument(
        "-t", "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8742,
        help="HTTP port (default: 8742)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to crux-memories.json (optional fallback when MCP roots unavailable)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root directory (optional fallback when MCP roots unavailable)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log level (default: INFO)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    if sys.version_info < (3, 10):
        sys.exit("Python >= 3.10 is required")

    from crux_mcp_server.server import create_server

    server, registry = create_server(
        config_path=args.config,
        project_root=args.project_root,
    )

    try:
        if args.transport == "stdio":
            server.run(transport="stdio")
        else:
            server.run(transport="http", host=args.host, port=args.port)
    finally:
        registry.shutdown()


if __name__ == "__main__":
    main()
