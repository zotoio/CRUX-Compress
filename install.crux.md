---
generated: 2026-04-22 15:30
sourceChecksum: "1739657208"
beforeTokens: ~9185
afterTokens: ~2510
reducedBy: 73%
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

M.MEMORY_FILE_PREFIXES{
 .cursor/[agents/crux-cursor-memory-manager.md,
  commands/[crux-dream.md,crux-mindreader.md,crux-forget.md,crux-amnesia.md],
  hooks/crux-detect-memory-changes.py,
  rules/crux-memories-integration.crux.mdc,
  skills/crux-skill-memory-*]}

Λ.is_memory_file{rel_path.startswith(∈MEMORY_FILE_PREFIXES)}
Λ.memories_already_installed{.crux/crux-memories.json∃}

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

Λ.get_release_files{
 fetch .crux/dist-manifest.json←CDN|RAW→json .files;
 ¬avail→fallback built-in minimal list}

Λ._download_one{CDN/{path}→target_dir/{path};return (path,ok)}

Λ.download_from_cdn{
 CDN@v{ver}/file ∀get_release_files(ver);
 ThreadPoolExecutor(max_workers=8)→parallel DL;
 progress: done/total every 4 files;
 AGENTS.md→extract <CRUX> block→AGENTS.crux.md;
 0 succeeded→error+exit;report stats}

Λ.verify_checksums{
 staging/.crux/crux-release-files.json∃→
 json .releases[ver].files→∀{file,checksum}→
 sha256 compare;mismatch→warn;report stats}

Λ.download_and_stage{
 url=DL/v{ver}/CRUX-Compress-v{ver}.zip;
 try http_get→zipfile→tmpdir→verify_checksums;
 ¬zip|¬GitHub→fallback download_from_cdn→verify_checksums;
 return staging_dir}

Λ.load_known_checksums{
 .crux/crux-release-files.json→∀releases→∀files→
 collect {filepath→{checksum*}} across all versions}

Λ.preview_install{
 ∀staged files:
  is_memory_file+¬install_memories→skip+count;
  checksum compare:
   same→[NO CHANGE]BLUE;
   diff+cksum∉known_releases→[MODIFIED]RED"local changes detected";
   diff+cksum∈known_releases→[UPDATE]YELLOW(+diff if verbose);
   ¬∃→[CREATE]GREEN;
 skipped∃→[SKIP]BLUE"N memory files (use --with-memories)";
 return locally_modified[]}

Λ.install_from_staging{
 save hooks.json aside→tmpfile;
 ∀files: is_memory_file+¬install_memories→skip;
 else→shutil.copy2;
 merge_hooks_json(saved);
 upsert_agents_crux_block(AGENTS.crux.md);
 chmod +x [crux-utils.py,memory-index.py,post-dream.py]}

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
 __file__∃+is install.py→shutil.copy2→.crux/update.py;
 ¬file(piped)→try RAW/install.py→.crux/update.py»chmod +x;
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
  commands=[/crux-dream,/crux-mindreader,/crux-forget,/crux-amnesia];
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
 install_memories=--with-memories|memories_already_installed»
 load_known_checksums(if upgrade)»
 download_and_stage»preview_install(install_memories)→locally_modified»
 locally_modified∃→warn+list+suggest "git diff before commit"»
 confirm→install_from_staging(install_memories)»
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

M.RELEASE_FILES{←.crux/dist-manifest.json .files
 (single source of truth: scripts/create-crux-zip.py→DIST_FILES)
 fallback=built-in minimal list if manifest unavailable}

M.standard_files(backup){
 CRUX.md;AGENTS.md;install.crux.md;
 .crux/[crux.json,crux-release-files.json];
 .cursor/[hooks.json,agents/crux-cursor-rule-manager.md,
  commands/crux-compress.md,
  hooks/[crux-detect-changes.py,crux-session-start.py],
  rules/_CRUX-RULE.mdc,
  skills/crux-utils/[SKILL.md,scripts/crux-utils.py]]}

Ω.decomp{lang=python;stdlib=[argparse,concurrent.futures,hashlib,io,json,os,
 re,shutil,subprocess,sys,tempfile,zipfile,datetime,pathlib,
 urllib.error,urllib.request]}
⟧
```
