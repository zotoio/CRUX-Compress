# CRUX MCP Server

A modular MCP (Model Context Protocol) server providing read-only access to the CRUX memory corpus.

## Requirements

- Python >= 3.10

## Install

```bash
pipx install ./crux_mcp_server
```

With embedding-based semantic search (optional, falls back to TF-IDF without it):

```bash
pipx install "./crux_mcp_server[embeddings]"
```

Or with pip:

```bash
pip install ./crux_mcp_server
```

Then add the server to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "crux-memories": {
      "command": "crux-mcp-server",
      "args": ["-t", "stdio", "--config", ".crux/crux-memories.json"]
    }
  }
}
```

## Usage

### stdio transport (default)

```bash
crux-mcp-server
```

### HTTP transport

```bash
crux-mcp-server -t http --port 8742
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-t`, `--transport` | `stdio` | Transport mode: `stdio` or `http` |
| `--host` | `127.0.0.1` | HTTP bind address |
| `--port` | `8742` | HTTP port |
| `--config` | auto-detect | Path to `.crux/crux-memories.json` |
| `--project-root` | CWD | Project root directory |
| `--log-level` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Tools

### `memory-search`

Semantic search across memories. Returns ranked results with frontmatter and file paths.

**Parameters**: `query` (required), `limit`, `types`, `tags`, `agentId`, `minStrength`, `includeContent`

### `memory-read`

Read full content of memory files by slug or path. Decompresses `*.memory.crux.md` bodies automatically.

**Parameters**: `slugs[]`, `files[]`

### `memory-stats`

Summary statistics: counts by type, total memories, index freshness, search backend.

## Architecture

```
crux_mcp_server/
├── pyproject.toml       # Package metadata and dependencies
├── __init__.py          # Package marker
├── __main__.py          # CLI entry point
├── server.py            # Server creation and lifecycle
├── config.py            # Configuration loader
├── tools/               # Auto-discovered tool modules
│   └── memory/          # Memory tools (search, read, stats)
├── indexer/             # Scanning, watching, search engine
│   ├── scanner.py       # Builds MemoryIndex from filesystem
│   ├── watcher.py       # Detects file changes, triggers rebuild
│   └── search_engine.py # TF-IDF + optional embeddings
└── utils/               # Shared utilities
    ├── frontmatter.py   # YAML frontmatter parser
    └── crux_decompress.py # Best-effort CRUX symbol expansion
```

## Adding New Tools

Create a new subdirectory under `tools/` with an `__init__.py` that exposes a `register(server, ctx)` function. The server auto-discovers and registers tool modules at startup.
