# Cursor Hooks Documentation

> [!IMPORTANT]
> Generated file — do not edit!

Cursor Hooks let you **observe, control, and extend** the agent loop via custom scripts. Hooks run as spawned processes that communicate with Cursor using JSON over stdin/stdout. They execute before or after specific agent stages.

---

## What Hooks Can Do

- **Inject context** at session start
- **Control subagents** (the Task tool)
- **Gate risky operations** (e.g., SQL writes, shell commands)
- **Scan for PII or secrets** before data leaves the workspace
- **Add analytics** or logging
- **Run formatters** after file edits

---

## Hook Events

### Agent Hooks

| Event | Description |
|-------|-------------|
| `sessionStart` / `sessionEnd` | Session lifecycle (fire-and-forget, non-blocking) |
| `preToolUse` / `postToolUse` / `postToolUseFailure` | Generic tool execution (all tools) |
| `subagentStart` / `subagentStop` | Task tool lifecycle |
| `beforeShellExecution` / `afterShellExecution` | Shell command execution |
| `beforeMCPExecution` / `afterMCPExecution` | MCP tool execution |
| `beforeReadFile` | File access control |
| `afterFileEdit` | Post-edit processing (e.g., formatters) |
| `beforeSubmitPrompt` | Validate prompts before sending to backend |
| `preCompact` | Observe context compaction (read-only) |
| `stop` | Agent loop ends; supports auto-followup |
| `afterAgentResponse` / `afterAgentThought` | Track agent output |

### Tab Hooks (Inline Completions)

| Event | Description |
|-------|-------------|
| `beforeTabFileRead` | Before Tab reads a file |
| `afterTabFileEdit` | After Tab edits a file |

---

## Configuration

Hooks are defined in **`hooks.json`** (version: 1).

### Configuration Locations

| Level | Path |
|-------|-----|
| **Project** | `.cursor/hooks.json` (runs from project root) |
| **User** | `~/.cursor/hooks.json` |
| **Team** | Web dashboard (enterprise; managed hooks directory) |
| **Enterprise (system)** | macOS: `/Library/Application Support/Cursor/hooks.json`<br>Linux: `/etc/cursor/hooks.json`<br>Windows: `C:\ProgramData\Cursor\hooks.json` |

### Priority Order

**Enterprise ≻ Team ≻ Project ≻ User**

All matching hooks run. If there is a conflict, the higher-priority level wins and merges override.

---

## Hook Types

### Command (default)

- Shell script; receives JSON on **stdin**, returns JSON on **stdout**
- **Exit 0** = success; Cursor uses the JSON output
- **Exit 2** = deny (equivalent to `permission: "deny"`)
- Any other exit = failure; Cursor proceeds by default (fail-open) unless `failClosed: true`

### Prompt

- `type: "prompt"` — an LLM evaluates a natural-language condition
- Optional `model` field to override; fast model used by default
- `$ARGUMENTS` in the prompt is auto-replaced with the hook input JSON; if absent, input is auto-appended
- Returns `{ ok: boolean, reason?: string }`

---

## Per-Script Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Script path or command |
| `type` | No | `"command"` (default) or `"prompt"` |
| `timeout` | No | Seconds; platform default if omitted |
| `loop_limit` | No | Max loops (5 for Cursor, null for Claude Code); applies to `stop` / `subagentStop` |
| `failClosed` | No | `false` (default): proceed on failure. `true`: block on crash, timeout, or bad JSON |
| `matcher` | No | Filter criteria for when the hook runs |

---

## Common Input (All Hooks)

Every hook receives:

- `conversation_id`, `generation_id`, `model`
- `hook_event_name`, `cursor_version` (e.g., `"1.7.2"`)
- `workspace_roots`, `user_email?`, `transcript_path?`

---

## Key Hook Events: Inputs and Outputs

### preToolUse

**Trigger:** Before any tool executes.

**Input (additional):** `tool_name`, `tool_input`, `tool_use_id`, `cwd`, `model`, `agent_message`

**Output:** `permission: "allow" | "deny"`, optional `user_message`, `agent_message`, `updated_input`

### postToolUse

**Trigger:** After successful tool execution.

**Input (additional):** `tool_name`, `tool_input`, `tool_output` (JSON string), `tool_use_id`, `cwd`, `duration` (ms), `model`

**Output:** `updated_mcp_tool_output` (MCP only — replaces output), `additional_context` (injected after result)

### postToolUseFailure

**Trigger:** Tool fail, timeout, or denied.
**Input (additional):** `tool_name`, `tool_input`, `error_message`, `failure_type` (`"error" | "timeout" | "permission_denied"`)
**Output:** None

### subagentStart

**Trigger:** Before Task tool spawns.

**Input (additional):** `subagent_id`, `subagent_type`, `task`, `parent_conversation_id`, `tool_call_id`, `subagent_model`, `is_parallel_worker`, `git_branch?`

**Output:** `permission: "allow" | "deny"` (ask → deny), optional `user_message`

### subagentStop

**Trigger:** Subagent finishes.

**Input (additional):** `subagent_type`, `status` (`"completed" | "error" | "aborted"`), `task`, `description`, `summary`, `duration_ms`, `message_count`, `tool_call_count`, `loop_count`, `modified_files`, `agent_transcript_path?`

**Output:** `followup_message` — when `status === "completed"`, auto-submitted as next user message. `loop_limit` applies (default 5).

### beforeShellExecution / afterShellExecution

**beforeShell:** input `command`, `cwd`, `sandbox` → output `permission`, optional `user_message`, `agent_message`
**afterShell:** input `command`, `output`, `duration`, `sandbox` (no output)

### beforeMCPExecution / afterMCPExecution

**beforeMCP:** input `tool_name`, `tool_input`, `url`|`command` → output `permission`, optional messages. **Note:** `failClosed: true` recommended.
**afterMCP:** input `tool_name`, `tool_input`, `result_json`, `duration`

### beforeReadFile / beforeTabFileRead

**beforeReadFile:** input `file_path`, `content`, `attachments` → output `permission`, optional `user_message`
**beforeTabFileRead:** input `file_path`, `content` (no attachments) → output `permission`

### afterFileEdit / afterTabFileEdit

**afterFileEdit:** input `file_path`, `edits: [{ old_string, new_string }]`
**afterTabFileEdit:** input `file_path`, `edits` (includes `range`, `old_line`, `new_line`)

### beforeSubmitPrompt

**Trigger:** User sends prompt; runs before backend.

**Input:** `prompt`, `attachments`
**Output:** `continue: boolean`, optional `user_message`

### stop

**Trigger:** Agent loop ends.

**Input:** `status` (`"completed" | "aborted" | "error"`), `loop_count`
**Output:** `followup_message` — auto-submitted as next user message. `loop_limit` default 5; `null` = no cap.

### sessionStart / sessionEnd

**sessionStart** (fire-and-forget): input includes `session_id`, `is_background_agent`, optional `composer_mode`. Output: `env` (key-value; set for all subsequent hooks), `additional_context`.

**sessionEnd** (fire-and-forget): input includes `session_id`, `reason`, `duration_ms`, `final_status`, optional `error_message`.

---

## Matchers

Matchers filter when a hook runs:

- `beforeShell` / `afterShell` → match on command string
- `subagentStart` / `subagentStop` → match on `subagent_type`
- `preToolUse` / `postToolUse` / `postToolUseFailure` → match on `tool_name` (e.g., `Shell`, `Read`, `Write`, `Grep`, `Delete`, `Task`, `"MCP: <name>"`)
- `afterFileEdit` → `tool_type` (`TabWrite`, `Write`)
- `beforeReadFile` → `tool_type` (`TabRead`, `Read`)

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CURSOR_PROJECT_DIR` | Workspace root (required) |
| `CURSOR_VERSION` | Version string (required) |
| `CURSOR_USER_EMAIL` | User email (if logged in) |
| `CURSOR_TRANSCRIPT_PATH` | Transcript path (if enabled) |
| `CURSOR_CODE_REMOTE` | `"true"` if workspace is remote |
| `CLAUDE_PROJECT_DIR` | Alias for compatibility |

Environment set by `sessionStart` applies to all subsequent hooks in the session.
