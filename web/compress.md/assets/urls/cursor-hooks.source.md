# Cursor Hooks

Hooks let you observe, control, and extend the agent loop using custom scripts. They are spawned processes that communicate over stdio using JSON in both directions. Hooks run before or after defined stages of the agent loop and can observe, block, or modify behavior.

With hooks, you can:

- Inject context at session start
- Control subagent (Task tool) execution
- Gate risky operations (e.g., SQL writes)
- Scan for PII or secrets
- Add analytics for events
- Run formatters after edits

---

## Agent and Tab Support

Hooks work with both Cursor Agent (Cmd+K/Agent Chat) and Cursor Tab (inline completions), using different hook events:

**Agent (Cmd+K/Agent Chat) events:**

- `afterAgentResponse` / `afterAgentThought` — Track agent responses
- `stop` — Handle agent completion
- `preCompact` — Observe context window compaction
- `beforeSubmitPrompt` — Validate prompts before submission
- `beforeReadFile` / `afterFileEdit` — Control file access and edits
- `beforeMCPExecution` / `afterMCPExecution` — Control MCP tool usage
- `beforeShellExecution` / `afterShellExecution` — Control shell commands
- `subagentStart` / `subagentStop` — Subagent (Task tool) lifecycle
- `preToolUse` / `postToolUse` / `postToolUseFailure` — Generic tool use hooks (all tools)
- `sessionStart` / `sessionEnd` — Session lifecycle management

**Tab (inline completions) events:**

- `afterTabFileEdit` — Post-process Tab edits
- `beforeTabFileRead` — Control file access for Tab completions

---

## Quickstart

Create a `hooks.json` file at the project level (`/.cursor/hooks.json`) or in your home directory (`~/.cursor/hooks.json`). Project-level hooks apply only to that project; home directory hooks apply globally.

**User hooks (`~/.cursor/`):**

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [{ "command": "./hooks/format.sh" }]
  }
}
```

Scripts run from `~/.cursor/`, so use `./hooks/format.sh`.

**Project hooks (`/.cursor/`):**

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [{ "command": ".cursor/hooks/format.sh" }]
  }
}
```

Scripts run from the project root; use `.cursor/hooks/format.sh` (not `./hooks/format.sh`).

Cursor watches hooks config files and reloads them automatically.

---

## Hook Types

### Command-Based Hooks

Command hooks execute shell scripts that receive JSON via stdin and return JSON via stdout.

**Exit codes:**

- `0` — Hook succeeded, use JSON output
- `2` — Block the action (equivalent to `permission: "deny"`)
- Other — Hook failed, action proceeds (fail-open by default)

```json
{
  "hooks": {
    "beforeShellExecution": [{
      "command": "./scripts/approve-network.sh",
      "timeout": 30,
      "matcher": "curl|wget|nc"
    }]
  }
}
```

### Prompt-Based Hooks

Prompt hooks use an LLM to evaluate a natural language condition. Useful for policy enforcement without custom scripts.

```json
{
  "hooks": {
    "beforeShellExecution": [{
      "type": "prompt",
      "prompt": "Does this command look safe? Only allow read-only operations.",
      "timeout": 10
    }]
  }
}
```

- Optional `model` field to override default LLM
- `$ARGUMENTS` placeholder auto-replaced with hook input JSON
- Returns `{ ok: boolean, reason?: string }`

---

## Configuration

**Priority order** (highest to lowest): Enterprise → Team → Project → User

**Config locations:**

- User: `~/.cursor/hooks.json`
- Project: `/.cursor/hooks.json`
- Team: Web dashboard (enterprise only)
- Enterprise: System paths (Windows: `C:\ProgramData\Cursor\`, Linux: `/etc/cursor/`, macOS: `/Library/Application Support/Cursor/`)

### Per-Script Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `command` | string | required | Script path or command |
| `type` | string | `"command"` | `"command"` or `"prompt"` |
| `timeout` | number | platform default | Execution timeout (seconds) |
| `loop_limit` | number | `5` | Per-script loop limit for stop/subagentStop; `null` = no limit |
| `failClosed` | boolean | `false` | When true, hook failures block the action |
| `matcher` | string/object | - | Filter criteria for when hook runs |

### Matchers

Matchers filter when a hook runs. The matched field depends on the hook:

- **beforeShellExecution / afterShellExecution** — Matched against shell command string
- **subagentStart / subagentStop** — Matched against subagent type (`explore`, `shell`, `generalPurpose`)
- **preToolUse / postToolUse** — Matched against tool type (`Shell`, `Read`, `Write`, `Grep`, `Task`, `MCP: ...`)
- **afterFileEdit / beforeReadFile** — Filter by tool type (`TabWrite`, `Write`, etc.)

---

## Key Hook Events Reference

### preToolUse

Called before any tool execution. Fires for all tool types. Use matchers to filter by tool.

**Output:** `permission` (`allow`|`deny`), `user_message`, `agent_message`, `updated_input` (optional modified tool input)

### postToolUse

Called after successful tool execution. Useful for auditing and injecting context.

**Input includes:** `tool_name`, `tool_input`, `tool_output`, `duration`, `cwd`

**Output:** `updated_mcp_tool_output` (MCP only), `additional_context` (extra context for conversation)

### subagentStart

Called before spawning a subagent (Task tool).

**Input includes:** `subagent_id`, `subagent_type`, `task`, `parent_conversation_id`, `subagent_model`, `git_branch`

**Output:** `permission` (`allow`|`deny`), `user_message`

### subagentStop

Called when a subagent completes, errors, or is aborted.

**Input includes:** `subagent_type`, `status` (completed|error|aborted), `task`, `summary`, `duration_ms`, `modified_files`, `loop_count`

**Output:** `followup_message` — Auto-continue with this message when status is `"completed"`. Subject to `loop_limit`.

### beforeShellExecution

Called before shell command executes.

**Input:** `command`, `cwd`, `sandbox`

**Output:** `permission` (`allow`|`deny`|`ask`), `user_message`, `agent_message`

Set `failClosed: true` for security-critical hooks to block on failure.

### afterShellExecution

Fires after shell command executes.

**Input:** `command`, `output`, `duration`, `sandbox`

### afterFileEdit

Fires after Agent edits a file. Useful for formatters.

**Input:** `file_path`, `edits` (array of `old_string`/`new_string`)

### stop

Called when the agent loop ends. Can auto-submit a follow-up to keep iterating.

**Input:** `status` (completed|aborted|error), `loop_count`

**Output:** `followup_message` — When provided, Cursor submits it as the next user message. Enables loop-style flows. Limited by `loop_limit` (default 5).

### sessionStart

Called when a new composer conversation is created. Fire-and-forget; agent loop does not wait.

**Input:** `session_id`, `is_background_agent`, `composer_mode`

**Output:** `env` (session-scoped env vars), `additional_context` (system context to inject)

### sessionEnd

Called when a composer conversation ends. Fire-and-forget; response not used.

**Input:** `session_id`, `reason` (completed|aborted|error|window_close|user_close), `duration_ms`, `final_status`, `error_message`

---

## Common Input Schema

All hooks receive these base fields in addition to hook-specific fields:

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | string | Stable ID across turns |
| `generation_id` | string | Changes with every user message |
| `model` | string | Model for the composer |
| `hook_event_name` | string | Which hook is running |
| `cursor_version` | string | Cursor version (e.g. "1.7.2") |
| `workspace_roots` | string[] | Root folders in workspace |
| `user_email` | string \| null | Authenticated user email |
| `transcript_path` | string \| null | Path to transcript file |

---

## Environment Variables

Hook scripts receive these environment variables:

| Variable | Description | Always Present |
|----------|-------------|----------------|
| `CURSOR_PROJECT_DIR` | Workspace root | Yes |
| `CURSOR_VERSION` | Cursor version | Yes |
| `CURSOR_USER_EMAIL` | User email | If logged in |
| `CURSOR_TRANSCRIPT_PATH` | Transcript file path | If transcripts enabled |
| `CURSOR_CODE_REMOTE` | `"true"` in remote workspace | For remote only |
| `CLAUDE_PROJECT_DIR` | Alias for project dir | Yes |

Session-scoped variables from `sessionStart` are passed to subsequent hooks in that session.

---

## Partner Integrations

- **MCP governance:** MintMCP, Oasis Security, Runlayer
- **Code security:** Corridor, Semgrep
- **Dependency security:** Endor Labs
- **Agent security:** Snyk (Evo Agent Guard)
- **Secrets management:** 1Password

See [Hooks for security and platform teams](https://cursor.com/blog/hooks-partners) for details.
