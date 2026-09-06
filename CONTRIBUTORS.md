# Contributing to CRUX Compress

![CRUX CI/CD and Hooks](crux-cicd-and-hooks.png)


Thank you for your interest in contributing to CRUX Compress! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Release Process](#release-process)
  - [Plugin System](#plugin-system)

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive experience for everyone.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/CRUX-Compress.git`
3. Add the upstream remote: `git remote add upstream https://github.com/zotoio/CRUX-Compress.git`
4. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Python >= 3.10
- `jq` for JSON processing (optional, used by some shell scripts)
- `bc` for calculations

### Installing Python Dependencies

```bash
# Eval test dependencies
pip install -r evals/requirements.txt

# MCP server (editable install — required for the test_l_mcp_server.py and
# test_m_config_validation.py suites to resolve `crux_mcp_server.*` imports)
pip install -e ./crux_mcp_server
```

### Authoring Agents and Commands

When writing new agents or commands under `.cursor/agents/` or `.cursor/commands/`:

- **Lazy-CRUX loading**: Do not unconditionally instruct agents to `Read CRUX.md` unless the agent's primary function involves CRUX notation. Use a conditional instruction (e.g. "If the task involves CRUX notation, read `CRUX.md`").
- **`context_manifest` honor block**: Include a `context_manifest` stanza near the top of each agent's load prompt. This prevents redundant re-reads of `AGENTS.md`, `CRUX.md`, and `.crux/crux-memories.json` when a parent agent has already loaded them. Example pattern: check for a `context_manifest` in the task prompt; if a file is marked `loaded`, do not re-read it.
- **Mode-scoped agents**: Each memory operation (`dream`, `rem`, `recall`, `remember`, `forget`) now has its own thin agent. Spawn the appropriate `crux-memory-<mode>` agent directly instead of routing through the deprecated `crux-cursor-memory-manager` dispatcher.
- **Source vs loadable**: Agent and command files follow the `<name>.source.mdx` (editable SoT) / `<name>.md` (Cursor-loadable, CRUX-compressed body) convention. Edit the `.source.mdx` and regenerate the `.md` loadable via `/crux-compress`.

## Testing

CRUX Compress uses [pytest](https://docs.pytest.org/) for all tests.

### Test Structure

```
evals/                              # All tests (pytest)
├── conftest.py                     # Shared fixtures and configuration
├── fixtures/                       # Test fixtures
│   └── sample-config.json
├── test_a_memory_crud.py           # Memory CRUD operations
├── test_b_dream_workflow.py        # Dream extraction workflow
├── test_c_rem_sleep.py             # REM sleep rebalancing
├── test_d_reference_tracking.py    # Reference tracking
├── test_e_memory_index.py          # Memory index building
├── test_f_type_transitions.py      # Type transition logic
├── test_g_compression.py           # Memory compression
├── test_h_agent_scoping.py         # Agent memory isolation
├── test_i_scope_ranking.py         # Scope ranking
├── test_k_session_hook.py          # Session start hook
├── test_l_mcp_server.py            # MCP server tools
├── test_m_config_validation.py     # Config validation
├── test_n_plugin_registry.py       # Plugin registry validation
├── test_q_meditate.py              # Meditate command eval
├── test_create_zip.py              # Distribution zip creation
├── test_crux_utils.py              # CRUX utility script
├── test_detect_hook.py             # File change detection hook
├── test_install.py                 # Installer script
├── test_test_runner.py             # Test runner script
├── requirements.txt                # pytest, pyyaml
└── USER_EVAL_CHECKLISTS.md         # Manual eval checklists

evals/sdk/tests/                    # TypeScript SDK eval tests
└── q-meditate.test.ts              # Meditate SDK eval

tests/fixtures/                     # Shared test fixture files
```

### Test Suites

| Test File | Script Under Test | Coverage |
|-----------|------------------|----------|
| `test_install.py` | `install.py` | CLI flags, version comparison, hooks merge, upsert |
| `test_crux_utils.py` | `crux-utils.py` | Token counting, checksums, compression ratio |
| `test_detect_hook.py` | `crux-detect-changes.py` | File filtering, queue management |
| `test_create_zip.py` | `create-crux-zip.py` | Zip contents, version matching, structure |
| `test_a_memory_crud.py` | Memory skills | Memory create, read, update, delete |
| `test_b_dream_workflow.py` | Dream extraction | Post-spec memory extraction workflow |
| `test_c_rem_sleep.py` | REM sleep | Promotion, demotion, archival |
| `test_d_reference_tracking.py` | Reference tracker | Usage tracking and strength sync |
| `test_e_memory_index.py` | Memory index | Index building and prioritisation |
| `test_f_type_transitions.py` | Type transitions | Type transition logic and promotion thresholds |
| `test_g_compression.py` | Memory compression | CRUX compression of memory bodies |
| `test_h_agent_scoping.py` | Agent scoping | Agent memory isolation and scope rules |
| `test_i_scope_ranking.py` | Scope ranking | Scope priority ranking logic |
| `test_k_session_hook.py` | Session hook | Memory nudge on session start |
| `test_l_mcp_server.py` | MCP server | MCP server tool validation |
| `test_m_config_validation.py` | Config validation | Memory configuration validation |
| `test_n_plugin_registry.py` | Plugin registry | Schema validation, `enabledByDefault` semantics |
| `test_q_meditate.py` | Meditate command | Meditation guide agent, skill delegation, mode gates |
| `test_r_crux_command_suite.py` | `/crux-test` / `run_crux_command_suite.py` | Pytest command-suite shim (deterministic + optional `llm_driven` scenarios) |
| `test_s_context_reduction.py` | Context token reduction | Lazy-CRUX enforcement, `context_manifest` honor, thin-agent split, `/crux-test` shim, compressed-primitive parity |
| `evals/sdk/tests/q-meditate.test.ts` | Meditate SDK | TypeScript SDK eval for meditate command |

### Running Tests

```bash
# Run all tests (bats + pytest)
python3 scripts/test.py

# Run all pytest tests
pytest evals/ -v

# Run a specific test file
pytest evals/test_install.py -v

# Run with short output
pytest evals/ --tb=short
```

### Writing New Tests

1. Create a new `test_*.py` file in the `evals/` directory
2. Use pytest fixtures (especially `tmp_path`) for test isolation
3. Use `conftest.py` helpers for creating memory/tracker fixtures
4. Name tests descriptively: `test_handles_edge_case_correctly`

Example:

```python
def test_script_handles_empty_input(tmp_path):
    result = subprocess.run(["./my-script.sh", ""], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Error: empty input" in result.stderr
```

### CI Integration

Tests run automatically on:
- Push to `main` branch
- Push to `feature/**` branches
- Pull requests to `main`

The CI pipeline (`.github/workflows/test.yml`) runs:
1. pytest suite
2. Zip creation validation
3. Install script syntax check
4. ShellCheck linting
5. Python eval tests (pytest)

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

| Prefix | Version Bump | Example |
|--------|-------------|---------|
| `fix:` | Patch (0.0.x) | `fix: correct token counting for unicode` |
| `feat:` | Minor (0.x.0) | `feat: add compression ratio display` |
| `feat!:` or `BREAKING CHANGE` | Major (x.0.0) | `feat!: change output format` |

Other prefixes (`docs:`, `chore:`, `test:`, `refactor:`, `style:`) trigger a patch bump.

### Examples

```bash
# Bug fix (1.0.0 → 1.0.1)
git commit -m "fix: handle empty files gracefully"

# New feature (1.0.1 → 1.1.0)
git commit -m "feat: add --verbose flag to install script"

# Breaking change (1.1.0 → 2.0.0)
git commit -m "feat!: change CRUX notation syntax

BREAKING CHANGE: The arrow operator → is now required"
```

## Pull Request Process

1. **Update tests**: Add or update tests for any new functionality
2. **Run tests locally**: Ensure all tests pass with `pytest evals/ -v`
3. **Check linting**: Run ShellCheck on your scripts
4. **Update documentation**: Update README.md if you've changed functionality
5. **Descriptive PR title**: Use conventional commit format
6. **Link issues**: Reference any related issues with "Fixes #123" or "Relates to #456"

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] ShellCheck passes
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow conventional commits
- [ ] No merge conflicts with main

## Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the problem
2. **Steps to reproduce**: Minimal steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version (if relevant)
6. **Logs/Output**: Any error messages or relevant output

## Release Process

Releases are fully automated via GitHub Actions. The CI/CD pipeline ensures that version bumps only occur when tests pass and release-relevant files change.

### CI/CD Flow

```
Push to main
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Test Workflow (.github/workflows/test.yml)                     │
│  ├─ Run pytest suite                                            │
│  ├─ Validate zip creation                                       │
│  ├─ Check install script syntax                                 │
│  └─ Run ShellCheck linting                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ success
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Version Bump Workflow (.github/workflows/version-bump.yml)     │
│  ├─ Read .crux/dist-manifest.json for release-relevant paths    │
│  │   (skips if only docs, tests, or non-release files changed) │
│  ├─ Analyze commit message for bump type (feat→minor, fix→patch)│
│  └─ Update .crux/crux.json and CRUX.md, commit with [skip ci]   │
└────────────────────────────┬────────────────────────────────────┘
                             │ Version changed
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Release Workflow (.github/workflows/release.yml)               │
│  ├─ Run scripts/create-crux-zip.py (single build step):         │
│  │   ├─ Update .crux/dist-manifest.json (canonical file list)   │
│  │   ├─ Generate checksums → .crux/crux-release-files.json      │
│  │   └─ Build distribution zip (CRUX-Compress-vX.Y.Z.zip)       │
│  ├─ Commit updated manifests                                    │
│  ├─ Create GitHub Release with tag vX.Y.Z                       │
│  ├─ Generate release notes from commits                         │
│  └─ Update CHANGELOG.md and commit                              │
└─────────────────────────────────────────────────────────────────┘
```

### Release-Relevant Files

Version bumps only occur when these files change. The file list is read from `.crux/dist-manifest.json` (generated by `scripts/create-crux-zip.py`, the single source of truth for distribution contents):

| File/Path | Description |
|-----------|-------------|
| `CRUX.md` | Core specification |
| `AGENTS.md` | Agent awareness block |
| `.crux/crux.json` | Version metadata |
| `.crux/crux-release-files.json` | Release manifest with checksums |
| `.cursor/hooks.json` | Hook configuration |
| `.cursor/agents/crux/crux-cursor-rule-manager.md` | Rule manager agent definition |
| `.cursor/agents/crux/crux-cursor-memory-manager.md` | Memory manager dispatcher (deprecated — see thin agents) |
| `.cursor/agents/crux/crux-memory-dream.md` | Dream mode agent |
| `.cursor/agents/crux/crux-memory-rem.md` | REM Sleep mode agent |
| `.cursor/agents/crux/crux-memory-recall.md` | Recall mode agent |
| `.cursor/agents/crux/crux-memory-remember.md` | Remember mode agent |
| `.cursor/agents/crux/crux-memory-forget.md` | Forget mode agent |
| `.cursor/agents/crux/crux-cursor-meditation-guide.md` | Meditation guide agent definition |
| `.cursor/commands/crux/crux-compress.md` | Compression command |
| `.cursor/commands/crux/crux-dream.md` | Dream extraction command |
| `.cursor/commands/crux/crux-recall.md` | Memory query command |
| `.cursor/commands/crux/crux-forget.md` | Memory forget command |
| `.cursor/commands/crux/crux-remember.md` | Ad-hoc memory creation command |
| `.cursor/commands/crux/crux-meditate.md` | Recursive exploration command |
| `.cursor/hooks/crux-detect-changes.py` | File change detection hook |
| `.cursor/hooks/crux-session-start.py` | Session start hook |
| `.cursor/rules/crux/_CRUX-RULE.mdc` | Always-applied rule |
| `.cursor/rules/crux/crux-memories-integration.crux.mdc` | Memory integration rule |
| `.cursor/skills/crux/crux-utils/**` | Utility skill |
| `.cursor/skills/crux/crux-skill-memory-*/**` | Memory skills (CRUD, compress, extract, index, rebalance, reference-tracker) |

Changes to other files (README, tests, examples, scripts) do **not** trigger releases.

### Memory System Components

Memory tooling (agent, commands, skills, rule) is included in the distribution zip and always installed. Runtime data is repo-local and created via `--with-memories`:

| Path | Distributed? | Purpose |
|------|:---:|---------|
| `.cursor/agents/crux/crux-cursor-memory-manager.md` | Yes | Memory lifecycle dispatcher (deprecated — thin agents below) |
| `.cursor/agents/crux/crux-memory-dream.md` | Pending dist update | Dream mode agent |
| `.cursor/agents/crux/crux-memory-rem.md` | Pending dist update | REM Sleep mode agent |
| `.cursor/agents/crux/crux-memory-recall.md` | Pending dist update | Recall mode agent |
| `.cursor/agents/crux/crux-memory-remember.md` | Pending dist update | Remember mode agent |
| `.cursor/agents/crux/crux-memory-forget.md` | Pending dist update | Forget mode agent |
| `.cursor/agents/crux/templates/recall-canvas.tsx.md` | Pending dist update | Canvas structural template (Recall `--total`) |
| `.cursor/agents/crux/crux-cursor-meditation-guide.md` | Yes | Meditation guide agent definition |
| `.cursor/commands/crux/crux-dream.md` | Yes | Dream extraction command |
| `.cursor/commands/crux/crux-recall.md` | Yes | Memory query command |
| `.cursor/commands/crux/crux-forget.md` | Yes | Memory forget command |
| `.cursor/commands/crux/crux-remember.md` | Yes | Ad-hoc memory creation command |
| `.cursor/commands/crux/crux-meditate.md` | Yes | Recursive exploration command |
| `.cursor/skills/crux/crux-skill-memory-*/` | Yes | Memory skills (CRUD, extract, rebalance, compress, index, reference-tracker) |
| `.cursor/skills/crux/crux-skill-memory-meditation-research/` | Yes | Research-mode Phases A–G recursion skill |
| `.cursor/skills/crux/crux-skill-memory-meditation-quick/` | Yes | Quick-mode parallel fan-out skill |
| `.cursor/skills/crux/crux-skill-memory-meditation-ensemble/` | Yes | Ensemble Aggregation skill |
| `.cursor/skills/crux/crux-skill-memory-meditation-review/` | Yes | Adversarial review skill |
| `.cursor/skills/crux/crux-skill-memory-meditation-report/` | Yes | HTML+PDF report generation skill |
| `.cursor/skills/crux/crux-skill-memory-meditation-coordination/` | Yes | File coordination primitives skill |
| `.cursor/rules/crux-memories-integration.crux.mdc` | Yes | Memory integration rule |
| `.crux/crux-memories.json` | No | Memory system configuration and feature flags (created by `--with-memories`) |
| `.crux/memory-index.yml` | No | Prioritised memory index for agent discovery |
| `memories/` | No | Memory file storage (by type: `core/`, `learning/`, `redflag/`, `goal/`, `idea/`) |
| `memories/agents/` | No | Agent-scoped memory storage |
| `crux_mcp_server/` | Separate zip | MCP server for semantic memory search (`CRUX-MCP-Server-v*.zip`) |
| `evals/` | No | Python-based eval tests for memory workflows |

### Plugin System

CRUX Compress supports an optional plugin architecture that extends the compression workflow with lifecycle hooks.

#### Registry Structure

Plugins are declared in `.crux/plugins/registry.json`:

```json
{
  "plugins": {
    "<plugin-name>": {
      "description": "What the plugin does",
      "hooks": ["beforeCompress", "afterCompress"],
      "failClosed": false,
      "enabledByDefault": false
    }
  }
}
```

Each plugin entry requires:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Human-readable purpose |
| `hooks` | string[] | Lifecycle hooks the plugin binds to |
| `failClosed` | boolean | Whether plugin failure blocks compression |
| `enabledByDefault` | boolean | Whether the plugin loads without explicit `--plugin` flag |

#### Hook Lifecycle

Plugins execute at predefined points in the compression flow:

1. `beforeFetch` — URL sources only, before content is fetched
2. `beforeCompress` — after source resolution, before compression begins
3. *Base compression* (core workflow)
4. `afterCompress` — after CRUX output is generated
5. *Semantic validation* (core workflow)
6. `afterValidate` — after validation produces a confidence score

#### Default Plugin Loading (`enabledByDefault`)

Plugins with `enabledByDefault: true` load automatically when no `--plugin` flags are given. Users can opt out with `--no-plugin <name>`. When explicit `--plugin` flags are present, only the named plugins load (defaults are not implicitly added).

#### Adding a New Plugin

1. Add an entry to `.crux/plugins/registry.json` with the required fields
2. Create a spec file at `.crux/plugins/<plugin-name>.md` documenting the plugin's behavior, inputs, and outputs for each hook
3. Update the command spec (`.cursor/commands/crux-compress.md`) and agent spec (`.cursor/agents/crux-cursor-rule-manager.md`) if the plugin requires behavioral changes
4. Add tests in `evals/` validating the registry entry and plugin behavior
5. Use `compression-level` (`.crux/plugins/compression-level.md`) as the canonical reference implementation

### Manual Version Bump

If you need to force a version bump:

1. Go to **Actions** → **Version Bump** workflow
2. Click **Run workflow**
3. Select bump type: `patch`, `minor`, or `major`
4. Click **Run workflow**

### Version Bump Rules

| Commit Prefix | Version Bump | Example |
|---------------|-------------|---------|
| `fix:` | Patch (0.0.x) | `fix: correct token counting` |
| `feat:` | Minor (0.x.0) | `feat: add new operator` |
| `feat!:` or `BREAKING CHANGE` | Major (x.0.0) | `feat!: change syntax` |
| Other (`docs:`, `chore:`, etc.) | Patch (0.0.x) | `docs: update README` |

## Questions?

Feel free to open an issue for questions or discussions about contributions.
