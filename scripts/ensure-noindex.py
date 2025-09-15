#!/usr/bin/env python3
"""
Ensure all files under drafts/ have a <meta name="robots" content="noindex,nofollow">
If missing, inject it after the <head> tag.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
drafts = root / 'drafts'
if not drafts.exists():
    raise SystemExit(0)

pattern = re.compile(r'<meta\s+name=["\']robots["\']', re.IGNORECASE)

def inject_noindex(html: str) -> str:
    if pattern.search(html):
        return html
    return re.sub(r'(<head[^>]*>)', r"\1\n        <meta name=\"robots\" content=\"noindex,nofollow\" />", html, count=1, flags=re.IGNORECASE)

changed = False
for file in drafts.glob('*.html'):
    text = file.read_text(encoding='utf-8')
    new = inject_noindex(text)
    if new != text:
        file.write_text(new, encoding='utf-8')
        changed = True

print('ensure-noindex: changed' if changed else 'ensure-noindex: no changes')
