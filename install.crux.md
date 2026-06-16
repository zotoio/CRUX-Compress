---
generated: 2026-06-17 00:00
sourceChecksum: "1456234472"
cruxLevel: 25
beforeTokens: 13109
afterTokens: 2496
reducedBy: 81%
confidence: 94%
note: includes agent bootstrap instructions not present in source
---

> [!IMPORTANT]
> Generated file - do not edit!

# CRUX Compress Installer

```crux
⟦CRUX:install.py
Ρ{CRUX Compress Installer — agent-executable specification}
Κ{repo=zotoio/CRUX-Compress;
 API=api.github.com/repos/{repo}/releases/latest;
 DL=github.com/{repo}/releases/download;
 RAW=raw.githubusercontent.com/{repo}/main;
 CDN=cdn.jsdelivr.net/gh/{repo};
 CDN_API=data.jsdelivr.com/v1/packages/gh/{repo}}

Φ.primitive_layout{
 SUBDIR=crux;DIRS=[agents,commands,rules,skills];
 install→.cursor/<type>/crux/<file>;
 src→.cursor/<type>/<file>}

Λ.to_crux_primitive_path{
 .cursor/{type∈DIRS}/{x}→.cursor/{type}/crux/{x};
 already crux/|¬primitive→passthrough}
Λ.from_crux_primitive_path{
 .cursor/{type}/crux/{x}→.cursor/{type}/{x};else→passthrough}

Φ.agent{THIS=default installer;ref impl=install.py(python3;stdlib);
 ¬python3→Φ.lang_fallback}
Φ.lang_fallback{
 detect=[python3,python,node,deno,bun,ruby,php];
 python→curl RAW/install.py|python3 -;
 node|deno|bun→fetch API→ver→DL zip→extract→copy;
 ¬any→manual: DL zip→merge hooks.json→upsert AGENTS.md}
Φ.opts{-y→NON_INTERACTIVE;--force→FORCE(+BACKUP);
 --backup;--verbose;--with-memories;--with-mcp-server}
Φ.usage{preferred=agent reads this→exec;
 python3: curl -fsSL RAW/install.py|python3 -;
 update: python3 .crux/update.py [opts]}

E.log{[log,verbose,success,warn,error]→
 [BLUE,BLUE(V),GREEN,YELLOW,RED];prefix=[CRUX];→stderr}
Λ.confirm{NON_INTERACTIVE→⊤;prompt→input→y=⊤|EOF→default}

M.SOURCE_RELEASE_FILES{CRUX.md;install.crux.md;.crux/crux.json;
 .cursor/[hooks.json,
  agents/[crux-cursor-rule-manager.md,
   crux-cursor-memory-manager.md,crux-cursor-meditation-guide.md],
  commands/[crux-compress.md,crux-dream.md,crux-recall.md,
   crux-remember.md,crux-meditate.md,crux-forget.md,crux-amnesia.md],
  hooks/[crux-detect-changes.py,crux-detect-memory-changes.py,
   crux-session-start.py],
  rules/[_CRUX-RULE.mdc,crux-memories-integration.crux.mdc],
  skills/[crux-utils/[SKILL.md,scripts/crux-utils.py],
   crux-skill-memory-crud/SKILL.md,crux-skill-memory-compress/SKILL.md,
   crux-skill-memory-extract/SKILL.md,
   crux-skill-memory-index/[SKILL.md,scripts/[memory-index.py,post-dream.py]],
   crux-skill-memory-rebalance/SKILL.md,
   crux-skill-memory-reference-tracker/SKILL.md,
   crux-skill-memory-meditation-*/SKILL.md]]}
M.RELEASE_FILES{∀SOURCE→to_crux_primitive_path}
M.LEGACY_MAP{zip(SOURCE,RELEASE) where src≠dest→{legacy:crux_path}}
M.MEMORY_PREFIXES{.cursor/[
 agents/{,crux/}crux-cursor-memory-manager.md,
 agents/{,crux/}crux-cursor-meditation-guide.md,
 commands/{,crux/}crux-[dream,meditate,recall,remember,forget,amnesia].md,
 hooks/crux-detect-memory-changes.py,
 rules/{,crux/}crux-memories-integration.crux.mdc,
 skills/{,crux/}crux-skill-memory-*]}
Λ.is_memory_file{path.startswith(∈MEMORY_PREFIXES)}
Λ.memories_installed{.crux/crux-memories.json∃}

Λ.http_get{urllib.request;User-Agent;timeout=30;fail→None}
Λ.get_latest_ver{API→.tag_name;¬→CDN_API→.versions[0];strip v;¬→exit!}
Λ.get_installed_ver{.crux/crux.json→.version;¬→""}
Λ.compare_ver{==→1;>→0;<→2}
Λ.get_ver_change_type{Δmajor|Δminor|else→patch}
Λ.get_checksum{sha256(read_bytes).hexdigest}
Λ.load_known_checksums{crux-release-files.json→∀ver→∀files→
 {path→{cksum*}};+to_crux_primitive_path+from_crux_primitive_path variants}
Λ.check_not_in_crux_repo{CRUX.md∃∧scripts/create-crux-zip.py∃→exit!}
Λ.detect_git_root{git rev-parse --show-toplevel}

Λ.create_backup_zip{tmp/crux/{name}/crux-backup-{ts}.zip;
 src=[AGENTS.md,crux-release-files.json,SOURCE_RELEASE_FILES,
  RELEASE_FILES]→dedup+∀*.crux.*;ZIP_DEFLATED}
Λ.merge_hooks_json{¬target→copy;
 merge [sessionStart,afterFileEdit,stop] dedup .command;fail→overwrite}
Λ.upsert_agents_crux_block{∃<CRUX→replace;∃¬block→prepend;
 ¬AGENTS.md→create;rm AGENTS.crux.md}
Λ.get_release_files{.crux/dist-manifest.json←CDN|RAW→.files;
 ¬→fallback RELEASE_FILES}
Λ._download_one{cdn/{path}→dest;
 ¬ok→try cdn/{from_crux_primitive_path(path)};return(path,ok)}
Λ.download_from_cdn{CDN@v{ver}∀release_files;
 ThreadPoolExecutor(8)→parallel;AGENTS.md→extract <CRUX>;
 0→exit!}
Λ.verify_checksums{staging crux-release-files.json→
 ∀files→sha256 compare;mismatch→warn}
Λ.download_and_stage{DL zip→extract→verify;¬→CDN fallback→verify}
Λ.preview_install{∀staged:mem+¬install→skip;
 cksum[same→NO_CHANGE;diff∉known→MODIFIED;diff∈known→UPDATE;¬∃→CREATE];
 return locally_modified}

Λ.install_from_staging{hooks.json→aside;∀files→copy2;
 merge_hooks;upsert_agents;
 chmod+x .cursor/skills/crux/[crux-utils/scripts/crux-utils.py,
  crux-skill-memory-index/scripts/[memory-index.py,post-dream.py]]}
Λ.remove_empty_parent_dirs{walk up→rmdir until stop|fail}
Λ.migrate_primitive_layout{∀LEGACY_MAP:
 mem+¬install→skip;
 legacy∃+target∃+same_cksum→rm legacy+cleanup dirs;
 legacy∃+target∃+diff→warn conflict;
 legacy∃+¬target→mv→target+mkdir+cleanup;
 report moved+removed+conflicts}

M.DEPRECATED_FILES{.cursor/hooks/detect-crux-changes.sh;
 .cursor/skills/CRUX-Utils/[SKILL.md,scripts/crux-utils.sh];
 .crux/update.sh}
M.INTERNAL_AGENTS{.cursor/agents/{,crux/}[crux-platform-architect.md,
 crux-software-engineer.md,integrity-expert.md,docs-sync-agent.md]}
M.DEPRECATED_HOOKS{[bash|sh|] .cursor/hooks/detect-crux-changes.sh}
Λ.cleanup_deprecated{∀DEPRECATED_FILES→∃→rm;parents→rmdir empty}
Λ.cleanup_internal_agents{∀INTERNAL_AGENTS→∃→rm;
 .cursor/agents/{crux,}→empty→rmdir}
Λ.cleanup_deprecated_hooks{hooks.json→filter DEPRECATED_HOOKS;
 empty→del lifecycle;Δ→write}
Λ.download_update_script{
 __file__→.crux/update.py;piped→RAW|CDN/install.py;
 +fetch install.crux.md}

E.DEFAULT_MEMORIES_CONFIG{platform=cursor;
 flags=[enableMemories=false,enableMemoryCompression=false];
 storage={memoriesDir=memories,agents=memories/agents,
  archive=.ai-ignored/executed,idx=.crux/memory-index.yml};
 sizeUnit=lines;minLines=500;maxSize=1000;target=33;unit=spec;
 commands∀.cursor/commands/crux/crux-{name}.md:
  [dream,recall,remember,meditate,forget,amnesia];
 types=[core,redflag,goal,learning,idea,archived];
 transitions={idea→5→learning;learning→15→core;redflag→10→core};
 demote=90d;archive=180d;
 refTracking={dir=.crux/reference-tracking,promoteAt=30,max=10};
 scopes=[base,agents,shared]}

M.MCP{module=crux_mcp_server;cfg=~/.cursor/mcp.json;
 dir=~/.crux-mcp-server}
Λ.setup_mcp{recommend_dir→DL MCP zip→extract→pip install;
 cfg→~/.cursor/mcp.json{mcpServers.crux-memories=
  {command:python3,args:[-m,crux_mcp_server,-t,stdio],cwd:dir}}}
Λ.setup_memories{cfg∃→skip;¬→create DEFAULT_MEMORIES_CONFIG;
 mkdir [memories/,memories/agents/,.crux/reference-tracking/]}
Λ.show_completion_report{banner;backup→revert paths(crux/ layout);
 show_reference_update_guidance→{
  tell user/agent: upd repo files w/ legacy CRUX primitive paths;
  old=.cursor/[agents,commands,rules,skills]/*;
  new=.cursor/[agents,commands,rules,skills]/crux/*;
  .cursor/hooks/* paths unchanged(hooks.json executes directly)};
 next=[hooks.json,crux:true,/crux-compress ALL,.crux/update.py]}

Γ.main{parse_args»clear»banner»check_not_in_crux_repo»
 detect_git_root»get_latest_ver»get_installed_ver»
 compare[newer→type info;same→FORCE|exit;older→confirm]»
 BACKUP→backup_zip»
 install_mem=--with-memories|memories_installed»
 known_checksums(if upgrade)»download_and_stage»
 if upgrade→migrate_primitive_layout(install_mem)»
 preview→locally_modified→warn»
 confirm→install_from_staging(install_mem)»
 cleanup[deprecated,internal_agents,hooks]»
 download_update_script»
 --with-memories→setup_memories»
 --with-mcp-server→setup_mcp»
 show_completion_report(show_reference_update_guidance=
  bool(installed_version))}

Γ.bootstrap_upgrade{Φ.lang_fallback;
 python{∃update.py→run --backup;¬→curl|python3 -};
 ¬python{fetch ver→zip→extract→merge hooks→upsert AGENTS.md→
  cleanup deprecated→migrate_primitive_layout→
  write crux.json};report}

Ω.decomp{lang=python;stdlib=[argparse,concurrent.futures,hashlib,
 io,json,os,re,shutil,subprocess,sys,tempfile,zipfile,
 datetime,pathlib,urllib.error,urllib.request]}
⟧
```
