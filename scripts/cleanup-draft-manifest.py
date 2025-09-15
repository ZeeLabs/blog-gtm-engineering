#!/usr/bin/env python3
"""
Cleanup tool: remove entries from drafts/drafts.json whose files no longer exist.
Run this after manual deletions or renames.
"""

import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest_path = root / "drafts" / "drafts.json"
if not manifest_path.exists():
    print("No drafts.json found.")
    raise SystemExit(0)

try:
    items = json.loads(manifest_path.read_text(encoding="utf-8"))
except Exception:
    items = []

clean = []
for it in items:
    url = it.get("url") or ""
    if not url.endswith(".html"):
        continue
    if (root / "drafts" / url).exists():
        clean.append(it)

manifest_path.write_text(json.dumps(clean, indent=2), encoding="utf-8")
print(f"Cleaned manifest: {len(items)} -> {len(clean)} entries")
