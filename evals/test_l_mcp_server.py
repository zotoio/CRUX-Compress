"""Category L: MCP Server tests.

Tests the crux_mcp_server package end-to-end: config loading, frontmatter
parsing, CRUX decompression, scanner/indexer, TF-IDF search engine, tool
registration, and the memory-search/read/stats tool functions.
"""

from __future__ import annotations

import asyncio
import json
import sys
import textwrap
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from conftest import MEMORY_TYPES, write_memory, write_tracker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_config(tmp_path: Path, **overrides) -> Path:
    """Write a standard crux-memories.json under tmp_path and return its path."""
    cfg_data = {
        "platform": "cursor",
        "flags": [{"enableMemories": "true"}],
        "cruxMemories": {
            "enabled": "true",
            "storage": {
                "memoriesDir": "memories",
                "agentMemoriesDir": "memories/agents",
                "archiveDir": ".ai-ignored/executed",
                "indexFile": ".crux/memory-index.yml",
            },
            "typePriority": MEMORY_TYPES,
            "referenceTracking": {
                "enabled": True,
                "trackingDir": ".crux/reference-tracking",
            },
            "scopeRanking": ["base", "agents", "shared"],
        },
    }
    for key, val in overrides.items():
        cfg_data["cruxMemories"][key] = val

    config_path = tmp_path / ".crux" / "crux-memories.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(cfg_data, indent=2), encoding="utf-8")
    return config_path


def _build_ctx(tmp_path: Path, config_path: Path | None = None):
    """Build an AppContext for testing (no watcher)."""
    from crux_mcp_server.config import load_config
    from crux_mcp_server.indexer.scanner import scan
    from crux_mcp_server.indexer.search_engine import SearchEngine
    from crux_mcp_server.server import AppContext

    cfg = load_config(
        config_path=config_path or _write_config(tmp_path),
        project_root=tmp_path,
    )
    index = scan(cfg)
    engine = SearchEngine()
    engine.build(index)
    return AppContext(config=cfg, memory_index=index, search_engine=engine)


def _register_tools(ctx):
    """Create a FastMCP server with all tools registered, return the server."""
    from fastmcp import FastMCP
    from crux_mcp_server.tools import discover_and_register

    server = FastMCP(name="test-server")
    discover_and_register(server, ctx)
    return server


def _get_tool_fn(server, tool_name: str):
    """Retrieve a tool's underlying function from the FastMCP server."""
    tool = asyncio.run(server.get_tool(tool_name))
    return tool.fn


def _write_tracker_with_total(tracking_dir: Path, slug: str, total: int) -> Path:
    """Write a tracker file using the totalReferences key the scanner expects."""
    tracking_dir.mkdir(parents=True, exist_ok=True)
    from datetime import date
    data = {
        "slug": slug,
        "totalReferences": total,
        "last_referenced": date.today().isoformat(),
        "strength": 1,
    }
    path = tracking_dir / f"{slug}.refs.yml"
    path.write_text(yaml.dump(data, default_flow_style=False), encoding="utf-8")
    return path


# ===================================================================
# 1. Config loading
# ===================================================================

class TestServerImportAndConfig:
    """Server module is importable and config loads correctly."""

    def test_config_module_importable(self):
        from crux_mcp_server.config import load_config, ServerConfig
        assert callable(load_config)

    def test_config_loads_from_file(self, tmp_path: Path):
        config_path = _write_config(tmp_path)
        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.enabled is True
        assert cfg.memories.storage.memories_dir == "memories"

    def test_config_defaults_without_file(self, tmp_path: Path):
        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=None, project_root=tmp_path)

        assert cfg.memories.enabled is False
        assert cfg.memories.storage.memories_dir == "memories"

    def test_config_flags_parsed(self, tmp_path: Path):
        cfg_data = {
            "platform": "cursor",
            "flags": [
                {"enableMemories": "true"},
                {"enableMemoryCompression": "true"},
            ],
            "cruxMemories": {
                "storage": {"memoriesDir": "mems"},
                "maxMemorySize": 500,
                "typePriority": MEMORY_TYPES,
            },
        }
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data), encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.enabled is True
        assert cfg.memories.compression is True
        assert cfg.memories.storage.memories_dir == "mems"
        assert cfg.memories.max_memory_size == 500

    def test_config_find_walks_upward(self, tmp_path: Path):
        _write_config(tmp_path)
        nested = tmp_path / "a" / "b" / "c"
        nested.mkdir(parents=True)

        from crux_mcp_server.config import _find_config
        found = _find_config(nested)
        assert found is not None
        assert found.exists()

    def test_config_reference_tracking(self, tmp_path: Path):
        config_path = _write_config(tmp_path)
        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.reference_tracking.enabled is True
        assert cfg.memories.reference_tracking.tracking_dir == ".crux/reference-tracking"


# ===================================================================
# 2. Frontmatter parsing
# ===================================================================

class TestFrontmatterParsing:
    """YAML frontmatter parser handles various edge cases."""

    def test_parse_standard_frontmatter(self):
        from crux_mcp_server.utils.frontmatter import parse

        text = textwrap.dedent("""\
            ---
            title: "Test Memory"
            type: "learning"
            strength: 5
            tags: [foo, bar]
            ---

            Body content here.
        """)
        result = parse(text)
        assert result.frontmatter["title"] == "Test Memory"
        assert result.frontmatter["type"] == "learning"
        assert result.frontmatter["strength"] == 5
        assert result.frontmatter["tags"] == ["foo", "bar"]
        assert "Body content here." in result.body

    def test_parse_no_frontmatter(self):
        from crux_mcp_server.utils.frontmatter import parse

        text = "Just plain text with no frontmatter."
        result = parse(text)
        assert result.frontmatter == {}
        assert result.body == text

    def test_parse_empty_frontmatter(self):
        from crux_mcp_server.utils.frontmatter import parse

        text = "---\n---\nBody only."
        result = parse(text)
        assert result.frontmatter == {}
        assert result.body == "Body only."

    def test_parse_malformed_yaml(self):
        from crux_mcp_server.utils.frontmatter import parse

        text = "---\n: : : broken\n---\nBody."
        result = parse(text)
        assert result.frontmatter == {}
        assert result.body == "Body."

    def test_extract_searchable_text(self):
        from crux_mcp_server.utils.frontmatter import extract_searchable_text

        fm = {"title": "My Title", "description": "A description", "tags": ["alpha", "beta"]}
        body = "Some body text."
        result = extract_searchable_text(fm, body)

        assert "My Title" in result
        assert "A description" in result
        assert "alpha" in result
        assert "beta" in result
        assert "Some body text." in result

    def test_extract_searchable_text_missing_fields(self):
        from crux_mcp_server.utils.frontmatter import extract_searchable_text

        result = extract_searchable_text({}, "Only body.")
        assert "Only body." in result


# ===================================================================
# 3. CRUX decompression
# ===================================================================

class TestCruxDecompress:
    """Lightweight CRUX decompression for memory bodies."""

    def test_is_compressed_positive(self):
        from crux_mcp_server.utils.crux_decompress import is_compressed

        assert is_compressed("⟦CRUX:memory\nsome stuff\n⟧") is True

    def test_is_compressed_negative(self):
        from crux_mcp_server.utils.crux_decompress import is_compressed

        assert is_compressed("Regular markdown body.") is False

    def test_decompress_expands_symbols(self):
        from crux_mcp_server.utils.crux_decompress import decompress

        text = "⟦CRUX:memory\nA→B\n¬C\n⟧"
        result = decompress(text)
        assert "leads to" in result
        assert "not" in result

    def test_decompress_expands_block_labels(self):
        from crux_mcp_server.utils.crux_decompress import decompress

        text = "⟦CRUX:memory\nΡ{purpose text}\nR{rule text}\n⟧"
        result = decompress(text)
        assert "[Purpose]" in result
        assert "[Rules]" in result

    def test_decompress_plain_text_passthrough(self):
        from crux_mcp_server.utils.crux_decompress import decompress

        result = decompress("No CRUX here, just text.")
        assert "No CRUX here" in result

    def test_decompress_all_symbols_mapped(self):
        from crux_mcp_server.utils.crux_decompress import SYMBOL_MAP

        for sym in ["→", "←", "¬", "⊤", "⊥", "∀", "∃", "⊕", "≻", "≺",
                     "⊲", "⊳", "∋", "»", "⊛", "Δ", "↑", "↓"]:
            assert sym in SYMBOL_MAP

    def test_decompress_qualified_block_label(self):
        from crux_mcp_server.utils.crux_decompress import decompress

        text = "⟦CRUX:memory\nR.validate{check stuff}\n⟧"
        result = decompress(text)
        assert "[Rules]" in result


# ===================================================================
# 4. Scanner / Indexer
# ===================================================================

class TestScanner:
    """Memory scanner builds correct index from filesystem."""

    def test_scanner_counts_by_type(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "core-one", mem_type="core")
        write_memory(mem_dir, "core-two", mem_type="core")
        write_memory(mem_dir, "learn-one", mem_type="learning")
        write_memory(mem_dir, "idea-one", mem_type="idea")

        from crux_mcp_server.config import load_config
        from crux_mcp_server.indexer.scanner import scan

        cfg = load_config(config_path=_write_config(tmp_path), project_root=tmp_path)
        index = scan(cfg)

        type_counts = Counter(e.type for e in index.entries)
        assert type_counts["core"] == 2
        assert type_counts["learning"] == 1
        assert type_counts["idea"] == 1
        assert len(index.entries) == 4

    def test_scanner_counts_compressed(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "plain-mem", mem_type="learning", compressed=False)
        write_memory(mem_dir, "crux-mem", mem_type="learning", compressed=True)

        from crux_mcp_server.config import load_config
        from crux_mcp_server.indexer.scanner import scan

        cfg = load_config(config_path=_write_config(tmp_path), project_root=tmp_path)
        index = scan(cfg)

        compressed = sum(1 for e in index.entries if e.file.endswith(".memory.crux.md"))
        uncompressed = sum(
            1 for e in index.entries
            if e.file.endswith(".memory.md") and not e.file.endswith(".crux.md")
        )
        assert compressed == 1
        assert uncompressed == 1

    def test_scanner_by_slug_lookup(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "my-insight", mem_type="core", body="insight body")

        ctx = _build_ctx(tmp_path)
        entry = ctx.memory_index.by_slug.get("my-insight")
        assert entry is not None
        assert entry.title == "My Insight"
        assert entry.type == "core"

    def test_scanner_by_file_lookup(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(mem_dir, "file-lookup", mem_type="learning")
        rel = str(path.relative_to(tmp_path))

        ctx = _build_ctx(tmp_path)
        entry = ctx.memory_index.by_file.get(rel)
        assert entry is not None
        assert entry.slug == "file-lookup"

    def test_scanner_slug_extraction(self):
        from crux_mcp_server.indexer.scanner import _extract_slug

        assert _extract_slug(Path("foo.memory.md")) == "foo"
        assert _extract_slug(Path("bar.memory.crux.md")) == "bar"
        assert _extract_slug(Path("baz.txt")) == "baz"

    def test_scanner_sort_order(self, tmp_path: Path):
        """Entries should be sorted by type priority, then strength desc."""
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "weak-core", mem_type="core", strength=1)
        write_memory(mem_dir, "strong-idea", mem_type="idea", strength=10)
        write_memory(mem_dir, "strong-core", mem_type="core", strength=5)
        write_memory(mem_dir, "redflag-item", mem_type="redflag", strength=3)

        ctx = _build_ctx(tmp_path)
        slugs = [e.slug for e in ctx.memory_index.entries]

        core_idx = [i for i, s in enumerate(slugs) if s in ("strong-core", "weak-core")]
        redflag_idx = [i for i, s in enumerate(slugs) if s == "redflag-item"]
        idea_idx = [i for i, s in enumerate(slugs) if s == "strong-idea"]

        assert max(core_idx) < min(redflag_idx), "core should come before redflag"
        assert max(redflag_idx) < min(idea_idx), "redflag should come before idea"

        core_entries = [(e.slug, e.strength) for e in ctx.memory_index.entries if e.type == "core"]
        assert core_entries[0][1] >= core_entries[1][1], "stronger core first"

    def test_scanner_reads_reference_counts(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "tracked-mem", mem_type="learning")

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        _write_tracker_with_total(tracking_dir, "tracked-mem", total=7)

        ctx = _build_ctx(tmp_path)
        entry = ctx.memory_index.by_slug["tracked-mem"]
        assert entry.references == 7

    def test_scanner_yaml_index_fallback(self, tmp_path: Path):
        """When frontmatter is sparse, scanner falls back to YAML index data."""
        mem_dir = tmp_path / "memories" / "learning"
        mem_dir.mkdir(parents=True)
        minimal = "---\ntype: learning\n---\nBody.\n"
        (mem_dir / "sparse.memory.md").write_text(minimal, encoding="utf-8")

        idx_dir = tmp_path / ".crux"
        idx_dir.mkdir(parents=True, exist_ok=True)
        idx_data = {
            "memories": [
                {
                    "slug": "sparse",
                    "title": "Fallback Title",
                    "description": "From YAML index",
                    "type": "learning",
                    "strength": 4,
                    "tags": ["yaml-tag"],
                }
            ]
        }
        (idx_dir / "memory-index.yml").write_text(
            yaml.dump(idx_data, default_flow_style=False), encoding="utf-8"
        )

        ctx = _build_ctx(tmp_path)
        entry = ctx.memory_index.by_slug["sparse"]
        assert entry.title == "Fallback Title"
        assert entry.description == "From YAML index"

    def test_scanner_empty_dir(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        assert len(ctx.memory_index.entries) == 0

    def test_scanner_skips_corrupt_file(self, tmp_path: Path):
        mem_dir = tmp_path / "memories" / "core"
        mem_dir.mkdir(parents=True)
        (mem_dir / "bad.memory.md").write_bytes(b"\x80\x81\x82")
        write_memory(tmp_path / "memories", "good", mem_type="core")

        ctx = _build_ctx(tmp_path)
        assert len(ctx.memory_index.entries) == 1
        assert ctx.memory_index.entries[0].slug == "good"


# ===================================================================
# 5. Search engine (TF-IDF)
# ===================================================================

class TestSearchEngine:
    """TF-IDF search engine returns relevant results."""

    def test_search_returns_relevant_results(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "python-patterns", mem_type="learning",
                     body="Python design patterns for large codebases",
                     tags=["python", "patterns"])
        write_memory(mem_dir, "rust-safety", mem_type="learning",
                     body="Rust memory safety and ownership model",
                     tags=["rust", "safety"])
        write_memory(mem_dir, "python-testing", mem_type="learning",
                     body="Python testing strategies with pytest",
                     tags=["python", "testing"])

        ctx = _build_ctx(tmp_path)
        results = ctx.search_engine.search("python patterns")

        assert len(results) >= 1
        slugs = [r.entry.slug for r in results]
        assert "python-patterns" in slugs
        assert results[0].entry.slug == "python-patterns"

    def test_search_empty_index(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        results = ctx.search_engine.search("anything")
        assert results == []

    def test_search_empty_query(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "some-mem", mem_type="core")

        ctx = _build_ctx(tmp_path)
        results = ctx.search_engine.search("")
        assert results == []

    def test_search_limit(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        for i in range(10):
            write_memory(mem_dir, f"testing-mem-{i}", mem_type="learning",
                         body=f"testing content about topic number {i}")

        ctx = _build_ctx(tmp_path)
        results = ctx.search_engine.search("testing content", limit=3)
        assert len(results) <= 3

    def test_search_scores_positive(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "relevance", mem_type="core", body="exact keyword match")

        ctx = _build_ctx(tmp_path)
        results = ctx.search_engine.search("keyword match")
        assert all(r.score > 0 for r in results)

    def test_search_case_insensitive(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "casing", mem_type="learning", body="Uppercase Keywords Here")

        ctx = _build_ctx(tmp_path)
        results_lower = ctx.search_engine.search("uppercase keywords")
        results_upper = ctx.search_engine.search("UPPERCASE KEYWORDS")
        assert len(results_lower) == len(results_upper)
        if results_lower:
            assert results_lower[0].score == results_upper[0].score


# ===================================================================
# 6. Tool registration
# ===================================================================

class TestToolRegistration:
    """Tool discovery and registration via discover_and_register."""

    def test_discover_registers_memory_module(self, tmp_path: Path):
        from crux_mcp_server.tools import discover_and_register
        from fastmcp import FastMCP

        ctx = _build_ctx(tmp_path)
        server = FastMCP(name="test")
        registered = discover_and_register(server, ctx)

        assert "memory" in registered

    def test_all_three_tools_registered(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)

        tools = asyncio.run(server.list_tools())
        tool_names = [t.name for t in tools]
        assert "memory-search" in tool_names
        assert "memory-read" in tool_names
        assert "memory-stats" in tool_names


# ===================================================================
# 7. memory-search tool (functional)
# ===================================================================

class TestMemorySearchTool:
    """Functional tests for the memory-search tool."""

    def test_search_returns_results(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "alpha-topic", mem_type="core",
                     body="Alpha topic discussion", tags=["alpha"])
        write_memory(mem_dir, "beta-topic", mem_type="learning",
                     body="Beta topic discussion", tags=["beta"])

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="alpha topic")
        assert isinstance(results, list)
        assert len(results) >= 1
        assert results[0]["slug"] == "alpha-topic"
        assert "score" in results[0]

    def test_search_type_filter(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "core-item", mem_type="core", body="shared keyword")
        write_memory(mem_dir, "idea-item", mem_type="idea", body="shared keyword")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="shared keyword", types=["core"])
        assert all(r["type"] == "core" for r in results)

    def test_search_tag_filter(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "tagged-a", mem_type="learning", body="content",
                     tags=["important"])
        write_memory(mem_dir, "tagged-b", mem_type="learning", body="content",
                     tags=["trivial"])

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="content", tags=["important"])
        slugs = [r["slug"] for r in results]
        assert "tagged-a" in slugs
        assert "tagged-b" not in slugs

    def test_search_min_strength_filter(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "weak", mem_type="learning", body="keyword", strength=1)
        write_memory(mem_dir, "strong", mem_type="learning", body="keyword", strength=10)

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="keyword", minStrength=5)
        slugs = [r["slug"] for r in results]
        assert "strong" in slugs
        assert "weak" not in slugs

    def test_search_agent_filter(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "base-mem", mem_type="core", body="shared keyword")
        write_memory(mem_dir, "agent-mem", mem_type="core", body="shared keyword",
                     agent_id="reviewer")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="shared keyword", agentId="reviewer")
        slugs = [r["slug"] for r in results]
        assert "agent-mem" in slugs
        assert "base-mem" not in slugs

    def test_search_include_content(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "with-body", mem_type="learning", body="detailed body text")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        without = search_fn(query="detailed body", includeContent=False)
        assert "content" not in without[0]

        with_content = search_fn(query="detailed body", includeContent=True)
        assert "content" in with_content[0]
        assert "detailed body text" in with_content[0]["content"]

    def test_search_limit_respected(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        for i in range(8):
            write_memory(mem_dir, f"repeat-{i}", mem_type="learning", body="repeat keyword")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="repeat keyword", limit=3)
        assert len(results) <= 3

    def test_search_result_schema(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "schema-check", mem_type="core", body="schema content",
                     tags=["check"], strength=3)

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        search_fn = _get_tool_fn(server, "memory-search")

        results = search_fn(query="schema content")
        assert len(results) >= 1
        r = results[0]
        required_keys = {"slug", "title", "description", "type", "strength", "tags", "file", "score"}
        assert required_keys.issubset(r.keys())


# ===================================================================
# 8. memory-read tool (functional)
# ===================================================================

class TestMemoryReadTool:
    """Functional tests for the memory-read tool."""

    def test_read_by_slug(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "readable", mem_type="core", body="Read me!")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(slugs=["readable"])
        assert len(results) == 1
        assert results[0]["slug"] == "readable"
        assert "Read me!" in results[0]["content"]
        assert "frontmatter" in results[0]

    def test_read_by_file(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(mem_dir, "by-file", mem_type="learning", body="File body")
        rel = str(path.relative_to(tmp_path))

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(files=[rel])
        assert len(results) == 1
        assert "File body" in results[0]["content"]

    def test_read_missing_slug(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(slugs=["nonexistent"])
        assert len(results) == 1
        assert results[0]["error"] == "not found"

    def test_read_missing_file(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(files=["memories/ghost.memory.md"])
        assert len(results) == 1
        assert "error" in results[0]

    def test_read_decompresses_crux(self, tmp_path: Path):
        mem_dir = tmp_path / "memories" / "core"
        mem_dir.mkdir(parents=True)

        content = textwrap.dedent("""\
            ---
            title: "Compressed Memory"
            type: "core"
            strength: 1
            tags: [test]
            compressed: true
            ---

            ⟦CRUX:memory
            R{A→B; ¬C}
            ⟧
        """)
        (mem_dir / "compressed-test.memory.crux.md").write_text(content, encoding="utf-8")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(slugs=["compressed-test"])
        assert len(results) == 1
        assert "⟦CRUX:" not in results[0]["content"]
        assert "leads to" in results[0]["content"]

    def test_read_multiple_slugs(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "first", mem_type="core", body="First body")
        write_memory(mem_dir, "second", mem_type="learning", body="Second body")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(slugs=["first", "second"])
        assert len(results) == 2
        slugs_returned = {r["slug"] for r in results}
        assert slugs_returned == {"first", "second"}

    def test_read_file_not_in_index_but_on_disk(self, tmp_path: Path):
        """Reading a file path that exists on disk but isn't indexed should still work."""
        mem_dir = tmp_path / "memories" / "core"
        mem_dir.mkdir(parents=True)

        orphan = mem_dir / "orphan.txt"
        orphan.write_text("---\ntitle: Orphan\n---\nOrphan body.", encoding="utf-8")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(files=["memories/core/orphan.txt"])
        assert len(results) == 1
        assert "Orphan body." in results[0]["content"]

    def test_read_frontmatter_preserved(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "fm-check", mem_type="core", strength=5,
                     tags=["tag1", "tag2"], body="Body here")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        read_fn = _get_tool_fn(server, "memory-read")

        results = read_fn(slugs=["fm-check"])
        fm = results[0]["frontmatter"]
        assert fm["type"] == "core"
        assert fm["strength"] == 5
        assert "tag1" in fm["tags"]


# ===================================================================
# 9. memory-stats tool (functional)
# ===================================================================

class TestMemoryStatsTool:
    """Functional tests for the memory-stats tool."""

    def test_stats_returns_correct_counts(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "s-core", mem_type="core")
        write_memory(mem_dir, "s-learn", mem_type="learning")
        write_memory(mem_dir, "s-crux", mem_type="idea", compressed=True)

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        stats_fn = _get_tool_fn(server, "memory-stats")

        stats = stats_fn()
        assert stats["totalMemories"] == 3
        assert stats["byType"]["core"] == 1
        assert stats["byType"]["learning"] == 1
        assert stats["byType"]["idea"] == 1
        assert stats["compressedCount"] == 1
        assert stats["uncompressedCount"] == 2
        assert stats["searchBackend"] == "tfidf"

    def test_stats_empty_corpus(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        stats_fn = _get_tool_fn(server, "memory-stats")

        stats = stats_fn()
        assert stats["totalMemories"] == 0
        assert stats["byType"] == {}
        assert stats["compressedCount"] == 0

    def test_stats_index_mtime(self, tmp_path: Path):
        (tmp_path / "memories").mkdir()
        idx_file = tmp_path / ".crux" / "memory-index.yml"
        idx_file.parent.mkdir(parents=True, exist_ok=True)
        idx_file.write_text("memories: []\n", encoding="utf-8")

        ctx = _build_ctx(tmp_path)
        server = _register_tools(ctx)
        stats_fn = _get_tool_fn(server, "memory-stats")

        stats = stats_fn()
        assert stats["indexLastModified"] is not None
        assert "T" in stats["indexLastModified"]


# ===================================================================
# 10. Agent scoping
# ===================================================================

class TestAgentScopingFilter:
    """Agent scoping filter with agentId parameter works correctly."""

    def test_scanner_tracks_agent_id(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "base-insight", mem_type="core")
        write_memory(mem_dir, "reviewer-insight", mem_type="core", agent_id="code-reviewer")

        ctx = _build_ctx(tmp_path)

        all_slugs = [e.slug for e in ctx.memory_index.entries]
        assert "base-insight" in all_slugs
        assert "reviewer-insight" in all_slugs

        agent_entries = [e for e in ctx.memory_index.entries if e.agent_id == "code-reviewer"]
        assert len(agent_entries) >= 1
        assert agent_entries[0].slug == "reviewer-insight"

        base_only = [e for e in ctx.memory_index.entries if e.slug == "base-insight"]
        assert all(e.agent_id is None for e in base_only)

    def test_agent_filter_excludes_other_agents(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "alpha-mem", mem_type="core", agent_id="alpha")
        write_memory(mem_dir, "beta-mem", mem_type="core", agent_id="beta")

        ctx = _build_ctx(tmp_path)

        alpha_only = [e for e in ctx.memory_index.entries if e.agent_id == "alpha"]
        assert len(alpha_only) == 1
        assert alpha_only[0].slug == "alpha-mem"

        beta_only = [e for e in ctx.memory_index.entries if e.agent_id == "beta"]
        assert len(beta_only) == 1
        assert beta_only[0].slug == "beta-mem"


# ===================================================================
# 11. Integration: create_server (no watcher)
# ===================================================================

class TestServerIntegration:
    """Integration test for the full server lifecycle."""

    def test_create_server_with_memories(self, tmp_path: Path, monkeypatch):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "int-test", mem_type="core", body="Integration test memory")
        config_path = _write_config(tmp_path)

        monkeypatch.chdir(tmp_path)

        from crux_mcp_server.server import create_server

        server, ctx = create_server(
            config_path=config_path,
            project_root=tmp_path,
        )

        try:
            assert len(ctx.memory_index.entries) == 1
            assert ctx.memory_index.by_slug["int-test"].body.strip() == "Integration test memory"

            tools = asyncio.run(server.list_tools())
            tool_names = [t.name for t in tools]
            assert "memory-search" in tool_names
            assert "memory-read" in tool_names
            assert "memory-stats" in tool_names
        finally:
            if ctx.watcher is not None:
                ctx.watcher.stop()

    def test_create_server_no_memories_dir(self, tmp_path: Path, monkeypatch):
        config_path = _write_config(tmp_path)
        monkeypatch.chdir(tmp_path)

        from crux_mcp_server.server import create_server
        server, ctx = create_server(
            config_path=config_path,
            project_root=tmp_path,
        )

        try:
            assert len(ctx.memory_index.entries) == 0
        finally:
            if ctx.watcher is not None:
                ctx.watcher.stop()


# ===================================================================
# 12. Watcher (unit-level)
# ===================================================================

class TestWatcher:
    """File watcher handler fires on relevant file events only."""

    def test_handler_fires_on_memory_file(self):
        from crux_mcp_server.indexer.watcher import MemoryFileHandler
        from unittest.mock import MagicMock

        callback = MagicMock()
        handler = MemoryFileHandler(callback, Path("/tmp/index.yml"))

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/project/memories/core/test.memory.md"

        handler.on_any_event(event)
        import time
        time.sleep(1.5)
        callback.assert_called_once()

    def test_handler_ignores_unrelated_file(self):
        from crux_mcp_server.indexer.watcher import MemoryFileHandler
        from unittest.mock import MagicMock

        callback = MagicMock()
        handler = MemoryFileHandler(callback, Path("/tmp/index.yml"))

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/project/README.md"

        handler.on_any_event(event)
        import time
        time.sleep(1.5)
        callback.assert_not_called()

    def test_handler_ignores_directories(self):
        from crux_mcp_server.indexer.watcher import MemoryFileHandler
        from unittest.mock import MagicMock

        callback = MagicMock()
        handler = MemoryFileHandler(callback, Path("/tmp/index.yml"))

        event = MagicMock()
        event.is_directory = True
        event.src_path = "/project/memories/"

        handler.on_any_event(event)
        import time
        time.sleep(1.5)
        callback.assert_not_called()
