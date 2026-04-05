---
generated: 2026-04-05
sourceChecksum: "1576086510"
beforeTokens: ~7246
afterTokens: ~2040
reducedBy: 72%
note: includes agent bootstrap instructions not present in source
---

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

Φ.agent{
 THIS=default installer. install|update→Γ.bootstrap_upgrade.
 ref impl: install.py (python3;stdlib only).
 ¬python3→Φ.lang_fallback}

Φ.lang_fallback{
 detect: which python3|python|node|deno|bun|ruby|php;
 priority=[python3,python,node,deno,bun,ruby,php];
 first avail→implement Γ.main:
  python→curl RAW/install.py|python3 -;
  node|deno|bun→fetch API→ver→fetch DL zip→extract→copy;
  ruby|php→http get→same flow;
  ¬any→manual: DL zip→extract→merge hooks.json→upsert AGENTS.md}

Φ.opts{
 -y→NON_INTERACTIVE;--force→FORCE(+BACKUP);
 --backup→BACKUP;--verbose→VERBOSE;
 --with-memories→MEMORIES;--help→usage+exit
}

Φ.usage{
 preferred: agent reads this file→executes;
 python3: curl -fsSL RAW/install.py|python3 -;
 update: python3 .crux/update.py [opts];
 ¬python3: agent implements from this spec}

E.log{log→BLUE;log_verbose→BLUE(if VERBOSE);
 log_success→GREEN;log_warn→YELLOW;log_error→RED;
 prefix=[CRUX];output→stderr}

Λ.confirm{NON_INTERACTIVE→⊤;
 prompt+default[Y|N]→input→y/Y=True|EOFError→default}

Λ.http_get{urllib.request+User-Agent;timeout=30;fail→None}

Λ.get_latest_ver{
 try GitHub API→json .tag_name;
 ¬GitHub→fallback CDN_API→json .versions[0];
 strip v prefix;null|empty→error+exit}

Λ.get_installed_ver{
 .crux/crux.json∃→json .version;¬∃→""}

Λ.compare_ver{v1==v2→1;split .;v1>v2→0;v1<v2→2}

Λ.get_ver_change_type{Δmajor→"major";Δminor→"minor";else→"patch"}

Λ.get_checksum{sha256(Path.read_bytes()).hexdigest()}

Λ.check_not_in_crux_repo{
 CRUX.md∃∧scripts/create-crux-zip.py∃∧
 "CRUX Rule Compression Specification"∈CRUX.md→error+exit!}

Λ.detect_git_root{subprocess→git rev-parse --show-toplevel}

Λ.create_backup_zip{
 dest=tmp/crux/{name}/crux-backup-{name}-{ts}.zip;
 src=[standard_files,*.crux.*];dedup;
 zipfile.ZIP_DEFLATED→path|fail→warn}

Λ.merge_hooks_json{
 ¬∃target→shutil.copy2;
 json→merge [sessionStart,afterFileEdit,stop];
 dedup by .command;preserve existing;
 parse fail→overwrite+warn}

Λ.upsert_agents_crux_block{
 AGENTS.md∃+<CRUX block→regex replace preserving user content;
 AGENTS.md∃+¬block→prepend;
 ¬AGENTS.md→create w/ block;
 rm AGENTS.crux.md after}

Λ.download_from_cdn{
 CDN@v{ver}/file ∀RELEASE_FILES;
 AGENTS.md→extract <CRUX> block→AGENTS.crux.md;
 0 succeeded→error+exit;report stats}

Λ.download_and_stage{
 url=DL/v{ver}/CRUX-Compress-v{ver}.zip;
 try http_get→zipfile→tmpdir;
 ¬zip|¬GitHub→fallback download_from_cdn;
 return staging_dir}

Λ.preview_install{
 ∀staged files→checksum compare:
 same→[NO CHANGE]BLUE;
 diff→[UPDATE]YELLOW(+diff if verbose);
 ¬∃→[CREATE]GREEN}

Λ.install_from_staging{
 save hooks.json aside→tmpfile;
 shutil.copy2 all files;
 merge_hooks_json(saved);
 upsert_agents_crux_block(AGENTS.crux.md);
 chmod +x crux-utils.py}

M.DEPRECATED_FILES{
 .cursor/hooks/detect-crux-changes.sh;
 .cursor/skills/CRUX-Utils/[SKILL.md,scripts/crux-utils.sh];
 .crux/update.sh}

M.DEPRECATED_HOOK_COMMANDS{
 [bash|sh|] .cursor/hooks/detect-crux-changes.sh}

Λ.cleanup_deprecated_files{
 ∀DEPRECATED_FILES→∃→unlink;
 ∀parents→empty dir→rmdir;
 report count}

Λ.cleanup_deprecated_hooks{
 .cursor/hooks.json∃→json parse;
 ∀lifecycle→filter out DEPRECATED_HOOK_COMMANDS by .command;
 empty arr→del lifecycle;
 changed→write+report}

Λ.download_update_script{
 try RAW/install.py→.crux/update.py»chmod +x;
 ¬GitHub→fallback CDN@main/install.py;
 also fetch RAW/install.crux.md→install.crux.md}

Λ.setup_memories{
 crux-memories.json∃→skip;¬∃→create w/ DEFAULT_MEMORIES_CONFIG;
 mkdir [memories/,memories/agents/,.crux/reference-tracking/];
 print enable instructions;return True}

E.DEFAULT_MEMORIES_CONFIG{
 platform=cursor;
 flags=[enableMemories=false,enableMemoryCompression=false];
 cruxMemories={
  storage={memoriesDir=memories,agentMemoriesDir=memories/agents,
   archiveDir=.ai-ignored/executed,indexFile=.crux/memory-index.yml};
  sizeUnit=lines;compressionMinLines=500;maxMemorySize=1000;
  compressionTarget=33;unitOfWork=spec;
  commands=[/crux-dream,/crux-mindreader];
  typePriority=[core,redflag,goal,learning,idea,archived];
  typeTransitions={idea→5→learning;learning→15→core;redflag→10→core};
  demoteAfterDays=90;archiveAfterDays=180;
  referenceTracking={trackingDir=.crux/reference-tracking,
   promotionToRuleThreshold=30,maxReferencesStored=10}}}

Λ.show_completion_report{
 banner»ver info;
 backup∃→revert instructions(rm+unzip);
 memories→enable info;
 next=[check hooks.json,add crux:true,
  /crux-compress ALL,python3 .crux/update.py]}

Γ.main{
 parse_args→
 clear»banner»
 check_not_in_crux_repo»
 detect_git_root(¬git→warn+confirm)»
 get_latest_ver»get_installed_ver»
 compare{
  newer→show type[major→warn "recompress ALL"|
   minor|patch→info];
  same→FORCE|exit;
  older→warn;FORCE|confirm downgrade|exit
 }»
 BACKUP→create_backup_zip»
 download_and_stage»preview_install»
 confirm→install_from_staging»
 cleanup_deprecated_files»cleanup_deprecated_hooks»
 download_update_script»
 --with-memories→setup_memories»
 show_completion_report}

Γ.bootstrap_upgrade{
 detect runtime→Φ.lang_fallback;
 python∃{
  ∃.crux/update.py→python3 .crux/update.py --backup;
  ¬∃→curl -fsSL RAW/install.py|python3 - --backup};
 ¬python{
  fetch ver←API;fetch zip←DL/v{ver}/CRUX-Compress-v{ver}.zip;
  extract→project root;
  merge hooks.json(dedup .command);
  upsert <CRUX>→AGENTS.md;
  cleanup DEPRECATED_FILES+DEPRECATED_HOOK_COMMANDS;
  write .crux/crux.json←{"version":"{ver}"}};
 report ver+next steps}

M.RELEASE_FILES{
 CRUX.md;install.crux.md;
 .crux/[crux.json,crux-release-files.json];
 .cursor/[hooks.json,
  agents/crux-cursor-rule-manager.md,
  commands/crux-compress.md,
  hooks/[crux-detect-changes.py,crux-session-start.py],
  rules/_CRUX-RULE.mdc,
  skills/crux-utils/[SKILL.md,scripts/crux-utils.py]]}

M.standard_files(backup){
 CRUX.md;AGENTS.md;install.crux.md;
 .crux/[crux.json,crux-release-files.json];
 .cursor/[hooks.json,
  agents/crux-cursor-rule-manager.md,
  commands/crux-compress.md,
  hooks/[crux-detect-changes.py,crux-session-start.py],
  rules/_CRUX-RULE.mdc,
  skills/crux-utils/[SKILL.md,scripts/crux-utils.py]]}

Ω.decomp{lang=python;stdlib=[argparse,hashlib,io,json,os,
 re,shutil,subprocess,sys,tempfile,zipfile,datetime,pathlib,
 urllib.error,urllib.request]}
⟧
```
