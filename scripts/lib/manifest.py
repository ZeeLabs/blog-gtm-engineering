#!/usr/bin/env python3
"""
Centralized manifest management for GTM Engineering Blog.
Single source of truth for drafts.json operations.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class DraftsManifest:
    """Manage drafts/drafts.json manifest file operations."""

    def __init__(self, project_root: Path):
        """
        Initialize manifest manager.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.drafts_dir = self.project_root / "drafts"
        self.manifest_path = self.drafts_dir / "drafts.json"

    def _load_manifest(self) -> List[Dict]:
        """Load existing manifest from disk."""
        if not self.manifest_path.exists():
            return []

        try:
            manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            if not isinstance(manifest, list):
                return []
            return manifest
        except Exception:
            return []

    def _save_manifest(self, manifest: List[Dict]) -> None:
        """Save manifest to disk."""
        self.drafts_dir.mkdir(exist_ok=True)
        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    def add_entry(self, slug: str, title: str, author: str, excerpt: str) -> None:
        """
        Add or update a draft entry in the manifest.

        Args:
            slug: Post slug (filename without .html)
            title: Post title
            author: Author name
            excerpt: Post excerpt
        """
        manifest = self._load_manifest()

        # Remove existing entry with same slug
        manifest = [item for item in manifest if item.get("slug") != slug]

        # Add new entry
        manifest.append(
            {
                "slug": slug,
                "title": title,
                "url": f"{slug}.html",
                "author": author,
                "excerpt": excerpt,
                "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )

        # Sort newest first
        try:
            manifest.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        except Exception:
            pass

        self._save_manifest(manifest)

    def remove_entry(self, slug: str) -> bool:
        """
        Remove a draft entry from the manifest.

        Args:
            slug: Post slug to remove

        Returns:
            bool: True if entry was found and removed, False otherwise
        """
        manifest = self._load_manifest()
        original_length = len(manifest)

        manifest = [item for item in manifest if item.get("slug") != slug]

        if len(manifest) < original_length:
            self._save_manifest(manifest)
            return True
        return False

    def get_entry(self, slug: str) -> Optional[Dict]:
        """
        Get a specific draft entry from manifest.

        Args:
            slug: Post slug to find

        Returns:
            Dict or None: Entry data if found
        """
        manifest = self._load_manifest()
        for item in manifest:
            if item.get("slug") == slug:
                return item
        return None

    def get_all_entries(self) -> List[Dict]:
        """Get all draft entries from manifest."""
        return self._load_manifest()

    def rebuild_from_files(self) -> int:
        """
        Rebuild manifest from actual files in drafts/ directory.
        Scans directory and regenerates manifest based on existing HTML files.

        Returns:
            int: Number of drafts found and added to manifest
        """
        import re

        drafts = []
        drafts_files = list(self.drafts_dir.glob("*.html"))

        # Exclude index.html
        drafts_files = [f for f in drafts_files if f.name != "index.html"]

        for draft_file in drafts_files:
            content = draft_file.read_text(encoding="utf-8")

            # Extract title from <title> tag or <h1>
            title_match = re.search(r"<title>([^<]+)</title>", content, re.IGNORECASE)
            if not title_match:
                title_match = re.search(r"<h1[^>]*>([^<]+)</h1>", content, re.IGNORECASE)

            title = title_match.group(1).strip() if title_match else draft_file.stem

            # Extract author if available
            author_match = re.search(r'<meta\s+name="author"\s+content="([^"]+)"', content, re.IGNORECASE)
            author = author_match.group(1) if author_match else "Unknown"

            # Extract excerpt/description
            excerpt_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
            excerpt = excerpt_match.group(1) if excerpt_match else ""

            # Use file modification time as creation date
            created_at = datetime.fromtimestamp(draft_file.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")

            drafts.append(
                {
                    "slug": draft_file.stem,
                    "title": title,
                    "url": draft_file.name,
                    "author": author,
                    "excerpt": excerpt,
                    "createdAt": created_at,
                }
            )

        # Sort newest first
        drafts.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

        # Save rebuilt manifest
        self._save_manifest(drafts)

        return len(drafts)

    def cleanup_orphaned_entries(self) -> int:
        """
        Remove manifest entries for files that no longer exist.

        Returns:
            int: Number of orphaned entries removed
        """
        manifest = self._load_manifest()
        original_length = len(manifest)

        # Filter out entries where the file doesn't exist
        manifest = [item for item in manifest if (self.drafts_dir / f"{item.get('slug')}.html").exists()]

        removed_count = original_length - len(manifest)

        if removed_count > 0:
            self._save_manifest(manifest)

        return removed_count
