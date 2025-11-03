#!/usr/bin/env python3
"""
Publish a draft post:
    - Moves drafts/<slug>.html to posts/<slug>.html
    - Runs add-post-card.py to insert the post card into index.html
    - Automatically updates blog metadata for related posts

Usage:
    python scripts/publish-draft.py <slug> [--featured]
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Import shared utilities
sys.path.insert(0, str(Path(__file__).parent))
from lib.manifest import DraftsManifest
from lib.shared import estimate_reading_time


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

    # Read draft content
    draft_content = draft_path.read_text(encoding="utf-8")

    # Recalculate reading time from actual HTML content
    print("📊 Calculating reading time from content...")
    actual_reading_time = estimate_reading_time(draft_content, strip_html=True)
    print(f"✅ Calculated reading time: {actual_reading_time} min")

    # Update reading time in content
    import re

    # Find current reading time pattern: "X min read" or "[X] min read"
    reading_time_pattern = r"\[?\d+\]?\s+min read"
    updated_content = re.sub(
        reading_time_pattern, f"{actual_reading_time} min read", draft_content, flags=re.IGNORECASE
    )

    # Write to posts directory with updated reading time
    post_path.write_text(updated_content, encoding="utf-8")
    draft_path.unlink()
    print(f"✅ Moved draft to posts: {post_path}")

    # Remove from drafts manifest using centralized module
    manifest = DraftsManifest(project_root)
    if manifest.remove_entry(args.slug):
        print("✅ Removed from drafts manifest")

    # Insert into index.html
    mode = "featured" if args.featured else "regular"
    cmd = [sys.executable, str(project_root / "scripts" / "add-post-card.py"), args.slug, "--auto", "--mode", mode]
    try:
        subprocess.check_call(cmd)
        print("✅ Added post card to index.html")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to update index.html with post card")
        sys.exit(e.returncode)

    # Automatically update blog metadata for related posts
    print("\n📊 Updating blog metadata for related posts...")
    metadata_cmd = [sys.executable, str(project_root / "scripts" / "update-blog-metadata.py"), args.slug]
    try:
        subprocess.check_call(metadata_cmd)
        print("✅ Updated blog metadata")
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Failed to update blog metadata (non-critical)")
        print(f"   You can run manually: python scripts/update-blog-metadata.py {args.slug}")

    print("\n🎉 Post published successfully!")
    print(f"📝 Post URL: /posts/{args.slug}.html")


if __name__ == "__main__":
    main()
