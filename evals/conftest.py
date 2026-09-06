"""Shared fixtures for CRUX memory system eval tests."""

from __future__ import annotations

import json
import sys
import textwrap
from datetime import date
from pathlib import Path

import pytest
import yaml

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_MCP_PKG_DIR = _PROJECT_ROOT / "crux_mcp_server"
if str(_MCP_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_MCP_PKG_DIR))

MEMORY_TYPES = ["core", "redflag", "goal", "learning", "idea", "archived"]

# ---------------------------------------------------------------------------
# Meditation artifact helpers (used by test_q_meditate.py new assertion classes)
# ---------------------------------------------------------------------------

MEDITATION_SKILL_NAMES = [
    "research",
    "quick",
    "ensemble",
    "review",
    "report",
    "coordination",
]

MEDITATION_SKILL_DIRS = [
    f"crux-skill-memory-meditation-{n}" for n in MEDITATION_SKILL_NAMES
]


def _prefer_sot(*candidates: Path) -> Path | None:
    """Prefer editable SoT (`.source.mdx` / `SKILL.mdx`) over generated loadable when present.

    Registration model: commands/agents edit `<name>.source.mdx` and ship compressed
    `<name>.md`; skills edit `SKILL.mdx` → compressed `SKILL.md`. Prose-contract evals
    must assert against SoT, not the CRUX loadable body.
    """
    for p in candidates:
        if p.exists():
            return p
    return None


def _read_meditation_artifact(kind: str, name: str | None = None) -> str:
    """Read a meditation source file by kind and optional name.

    kind:
        "command"               → crux-meditate.source.mdx (preferred) or crux-meditate.md
        "guide_agent"           → crux-cursor-meditation-guide.source.mdx (preferred) or .md
        "memory_manager"        → .cursor/agents/crux-cursor-memory-manager.md
        "skill"                 → SKILL.mdx (preferred) or SKILL.md under meditation skill dir
        "all_meditation_sources" → concatenation of command + guide_agent + all skills
    """
    root = _PROJECT_ROOT
    if kind == "command":
        p = _prefer_sot(
            root / ".cursor" / "commands" / "crux-meditate.source.mdx",
            root / ".cursor" / "commands" / "crux-meditate.md",
        )
        return p.read_text(encoding="utf-8") if p else ""
    if kind == "guide_agent":
        p = _prefer_sot(
            root / ".cursor" / "agents" / "crux-cursor-meditation-guide.source.mdx",
            root / ".cursor" / "agents" / "crux-cursor-meditation-guide.md",
        )
        return p.read_text(encoding="utf-8") if p else ""
    if kind == "memory_manager":
        p = root / ".cursor" / "agents" / "crux-cursor-memory-manager.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""
    if kind == "skill":
        if not name:
            raise ValueError("name is required for kind='skill'")
        skill_dir = f"crux-skill-memory-meditation-{name}"
        base = root / ".cursor" / "skills" / skill_dir
        p = _prefer_sot(base / "SKILL.mdx", base / "SKILL.md")
        return p.read_text(encoding="utf-8") if p else ""
    if kind == "all_meditation_sources":
        parts = [_read_meditation_artifact("command")]
        parts.append(_read_meditation_artifact("guide_agent"))
        for n in MEDITATION_SKILL_NAMES:
            parts.append(_read_meditation_artifact("skill", n))
        return "\n".join(parts)
    raise ValueError(f"Unknown kind: {kind!r}")


def _make_config(
    tmp_path: Path,
    *,
    memories_dir: str = "memories",
    agent_memories_dir: str = "memories/agents",
    archive_dir: str = ".ai-ignored/executed",
    index_file: str = ".crux/memory-index.yml",
    tracking_dir: str = ".crux/reference-tracking",
    compression_min_lines: int = 500,
    max_memory_size: int = 1000,
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
            "sizeUnit": "lines",
            "compressionMinLines": compression_min_lines,
            "maxMemorySize": max_memory_size,
            "compressionTarget": 33,
            "unitOfWork": "spec",
            "dream": {
                "maxCandidateFacts": max_candidate_facts,
                "maxUnrelatedChanges": 50,
                "stateFile": "_execution-state.yml",
                "workDir": "specs",
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
            {"spec": "20260403-crux-memories", "count": 2, "last": today},
            {"spec": "20260402-other-spec", "count": 1, "last": today},
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
    source: str = "test-spec",
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
        or [{"spec": "test-spec", "count": references, "last": last_referenced}],
    }
    tracking_dir.mkdir(parents=True, exist_ok=True)
    path = tracking_dir / f"{slug}.refs.yml"
    path.write_text(
        "# Managed by crux-skill-memory-reference-tracker\n"
        + yaml.dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    return path


# ---------------------------------------------------------------------------
# Meditation working-directory fixtures (plan §5.2 / §5.3)
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_meditation_working_dir(tmp_path: Path) -> Path:
    """Create a temp meditation working directory pre-populated with stub artefacts."""
    today = date.today().strftime("%Y%m%d")
    work_dir = tmp_path / "meditations" / f"{today}-sample-topic"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "facet-registry.yml").write_text("# facet registry stub\n", encoding="utf-8")
    (work_dir / "citations-index.yml").write_text("# citations index stub\n", encoding="utf-8")
    (work_dir / "facets.md").write_text("---\ntitle: sample-topic\n---\n", encoding="utf-8")
    return work_dir


@pytest.fixture()
def crux_llm_eval():
    """Fixture for LLM-driven CRUX validation assertions.

    Provides an assertion callable suitable for ``@pytest.mark.llm_driven`` tests.

    Skip path (CI default):
        When the ``CRUX_LLM_EVAL`` environment variable is not set, every call to
        the returned callable immediately skips the test with a clear message that
        explains how to enable live assertions.  This ensures the test never
        silently passes without LLM involvement.

    Assertion path (when CRUX_LLM_EVAL=1):
        Call the fixture with a structured result dict returned by a real LLM
        invocation (e.g. via crux-cursor-rule-manager).  The callable enforces:
          - ``result["confidence"]`` is a float in [0.0, 1.0] and >= min_confidence
          - ``result["passed"]`` is True

    Expected result shape::

        {
            "confidence": 0.87,   # 0.0–1.0 float; ≥ min_confidence required
            "passed": True,       # overall pass/fail from LLM
            "notes": "...",       # free-form explanation from LLM (optional)
        }

    Usage in a test::

        def test_llm_validates_crux(self, crux_llm_eval):
            # Replace None with your actual LLM invocation result
            llm_result = None  # e.g. invoke_crux_cursor_rule_manager(crux_content)
            crux_llm_eval(llm_result, min_confidence=0.80)

    To wire the live LLM path: set ``CRUX_LLM_EVAL=1``, replace the ``None``
    placeholder in each test with a real LLM call, and pass its returned dict here.
    """
    import os

    llm_enabled = os.environ.get("CRUX_LLM_EVAL", "").lower() in ("1", "true", "yes")

    def _evaluate(result: dict | None, *, min_confidence: float = 0.80) -> None:
        """Assert on a structured LLM result, or skip when LLM is not available.

        Args:
            result: Structured LLM result dict (see fixture docstring), or None.
                    When None and CRUX_LLM_EVAL=1, the test fails with an actionable
                    message prompting the caller to wire up the live LLM call.
            min_confidence: Minimum acceptable confidence (default 0.80).
        """
        if not llm_enabled:
            pytest.skip(
                "LLM eval disabled; set CRUX_LLM_EVAL=1 to activate live model assertions "
                f"(confidence >= {min_confidence:.0%} required). "
                "Wire up LLM invocation by replacing the None placeholder in each test."
            )
        if result is None:
            pytest.fail(
                "CRUX_LLM_EVAL=1 is set but no LLM result was provided. "
                "Replace the None placeholder with a real LLM invocation that returns "
                '{"confidence": float, "passed": bool, "notes": str}.'
            )
        if not isinstance(result, dict):
            pytest.fail(f"crux_llm_eval expected a dict, got {type(result).__name__}: {result!r}")
        confidence = float(result.get("confidence", 0))
        assert confidence >= min_confidence, (
            f"LLM confidence {confidence:.0%} is below threshold {min_confidence:.0%}. "
            f"Notes: {result.get('notes', 'none provided')}"
        )
        assert result.get("passed", False), (
            f"LLM validation did not pass (confidence={confidence:.0%}). "
            f"Notes: {result.get('notes', 'none provided')}"
        )

    return _evaluate


@pytest.fixture()
def sample_init_suggestions_yml(tmp_path: Path, request: pytest.FixtureRequest) -> Path:
    """Create an init-suggestions-{ts}.yml fixture with the canonical 4-treatment schema.

    Parameterise via ``pytest.mark.parametrize`` or ``request.param`` to supply a custom
    list of treatment strings.  Defaults to all four canonical modes.
    """
    treatments: list[str] = getattr(
        request,
        "param",
        ["skip", "additional_facet", "report_section_only", "additional_facet_AND_section"],
    )
    ts = date.today().strftime("%Y%m%d%H%M%S")
    data = {
        "additional_focus_areas": [
            {
                "title": f"Focus area — {t}",
                "treatment": t,
                "resulting_section_id": f"section-{t.replace('_', '-')}",
                "resulting_branch_index": None,
                "custom_report_section_title": f"Custom section for {t}",
            }
            for t in treatments
        ],
        "confirmed_sections": [],
        "confirmed_visualisations": [],
    }
    p = tmp_path / f"init-suggestions-{ts}.yml"
    p.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False), encoding="utf-8")
    return p
