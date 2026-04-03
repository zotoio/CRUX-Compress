"""Tests for the crux-utils.sh shell script.

Validates token counting, checksum calculation, and CLI behavior
of the CRUX utility script.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CRUX_UTILS = PROJECT_ROOT / ".cursor" / "skills" / "crux-utils" / "scripts" / "crux-utils.sh"

SAMPLE_MD = """\
---
crux: true
alwaysApply: true
---

# Sample Rule

This is a sample rule for testing CRUX compression.

## Guidelines

1. Always write clean code
2. Follow naming conventions
3. Add proper documentation

### Code Style

- Use consistent indentation
- Keep functions small
- Write meaningful comments

```javascript
function example() {
    const result = processData(input);
    return result;
}
```

## Summary

This rule ensures code quality across the project.
"""

SAMPLE_CRUX = """\
---
generated: 2024-01-01 12:00
sourceChecksum: "1234567890"
beforeTokens: 500
afterTokens: 100
confidence: 95%
---

> [!IMPORTANT]
> Generated file - do not edit!

# Sample Rule

```crux
\u27e6CRUX:sample-rule.md
\u03a1{code quality standards}
\u039a{code=clean;naming=conventions;docs=proper}
R.style{
  indent=consistent;fn=small;comments=meaningful
}
\u03a9{quality;maintainability}
\u27e7
```
"""


def _run(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(CRUX_UTILS)] + args,
        capture_output=True, text=True,
        cwd=cwd or str(PROJECT_ROOT),
    )


class TestScriptExists:
    def test_exists(self):
        assert CRUX_UTILS.is_file()


class TestHelp:
    def test_help_shows_usage(self):
        result = _run(["--help"])
        assert result.returncode == 0
        assert "CRUX Utils" in result.stdout
        assert "--token-count" in result.stdout
        assert "--cksum" in result.stdout

    def test_no_args_shows_help(self):
        result = _run([])
        assert result.returncode == 0
        assert "Usage:" in result.stdout

    def test_unknown_mode_fails(self):
        result = _run(["--unknown-mode"])
        assert result.returncode == 1
        assert "Unknown mode" in result.stdout or "Unknown mode" in result.stderr


class TestTokenCount:
    def test_estimates_tokens(self, tmp_path: Path):
        sample = tmp_path / "sample.md"
        sample.write_text(SAMPLE_MD, encoding="utf-8")

        result = _run(["--token-count", str(sample)])
        assert result.returncode == 0
        assert "Token Estimate" in result.stdout
        assert "TOTAL TOKENS" in result.stdout
        assert "Prose tokens" in result.stdout
        assert "Code tokens" in result.stdout

    def test_fails_for_nonexistent_file(self, tmp_path: Path):
        result = _run(["--token-count", str(tmp_path / "nonexistent.md")])
        assert result.returncode == 1
        assert "File not found" in result.stdout or "File not found" in result.stderr

    def test_ratio_compares_two_files(self, tmp_path: Path):
        source = tmp_path / "sample.md"
        crux = tmp_path / "sample.crux.md"
        source.write_text(SAMPLE_MD, encoding="utf-8")
        crux.write_text(SAMPLE_CRUX, encoding="utf-8")

        result = _run(["--token-count", "--ratio", str(source), str(crux)])
        assert result.returncode == 0
        assert "Compression Ratio" in result.stdout or "Compression Summary" in result.stdout

    def test_ratio_fails_with_one_arg(self, tmp_path: Path):
        sample = tmp_path / "sample.md"
        sample.write_text(SAMPLE_MD, encoding="utf-8")

        result = _run(["--token-count", "--ratio", str(sample)])
        assert result.returncode == 1
        assert "requires two file arguments" in result.stdout or "requires two" in result.stderr

    def test_crux_file_counts_special_chars(self, tmp_path: Path):
        special = tmp_path / "special.crux.md"
        special.write_text(
            "# Test\n\u27e6CRUX:test.md\n\u039a{code\u2192clean}\nR.style{indent\u2192consistent}\n\u2200fn\u2192small\n\u27e7\n",
            encoding="utf-8",
        )
        result = _run(["--token-count", str(special)])
        assert result.returncode == 0
        assert "Special tokens" in result.stdout


class TestChecksum:
    def test_calculates_checksum(self, tmp_path: Path):
        sample = tmp_path / "sample.md"
        sample.write_text(SAMPLE_MD, encoding="utf-8")

        result = _run(["--cksum", str(sample)])
        assert result.returncode == 0
        assert "Checksum" in result.stdout
        assert "FRONTMATTER" in result.stdout

    def test_consistent_output(self, tmp_path: Path):
        sample = tmp_path / "sample.md"
        sample.write_text(SAMPLE_MD, encoding="utf-8")

        r1 = _run(["--cksum", str(sample)])
        r2 = _run(["--cksum", str(sample)])
        assert r1.stdout == r2.stdout

    def test_fails_for_nonexistent_file(self, tmp_path: Path):
        result = _run(["--cksum", str(tmp_path / "nonexistent.md")])
        assert result.returncode == 1
        assert "File not found" in result.stdout or "File not found" in result.stderr
