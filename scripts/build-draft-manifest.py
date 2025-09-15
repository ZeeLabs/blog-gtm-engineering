#!/usr/bin/env python3
"""
Rebuild drafts/drafts.json manifest from files under drafts/ and keep drafts/index.html unchanged.
"""
from pathlib import Path
import json
from datetime import datetime

root = Path(__file__).resolve().parent.parent
drafts_dir = root / 'drafts'
manifest_path = drafts_dir / 'drafts.json'

if not drafts_dir.exists():
    raise SystemExit(0)

items = []
for file in sorted(drafts_dir.glob('*.html')):
    if file.name == 'index.html':
        continue
    slug = file.stem
    # naive createdAt: use file mtime if exists in manifest else now
    created_at = datetime.utcfromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
    # very light extraction of title/excerpt
    text = file.read_text(encoding='utf-8', errors='ignore')
    title = None
    import re
    m = re.search(r'<title[^>]*>([^<]+)</title>', text, re.IGNORECASE)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', text, re.IGNORECASE)
        title = m.group(1).strip() if m else slug
    # basic excerpt from meta description
    excerpt = None
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', text, re.IGNORECASE)
    if m:
        excerpt = m.group(1).strip()
    items.append({
        'slug': slug,
        'title': title,
        'url': f'{slug}.html',
        'author': 'Jorge Macias',
        'excerpt': excerpt or '',
        'createdAt': created_at,
    })

manifest_path.write_text(json.dumps(sorted(items, key=lambda x: x['createdAt'], reverse=True), indent=2), encoding='utf-8')
print(f'build-draft-manifest: wrote {len(items)} entries')
