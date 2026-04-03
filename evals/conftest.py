"""Shared fixtures for CRUX memory system eval tests."""

from __future__ import annotations

import json
import textwrap
from datetime import date
from pathlib import Path

import pytest
import yaml

MEMORY_TYPES = ["core", "redflag", "goal", "learning", "idea", "archived"]


def _make_config(
    tmp_path: Path,
    *,
    memories_dir: str = "memories",
    agent_memories_dir: str = "memories/agents",
    archive_dir: str = ".ai-ignored/executed",
    index_file: str = ".crux/memory-index.yml",
    tracking_dir: str = ".crux/reference-tracking",
    max_memory_size: int = 2048,
    max_candidate_facts: int = 5,
    max_references_stored: int = 10,
    demote_days: int = 90,
    archive_days: int = 180,
) -> dict:
    """Return a config dict with paths rooted under *tmp_path*."""
    return {
        "platform": "cursor",
        "flags": [
            {"enableMemories": "true"},
            {"enableMemoryCompression": "false"},
        ],
        "cruxMemories": {
            "enabled": "true",
            "compression": "false",
            "storage": {
                "memoriesDir": memories_dir,
                "agentMemoriesDir": agent_memories_dir,
                "archiveDir": archive_dir,
                "compressionSourceArchive": ".ai-ignored/memories/sources",
                "indexFile": index_file,
            },
            "maxMemorySize": max_memory_size,
            "compressionTarget": 33,
            "unitOfWork": "plan",
            "dream": {
                "maxCandidateFacts": max_candidate_facts,
                "maxUnrelatedChanges": 50,
                "stateFile": "_execution-state.yml",
                "workDir": "plans",
                "summaryPattern": "dream-{slug}-{yyyymmdd}.md",
            },
            "typePriority": MEMORY_TYPES,
            "typeTransitions": {
                "idea": {"promoteAt": 5, "promoteTo": "learning"},
                "learning": {"promoteAt": 15, "promoteTo": "core"},
                "redflag": {"promoteAt": 10, "promoteTo": "core"},
                "core": {"promoteAt": None},
                "goal": {"promoteAt": None},
            },
            "demoteAfterDaysUnreferenced": demote_days,
            "archiveAfterDaysUnreferenced": archive_days,
            "referenceTracking": {
                "enabled": True,
                "trackingDir": tracking_dir,
                "indicateInOutput": True,
                "indicatorFormat": "[memory:{title}]",
                "promotionToRuleThreshold": 30,
                "maxReferencesStored": max_references_stored,
            },
            "scopeRanking": ["base", "agents", "shared"],
            "scopes": {
                "base": {"memoriesDir": memories_dir, "readonly": False},
                "agents": {
                    "memoriesDir": f"{agent_memories_dir}/{{agent-id}}",
                    "readonly": False,
                    "writeOnlyDuringDream": True,
                    "boostSameType": True,
                },
                "shared": [],
            },
        },
    }


@pytest.fixture()
def tmp_memories_dir(tmp_path: Path) -> Path:
    """Create a temp directory with the full memory type subdirectory structure."""
    mem_root = tmp_path / "memories"
    for t in MEMORY_TYPES:
        (mem_root / t).mkdir(parents=True, exist_ok=True)
    (mem_root / "agents" / "code-reviewer").mkdir(parents=True, exist_ok=True)
    return mem_root


@pytest.fixture()
def sample_config(tmp_path: Path) -> Path:
    """Generate a valid .crux/crux-memories.json under tmp_path and return its path."""
    crux_dir = tmp_path / ".crux"
    crux_dir.mkdir(parents=True, exist_ok=True)

    cfg = _make_config(tmp_path)
    config_path = crux_dir / "crux-memories.json"
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return config_path


@pytest.fixture()
def sample_memory_file(tmp_memories_dir: Path) -> Path:
    """Create a sample memory file with valid frontmatter in the learning directory."""
    today = date.today().isoformat()
    content = textwrap.dedent(f"""\
        ---
        title: "Always validate checksums before overwriting"
        description: "Source files can drift. Recompute and compare sourceChecksum before regenerating."
        type: "learning"
        strength: 1
        created: {today}
        modified: {today}
        source: "20260403-crux-memories"
        tags: [crux, validation, checksums]
        ---

        Detailed explanation of why checksum validation matters.
    """)
    target = tmp_memories_dir / "learning" / "validate-checksums.memory.md"
    target.write_text(content, encoding="utf-8")
    return target


@pytest.fixture()
def sample_tracker_file(tmp_path: Path) -> Path:
    """Create a sample .refs.yml tracker file."""
    tracking_dir = tmp_path / ".crux" / "reference-tracking"
    tracking_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    data = {
        "slug": "validate-checksums",
        "references": 3,
        "last_referenced": today,
        "strength": 1,
        "recent_references": [
            {"plan": "20260403-crux-memories", "count": 2, "last": today},
            {"plan": "20260402-other-plan", "count": 1, "last": today},
        ],
    }
    tracker_path = tracking_dir / "validate-checksums.refs.yml"
    tracker_path.write_text(
        "# Managed by crux-skill-memory-reference-tracker\n"
        + yaml.dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    return tracker_path


def write_memory(
    base_dir: Path,
    slug: str,
    *,
    mem_type: str = "learning",
    strength: int = 1,
    created: str | None = None,
    modified: str | None = None,
    source: str = "test-plan",
    tags: list[str] | None = None,
    body: str = "",
    agent_id: str | None = None,
    compressed: bool = False,
) -> Path:
    """Helper to write a memory file with valid frontmatter.

    Returns the path of the created file.
    """
    today = date.today().isoformat()
    created = created or today
    modified = modified or today
    tags = tags or ["test"]

    fm = {
        "title": slug.replace("-", " ").title(),
        "description": f"Description for {slug}",
        "type": mem_type,
        "strength": strength,
        "created": created,
        "modified": modified,
        "source": source,
        "tags": tags,
    }

    ext = ".memory.crux.md" if compressed else ".memory.md"
    if agent_id:
        target_dir = base_dir / "agents" / agent_id / mem_type
    else:
        target_dir = base_dir / mem_type
    target_dir.mkdir(parents=True, exist_ok=True)

    path = target_dir / f"{slug}{ext}"
    content = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n"
    if body:
        content += "\n" + body + "\n"
    path.write_text(content, encoding="utf-8")
    return path


def write_tracker(
    tracking_dir: Path,
    slug: str,
    *,
    references: int = 1,
    strength: int = 1,
    last_referenced: str | None = None,
    recent_references: list[dict] | None = None,
) -> Path:
    """Helper to write a tracker .refs.yml file. Returns the path."""
    today = date.today().isoformat()
    last_referenced = last_referenced or today

    data = {
        "slug": slug,
        "references": references,
        "last_referenced": last_referenced,
        "strength": strength,
        "recent_references": recent_references
        or [{"plan": "test-plan", "count": references, "last": last_referenced}],
    }
    tracking_dir.mkdir(parents=True, exist_ok=True)
    path = tracking_dir / f"{slug}.refs.yml"
    path.write_text(
        "# Managed by crux-skill-memory-reference-tracker\n"
        + yaml.dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    return path
