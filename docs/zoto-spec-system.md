# Setting up `zoto-spec-system` in this repository

This repo's existing specs (e.g. `specs/20260406-crux-forget/`, `specs/20260425-crux-recall/`) follow the [`zoto-spec-system`](https://github.com/zotoio/zoto-agents/tree/main/plugins/zoto-spec-system) workflow — the structured **create → judge → execute** Cursor plugin published in [`zotoio/zoto-agents`](https://github.com/zotoio/zoto-agents).

The plugin itself is not vendored into this repo. This guide explains the small amount of repo-side wiring that is checked in and how a developer enables the slash commands (`/zoto-spec-create`, `/zoto-spec-judge`, `/zoto-spec-execute`).

## What lives in this repository

| Path | Purpose |
|------|---------|
| `.zoto-spec-system/config.json` | Plugin configuration (unitOfWork, specsDir, hook settings, memory extension) |
| `specs/` | Durable spec directories: `[yyyymmdd]-[feature-name]/` with index, subtasks, assessment, execution report |
| `specs/current/` | `workDir` inbox watched by the session-start hook (drop rough notes here) |
| `.cursor/rules/spec-agent-allocation.md` | Always-applied rule that maps subtasks to CRUX agents instead of `generalPurpose` |
| `AGENTS.md` → "Spec Execution — Agent Allocation" | Same allocation table, surfaced for agents that read AGENTS.md |
| `.github/workflows/test.yml` | Conditional pytest step `plugins/zoto-spec-system/tests/` (only runs if the plugin is vendored) |

## Installing the plugin

The plugin ships through Cursor's plugin marketplace. From inside Cursor:

```bash
cursor plugin install zoto-spec-system
```

After install, restart Cursor (or reload the window) so it picks up the new commands, agents, skills, and hook.

### Manual install (optional)

If you prefer to vendor the plugin into this repo (for example to pin a version or to satisfy the conditional CI step in `.github/workflows/test.yml`), clone the source under `plugins/zoto-spec-system/` and follow the build instructions in [`zoto-agents/README.md`](https://github.com/zotoio/zoto-agents/blob/main/README.md):

```bash
git clone https://github.com/zotoio/zoto-agents.git /tmp/zoto-agents
cp -R /tmp/zoto-agents/plugins/zoto-spec-system plugins/
cd plugins/zoto-spec-system && pnpm install && pnpm build && pnpm test
```

> Following the workspace user rule, prefer `yarn` if you bring this into a yarn-managed workspace. The upstream plugin uses `pnpm`; either tool works for installing its dependencies.

## Configuration

The active configuration is at [`.zoto-spec-system/config.json`](../.zoto-spec-system/config.json):

```json
{
  "unitOfWork": "spec",
  "specsDir": "specs",
  "workDir": "specs/current",
  "spec": {
    "maxSubtasks": 99,
    "parallelLimit": 4,
    "adversarialVerification": true
  },
  "hooks": {
    "sessionStartNudge": {
      "enabled": true,
      "threshold": 20,
      "message": "You have ${count} unprocessed ${unitOfWork}s in specs/current. Consider running /zoto-spec-create to organize them."
    }
  },
  "extensions": {
    "memory": {
      "enabled": true,
      "plugin": "crux-memories"
    }
  }
}
```

Field reference: [`zoto-agents/plugins/zoto-spec-system/docs/config-schema.md`](https://github.com/zotoio/zoto-agents/blob/main/plugins/zoto-spec-system/docs/config-schema.md).

### Why `extensions.memory.enabled` is `true`

This repo *is* the CRUX-Compress memory plugin. Enabling the extension wires the spec lifecycle into the existing memory commands (`/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-meditate`). Specifically:

- After `/zoto-spec-execute` finishes, the executor suggests `/crux-dream` so learnings from the execution report are extracted.
- Spec generation can pull existing memories into context via `/crux-recall`.

If you don't want memory integration in a particular checkout, set `extensions.memory.enabled` to `false` — Spec System will fall back to plain spec / judge / execute.

## Daily workflow

1. **Capture** — Drop a one-liner or design note into `specs/current/your-idea.md`.
2. **Create** — Run `/zoto-spec-create @specs/current/your-idea.md` (or just `/zoto-spec-create "free text description"`). The generator writes `specs/[yyyymmdd]-[slug]/spec-[slug]-[yyyymmdd].md` plus subtask files.
3. **Judge** — Run `/zoto-spec-judge specs/[yyyymmdd]-[slug]/` for an independent quality gate. Accept the offered fixes if any.
4. **Execute** — Run `/zoto-spec-execute specs/[yyyymmdd]-[slug]/`. The executor spawns subagents per subtask, performs adversarial verification with `zoto-spec-judge`, and writes `execution-report-[slug]-[yyyymmdd].md`.
5. **Dream** *(optional, with memory enabled)* — Run `/crux-dream` to extract memories from the execution report.

The CRUX agent allocation rule (`.cursor/rules/spec-agent-allocation.md`) is consulted both by the generator (when filling the `Assigned Subagent` field on each subtask) and by the executor (when spawning subagents) — so subtasks land on `crux-platform-architect`, `crux-software-engineer`, `crux-cursor-rule-manager`, `crux-cursor-memory-manager`, `integrity-expert`, or `docs-sync-agent` rather than `generalPurpose`.

## Verifying the install

Inside Cursor, after restart:

```text
/zoto-spec-create --help
```

…should describe the command. If it doesn't appear, confirm the plugin is enabled in **Settings → Plugins** and that `.zoto-spec-system/config.json` parses (the session-start hook logs an error otherwise).

For a manual sanity check from the shell:

```bash
python3 -c "import json; json.load(open('.zoto-spec-system/config.json')); print('config OK')"
```

## Existing specs as reference

Browse `specs/20260406-crux-forget/` and `specs/20260425-crux-recall/` for fully-executed examples — they include the spec index, dependency-ordered subtasks, the judge's assessment (`assessment-...md`), and the executor's report (`execution-report-...md`).
