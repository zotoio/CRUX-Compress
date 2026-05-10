# Subtask: MCP Server (crux_mcp_server)

## Metadata
- **Subtask ID**: 09
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 05
- **Created**: 20260403

## Objective

Create the `crux_mcp_server` — a modular MCP server that starts with memory-related tools and is architectured for future addition of other CRUX functions. Supports both HTTP and stdio transport modes via a `-t` parameter.

## Deliverables Checklist

### Directory Structure
- [ ] `crux_mcp_server/` at repo root with decomposed structure:
  ```
  crux_mcp_server/
  ├── README.md                    # Server documentation
  ├── requirements.txt             # Python dependencies (mcp, pyyaml, sentence-transformers optional)
  ├── __main__.py                  # Entry point with -t param
  ├── server.py                    # Core MCP server setup
  ├── config.py                    # Config loading from .crux/crux-memories.json
  ├── tools/                       # Tool modules (modular)
  │   ├── __init__.py
  │   └── memory/                  # Memory tools module
  │       ├── __init__.py
  │       ├── search.py            # memory-search tool
  │       ├── read.py              # memory-read tool
  │       └── stats.py             # memory-stats tool
  ├── indexer/                     # Memory indexing engine
  │   ├── __init__.py
  │   ├── scanner.py               # File system scanner
  │   ├── watcher.py               # File system watcher
  │   └── search_engine.py         # TF-IDF / sentence-transformers
  └── utils/                       # Shared utilities
      ├── __init__.py
      ├── frontmatter.py           # YAML frontmatter parser
      └── crux_decompress.py       # CRUX decompression for .memory.crux.md
  ```

### Transport Modes
- [ ] `-t stdio` (default): MCP stdio transport — reads JSON-RPC from stdin, writes to stdout
- [ ] `-t http`: MCP HTTP/SSE transport — runs on configurable port
- [ ] `--config` flag: path to `.crux/crux-memories.json` (default: auto-detect from CWD)

### Memory Tools (first module)
- [ ] `memory-search`: Semantic search across memories
  - Input: `query`, `limit`, `types`, `tags`, `agentId`, `minStrength`, `includeContent`
  - Output: ranked results with frontmatter and file paths (+ optional content)
  - Search engine: `sentence-transformers` when available, TF-IDF fallback over title/description/tags
- [ ] `memory-read`: Read full content of memory files by slug or path
  - Input: `slugs[]`, `files[]`
  - Output: full file contents for each
  - Decompresses `*.memory.crux.md` bodies on read
- [ ] `memory-stats`: Summary statistics about the memory corpus
  - Output: counts by type, total memories, index freshness

### Indexing Engine
- [ ] On startup: read `.crux/memory-index.yml` and scan all memory files to build search index
- [ ] File system watcher: detect create/modify/delete/move in `memoriesDir` and update index incrementally
- [ ] Re-sync when `.crux/memory-index.yml` is modified (post-dream/REM trigger)
- [ ] For compressed memories: index frontmatter directly (never compressed), optionally decompress body for richer search

### Modularity
- [ ] Tool registration system: tools are discovered from `tools/` subdirectories
- [ ] Each tool module exposes a standard interface for registration
- [ ] Future CRUX tools (e.g., compression, validation) can be added as new subdirectories under `tools/`

### Server Properties
- [ ] Read-only: never writes memory files or tracker files
- [ ] Respects agent scoping: `agentId` parameter controls visible agent directories
- [ ] Graceful degradation: works without `sentence-transformers` (falls back to TF-IDF)

## Definition of Done
- [ ] Server starts in stdio mode: `python -m crux_mcp_server -t stdio --config .crux/crux-memories.json`
- [ ] Server starts in HTTP mode: `python -m crux_mcp_server -t http --config .crux/crux-memories.json`
- [ ] All 3 memory tools respond correctly
- [ ] Search returns relevant results for test queries
- [ ] Agent scoping filters work correctly
- [ ] `includeContent` toggle works for memory-search
- [ ] File watcher detects changes and updates index
- [ ] No Python linter errors

## Implementation Notes

Reference `docs/crux-memories.md`:
- "MCP Memory Server Specification" section for tool schemas
- "Reference Local stdio Server" section for server implementation guidance
- "Indexing Workflow" section for startup and re-sync behavior

Use the Python `mcp` package for MCP protocol handling. The server should follow MCP SDK conventions for tool registration.

**Python version**: Require `>=3.10` — specify in `crux_mcp_server/requirements.txt` header.

For the search engine:
- Try importing `sentence_transformers` first. If available, use it for embedding-based semantic search
- Fall back to a lightweight TF-IDF implementation using only Python stdlib (`collections.Counter`, `math.log` for IDF weighting) + `pyyaml` (already required). Do NOT depend on `sklearn` or other heavy packages for the fallback path
- Mark `sentence-transformers` as optional in `requirements.txt` with a comment (e.g., `# Optional: sentence-transformers>=2.0  # for semantic search, falls back to TF-IDF without it`)
- Index title, description, and tags from frontmatter (these are never compressed)

The modular architecture means each tool "module" (directory under `tools/`) registers its tools with the server. This allows future additions like `tools/compression/` or `tools/validation/` without modifying core server code.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Test server startup in both modes
- Test each tool endpoint with sample queries
- Defer full test suite execution to the final verification phase

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
