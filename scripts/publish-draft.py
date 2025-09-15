#!/usr/bin/env python3
"""
Publish a draft post:
    - Moves drafts/<slug>.html to posts/<slug>.html
    - Runs add-post-card.py to insert the post card into index.html

Usage:
    python scripts/publish-draft.py <slug> [--featured]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Publish a draft blog post")
    parser.add_argument("slug", help="Draft filename without .html")
    parser.add_argument("--featured", action="store_true", help="Promote as featured on index")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    drafts_dir = project_root / "drafts"
    posts_dir = project_root / "posts"
    posts_dir.mkdir(exist_ok=True)

    draft_path = drafts_dir / f"{args.slug}.html"
    post_path = posts_dir / f"{args.slug}.html"

    if not draft_path.exists():
        print(f"❌ Draft not found: {draft_path}")
        sys.exit(1)

    # Move file
    post_path.write_text(draft_path.read_text(encoding="utf-8"), encoding="utf-8")
    draft_path.unlink()
    print(f"✅ Moved draft to posts: {post_path}")

    # Remove from drafts manifest if present
    manifest_path = drafts_dir / "drafts.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
        manifest = [it for it in manifest if it.get("slug") != args.slug]
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    except Exception:
        pass

    # Insert into index.html
    mode = "featured" if args.featured else "regular"
    cmd = [sys.executable, str(project_root / "scripts" / "add-post-card.py"), args.slug, "--auto", "--mode", mode]
    try:
        subprocess.check_call(cmd)
        print("✅ Added post card to index.html")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to update index.html with post card")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
