---
id: "dbfd3ed"
title: "File paths in documentation and websites must reference files that actually exist"
description: "Adversarial verification caught that web/compress.md/index.html listed hook files as .sh when the actual files are .py. Documentation file trees should be verified against disk contents, not assumed accurate from previous edits."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [documentation, verification, website, file-paths, adversarial]
---

**Anti-pattern**: Documentation lists file paths (file trees, install manifests, quick-start guides) that reference files with stale names or extensions.

**Example**: The website "What Gets Installed" section listed `.cursor/hooks/crux-detect-changes.sh` and `crux-session-start.sh` when the actual files had been renamed to `.py`. The original audit (subtask 10) checked for `install.sh` string references and HTML tag balance but missed stale hook file extensions.

**Prevention**:
1. When renaming or re-extending files, grep all documentation for the old name
2. Verification checklists should include "file paths point to files that exist on disk"
3. Adversarial verifiers should spot-check paths in file trees against `ls` output
