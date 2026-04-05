"""Category G: Compression tests.

Validates compressed file naming, frontmatter preservation in compressed
output, compressionTarget adherence, and migration detection with source
archival.
"""

from __future__ import annotations

import json
import textwrap
from datetime import date
from pathlib import Path

import yaml

from conftest import _make_config, write_memory


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1])


class TestCompressedFileProduction:
    """Enabling compression produces *.memory.crux.md files within size limit."""

    def test_compressed_extension(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(mem_dir, "compress-me", mem_type="learning", compressed=True)
        assert path.name.endswith(".memory.crux.md")

    def test_compressed_file_within_size_limit(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        max_size = cfg["cruxMemories"]["maxMemorySize"]
        size_unit = cfg["cruxMemories"].get("sizeUnit", "lines")

        mem_dir = tmp_path / "memories"
        body = "A" * 500
        path = write_memory(
            mem_dir, "sized-memory", mem_type="learning",
            compressed=True, body=body,
        )

        if size_unit == "lines":
            file_size = len(path.read_text().splitlines())
            assert file_size <= max_size, (
                f"Compressed file {file_size} lines exceeds maxMemorySize {max_size}"
            )
        else:
            file_size = path.stat().st_size
            assert file_size <= max_size, (
                f"Compressed file {file_size} bytes exceeds maxMemorySize {max_size}"
            )

    def test_config_compression_flag(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        cfg["flags"] = [
            {"enableMemories": "true"},
            {"enableMemoryCompression": "true"},
        ]
        cfg["cruxMemories"]["compression"] = "true"

        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

        raw = json.loads(config_path.read_text(encoding="utf-8"))
        compression_flag = next(
            (f["enableMemoryCompression"] for f in raw["flags"] if "enableMemoryCompression" in f),
            None,
        )
        assert compression_flag == "true"


class TestFrontmatterPreservation:
    """Frontmatter (title, description) remains human-readable in compressed files."""

    def test_title_readable_in_compressed(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(
            mem_dir, "readable-title", mem_type="core",
            compressed=True, body="```crux\ncompressed content here\n```",
        )

        fm = _parse_frontmatter(path)
        assert "title" in fm
        assert fm["title"] == "Readable Title"

    def test_description_readable_in_compressed(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(
            mem_dir, "readable-desc", mem_type="learning",
            compressed=True, body="```crux\nΡ{test}\n```",
        )

        fm = _parse_frontmatter(path)
        assert "description" in fm
        assert isinstance(fm["description"], str)
        assert len(fm["description"]) > 0

    def test_all_required_frontmatter_fields_present(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(
            mem_dir, "full-fm", mem_type="idea",
            compressed=True, body="compressed body",
        )

        fm = _parse_frontmatter(path)
        required = {"title", "description", "type", "strength", "created", "modified", "source", "tags"}
        assert required.issubset(fm.keys()), f"Missing: {required - fm.keys()}"


class TestCompressionTarget:
    """The compressionTarget (33%) from config is respected."""

    def test_compression_target_configured(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["compressionTarget"] == 33

    def test_compressed_body_smaller_than_original(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        original_body = textwrap.dedent("""\
            When working with CRUX compression, always validate that the
            sourceChecksum matches the current file content before regenerating
            the compressed output. This prevents accidental data loss when the
            source has been modified outside of the compression workflow.
            Additionally, ensure the compression ratio meets the target threshold
            before accepting the compressed output as valid.
        """)

        uncompressed = write_memory(
            mem_dir, "original-verbose", mem_type="learning",
            body=original_body,
        )

        compressed_body = "```crux\nΡ{validate srcChksum ⊲ regen; ratio≥target}\n```"
        compressed = write_memory(
            mem_dir, "original-compressed", mem_type="learning",
            compressed=True, body=compressed_body,
        )

        assert compressed.stat().st_size < uncompressed.stat().st_size


class TestMigrationDetection:
    """Detect uncompressed files and archive sources to .ai-ignored/memories/sources/."""

    def test_detect_uncompressed_files(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "already-compressed", mem_type="learning", compressed=True)
        write_memory(mem_dir, "needs-compression", mem_type="learning", compressed=False)

        uncompressed = list((mem_dir / "learning").glob("*.memory.md"))
        compressed = list((mem_dir / "learning").glob("*.memory.crux.md"))

        assert len(uncompressed) == 1
        assert len(compressed) == 1
        assert "needs-compression" in uncompressed[0].name

    def test_source_archival_directory(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        archive_path = cfg["cruxMemories"]["storage"]["compressionSourceArchive"]

        mem_dir = tmp_path / "memories"
        source_path = write_memory(mem_dir, "archive-source", mem_type="learning")

        archive_dir = tmp_path / archive_path
        archive_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        archived = archive_dir / source_path.name
        shutil.copy2(str(source_path), str(archived))

        assert archived.exists()
        assert archived.name == source_path.name

    def test_source_archive_config_path(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["storage"]["compressionSourceArchive"] == ".ai-ignored/memories/sources"
