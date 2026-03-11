---
generated: 2026-03-06 20:00
sourceUrl: https://cursor.com/docs/hooks
beforeTokens: 6800
afterTokens: 1200
reducedBy: 82%
confidence: 94%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Cursor Hooks Documentation

```crux
⟦CRUX:cursor-hooks.md
Ρ{Cursor Hooks; observe+control+extend agent loop via custom scripts;
 spawned processes; JSON over stdio; run before|after agent stages}

Κ{hook=script⊲agent_stage; cmd=command-based(default);
 prompt=LLM-evaluated; matcher=filter criteria;
 Tab=inline completions; Agent=Cmd+K|Agent Chat}

E.capabilities{inject ctx@sessionStart; control subagent(Task);
 gate risky ops(e.g. SQL writes); scan PII|secrets;
 add analytics; run formatters post-edit}

E.agent_hooks{
 sessionStart|sessionEnd→session lifecycle;
 preToolUse|postToolUse|postToolUseFailure→generic(∀tools);
 subagentStart|subagentStop→Task tool lifecycle;
 beforeShellExecution|afterShellExecution→shell cmd;
 beforeMCPExecution|afterMCPExecution→MCP tool;
 beforeReadFile→file access control;
 afterFileEdit→post-edit(formatters);
 beforeSubmitPrompt→validate prompts pre-send;
 preCompact→observe ctx compaction;
 stop→agent loop end+auto-followup;
 afterAgentResponse|afterAgentThought→track output
}
E.tab_hooks{beforeTabFileRead; afterTabFileEdit}

Φ.cfg{
 file=hooks.json; version:num=1;
 project@.cursor/hooks.json→run from project root;
 user@~/.cursor/hooks.json→run from ~/.cursor/;
 team=web dashboard(enterprise)→managed hooks dir;
 enterprise=[macOS@"/Library/Application Support/Cursor/hooks.json",
  linux@/etc/cursor/hooks.json,
  win@"C:\ProgramData\Cursor\hooks.json"]
}
R.priority{Enterprise≻Team≻Project≻User;
 ∀matching hooks run; conflict→higher priority wins merge}

E.types.cmd{
 shell script; stdin←JSON; stdout→JSON;
 exit0=ok+use JSON output;
 exit2=deny(=permission:"deny");
 other=fail→proceed(fail-open default)
}
E.types.prompt{
 type:"prompt"; LLM evaluates natural lang condition;
 ?model field override; fast model default;
 $ARGUMENTS→auto-replace w/ hook input JSON;
 absent $ARGUMENTS→input auto-appended;
 returns {ok:bool,?reason:str}
}

Φ.per_script{
 command:str!→script path|cmd;
 type:"command"|"prompt"="command";
 timeout:num=platform_default(seconds);
 loop_limit:num?=5(cursor)|null(claude_code)→stop|subagentStop;
 failClosed:bool=⊥;⊤→block on failure(crash|timeout|bad JSON);
 matcher:str?→filter when hook runs
}

M.common_input{∀hooks receive:
 conversation_id:str; generation_id:str; model:str;
 hook_event_name:str; cursor_version:str(e.g."1.7.2");
 workspace_roots:[str]; user_email:str?; transcript_path:str?
}

E.preToolUse{⊲any tool exec;
 in+={tool_name,tool_input:obj,tool_use_id,cwd,model,agent_message};
 out={permission:"allow"|"deny",?user_message,?agent_message,
  ?updated_input:obj→modified tool input}}

E.postToolUse{⊲successful tool exec;
 in+={tool_name,tool_input,tool_output:str(JSON),
  tool_use_id,cwd,duration:ms,model};
 out={?updated_mcp_tool_output:obj(MCP only→replaces output),
  ?additional_context:str→injected after result}}

E.postToolUseFailure{⊲tool fail|timeout|denied;
 in+={tool_name,tool_input,tool_use_id,cwd,error_message:str,
  failure_type:"error"|"timeout"|"permission_denied",
  duration:ms,is_interrupt:bool}; out=∅}

E.subagentStart{⊲before Task tool spawn;
 in+={subagent_id,subagent_type:str(generalPurpose|explore|shell|...),
  task:str,parent_conversation_id,tool_call_id,
  subagent_model,is_parallel_worker:bool,?git_branch};
 out={permission:"allow"|"deny"(ask→deny),?user_message}}

E.subagentStop{⊲subagent done;
 in+={subagent_type,status:"completed"|"error"|"aborted",
  task,description,summary,duration_ms,message_count,
  tool_call_count,loop_count(starts 0),
  modified_files:[str],?agent_transcript_path};
 out={?followup_message→auto-continue(only status=completed)};
 loop_limit applies(default 5)}

E.beforeShellExecution{in+={command,cwd,sandbox:bool};
 out={permission:"allow"|"deny"|"ask",?user_message,?agent_message}}
E.beforeMCPExecution{in+={tool_name,tool_input,url|command};
 out={permission:"allow"|"deny"|"ask",?user_message,?agent_message};
 failClosed=⊤ recommended}
E.afterShellExecution{in+={command,output,duration:ms,sandbox:bool}}
E.afterMCPExecution{in+={tool_name,tool_input,result_json,duration:ms}}

E.afterFileEdit{in+={file_path:abs,edits:[{old_string,new_string}]}}
E.beforeReadFile{
 in+={file_path:abs,content,attachments:[{type:"file"|"rule",file_path}]};
 out={permission:"allow"|"deny",?user_message}}
E.beforeTabFileRead{in+={file_path,content};¬attachments;
 out={permission:"allow"|"deny"}}
E.afterTabFileEdit{in+={file_path,edits:[{old_string,new_string,
 range:{start_line_number,start_column,end_line_number,end_column},
 old_line,new_line}]}}

E.beforeSubmitPrompt{⊲user send→before backend;
 in+={prompt,attachments:[{type,file_path}]};
 out={continue:bool,?user_message}}
E.afterAgentResponse{in+={text:str}}
E.afterAgentThought{in+={text:str,?duration_ms}}

E.stop{⊲agent loop ends;
 in+={status:"completed"|"aborted"|"error",loop_count};
 out={?followup_message→auto-submit as next user msg};
 loop_limit=5 default;null=no cap}

E.sessionStart{fire-and-forget;¬blocking;
 in+={session_id,is_background_agent:bool,
  ?composer_mode:"agent"|"ask"|"edit"};
 out={?env:{k:v}→set ∀subsequent hooks,?additional_context}}

E.sessionEnd{fire-and-forget;
 in+={session_id,reason:"completed"|"aborted"|"error"|"window_close"|"user_close",
  duration_ms,is_background_agent:bool,final_status,?error_message}}

E.preCompact{observe only;¬block|modify;
 in+={trigger:"auto"|"manual",context_usage_percent,
  context_tokens,context_window_size,message_count,
  messages_to_compact,is_first_compaction:bool};
 out={?user_message}}

M.matchers{
 beforeShellExecution|afterShellExecution→cmd string;
 subagentStart|subagentStop→subagent_type;
 preToolUse|postToolUse|postToolUseFailure→tool_name
  [Shell,Read,Write,Grep,Delete,Task,"MCP: <name>"];
 afterFileEdit→tool_type[TabWrite,Write];
 beforeReadFile→tool_type[TabRead,Read];
 afterAgentThought→"AgentThought";
 afterAgentResponse→"AgentResponse";
 stop→"Stop"; beforeSubmitPrompt→"UserPromptSubmit"
}

Φ.env{
 CURSOR_PROJECT_DIR=ws root!;
 CURSOR_VERSION=ver str!;
 CURSOR_USER_EMAIL=email(if logged in);
 CURSOR_TRANSCRIPT_PATH=transcript(if enabled);
 CURSOR_CODE_REMOTE="true"(if remote ws);
 CLAUDE_PROJECT_DIR=alias compat!;
 sessionStart env→∀subsequent hooks in session
}

M.partners{
 MCP_governance=[MintMCP→inventory+monitor+scan,
  "Oasis Security"→least-privilege+audit,
  Runlayer→MCP broker+control];
 code_security=[Corridor→realtime code feedback,
  Semgrep→vuln scan+auto-regenerate];
 dep_security=["Endor Labs"→malicious pkg detect+supply chain];
 agent_security=[Snyk→"Evo Agent Guard"+prompt injection];
 secrets=[1Password→env validation+JIT secrets ¬disk]
}

R.distribution{
 project=.cursor/hooks.json in VCS→auto load trusted ws;
 MDM=deploy hooks.json+scripts→~/.cursor/|system dirs;
 cloud(enterprise)=dashboard→auto sync ∀members q30min;
 3rd party(Claude Code)=supported w/ compat
}
⟧
```