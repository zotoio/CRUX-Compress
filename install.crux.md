---
generated: 2026-02-06
sourceChecksum: "3344498055"
beforeTokens: ~7400
afterTokens: ~1079
reducedBy: 85%
---

# CRUX Compress Installer

```crux
⟦CRUX:install.sh
Ρ{CRUX Compress Installer;bash;set -e}
Κ{repo=zotoio/CRUX-Compress;
 API=api.github.com/repos/{repo}/releases/latest;
 DL=github.com/{repo}/releases/download;
 RAW=raw.githubusercontent.com/{repo}/main;
 CDN=cdn.jsdelivr.net/gh/{repo};
 CDN_API=data.jsdelivr.com/v1/packages/gh/{repo}}

Φ.opts{
 -y→NON_INTERACTIVE;--force→FORCE+BACKUP;
 --backup→BACKUP;--verbose→VERBOSE;--help→usage+exit
}

Φ.usage{
 curl -fsSL .../install.sh|bash -s -- [opts];
 .crux/update.sh [opts]
}

E.log{log→BLUE;log_verbose→BLUE(if VERBOSE);
 log_success→GREEN;log_warn→YELLOW;log_error→RED;
 prefix=[CRUX]}

Λ.detect_script_loc{
 BASH_SOURCE in .crux/→PROJECT_ROOT=parent»cd
}

Λ.check_not_in_crux_repo{
 CRUX.md∃&scripts/create-crux-zip.sh∃→error+exit!
}

Λ.check_deps{
 req=[curl,unzip,zip];?jq→fallback JSON parse;
 missing→error+exit
}

Λ.detect_git_root{git rev-parse --show-toplevel}

Λ.confirm{
 NON_INTERACTIVE→⊤;
 prompt+default[Y|N]→read -n1→Y/y=0|else=1
}

Λ.get_latest_ver{
 try GitHub API→jq .tag_name|grep+sed;
 ¬GitHub→fallback CDN_API→jq .versions[0]|grep+sed;
 strip v prefix;null|empty→error+exit
}

Λ.get_installed_ver{
 .crux/crux.json∃→jq|grep .version;¬∃→""
}

Λ.compare_ver{
 v1==v2→1;split on .;v1>v2→0;v1<v2→2
}

Λ.get_ver_change_type{
 Δmajor→"major";Δminor→"minor";else→"patch"
}

Λ.get_manifest_files{
 .crux/crux-release-files.json+jq→.allFiles|keys
}

Λ.create_backup_zip{
 dest=/tmp/crux/{name}/crux-backup-{name}-{ts}.zip;
 src=[manifest files,standard CRUX files,*.crux.*];
 dedup»zip -q→path|fail→warn
}

Λ.backup_file{file+BACKUP→cp file.backup.{ts}}

Λ.show_file_diff{
 diff -u old new|head -20;color if tty
}

Λ.get_checksum{
 sha256sum≻shasum -a 256≻md5sum≻md5 -q≻stat size
}

Λ.preview_install{
 ∀staged→cksum compare:
  same→[NO CHANGE]BLUE;
  diff→[UPDATE]YELLOW(+diff if verbose);
  ¬∃→[CREATE]GREEN
}

Λ.upsert_agents_crux_block{
 AGENTS.md∃+<CRUX block→awk replace;
 AGENTS.md∃+¬block→prepend;
 ¬AGENTS.md→create w/ block;
 rm AGENTS.crux.md after
}

Λ.merge_hooks_json{
 ¬∃target→cp staging;
 jq→merge [sessionStart,afterFileEdit,stop];
  dedup by .command;preserve existing;
 ¬jq→overwrite+warn
}

Λ.download_from_cdn{
 CDN@v{ver}/file ∀release_files;
 AGENTS.md→extract <CRUX> block→AGENTS.crux.md;
 0 succeeded→error+exit;report stats
}

Λ.download_and_stage{
 url=DL/v{ver}/CRUX-Compress-v{ver}.zip;
 try curl→tmpdir»unzip -o -q→content»rm zip;
 ¬GitHub→fallback download_from_cdn;
 return staging path
}

Λ.install_from_staging{
 save hooks.json aside;
 rsync -a --exclude hooks.json≻cp -r;
 merge_hooks_json;
 upsert_agents_crux_block AGENTS.crux.md;
 chmod +x hooks/*.sh+crux-utils.sh
}

Λ.download_update_script{
 try curl RAW/install.sh→.crux/update.sh»chmod +x;
 ¬GitHub→fallback CDN@main/install.sh;
 ¬both→warn
}

Λ.show_completion_report{
 banner»ver info;
 backup→revert instructions;
 next=[check hooks.json,add crux:true,
  /crux-compress ALL,.crux/update.sh]
}

Γ.main{
 clear»banner»
 detect_script_loc»check_not_in_crux_repo»
 check_deps»detect_git_root(¬git→warn+confirm)»
 get_latest_ver»get_installed_ver»
 compare{
  newer→show type[major→warn+recompress|
   minor|patch→info];
  same→FORCE|exit;
  older→FORCE|confirm downgrade|exit
 }»
 create_backup_zip(if upgrade)»
 download_and_stage»preview_install»
 confirm→install_from_staging»
 download_update_script»show_completion_report
}

P.exec{BASH_SOURCE==0|empty→main;
 ¬source-only exec}

M.standard_files{
 CRUX.md;AGENTS.md;.crux/[crux.json,
  crux-release-files.json];
 .cursor/[hooks.json,
  agents/crux-cursor-rule-manager.md,
  commands/crux-compress.md,
  hooks/[crux-detect-changes.sh,crux-session-start.sh],
  rules/_CRUX-RULE.mdc,
  skills/crux-utils/[SKILL.md,scripts/crux-utils.sh]]}

Ω.decomp{emulate=shellcheck;src=sh;
  focus=[io_redir(log fn→stderr via >&2),
  quoting(word_split+glob in array assign),
  subshell_capture(echo→stdout only;log→stderr)]}
⟧
```
