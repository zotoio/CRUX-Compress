#!/usr/bin/env python3
"""Embed data.json into report.template.html -> report.html (works from file://)."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    data = json.loads((HERE / "data.json").read_text(encoding="utf-8"))
    payload = json.dumps(data, ensure_ascii=False)
    template = (HERE / "report.template.html").read_text(encoding="utf-8")
    if "/*__DATA__*/" not in template:
        raise SystemExit("report.template.html missing /*__DATA__*/ placeholder")
    out = template.replace("/*__DATA__*/", payload, 1)
    (HERE / "report.html").write_text(out, encoding="utf-8")
    print(f"Wrote {HERE / 'report.html'} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
