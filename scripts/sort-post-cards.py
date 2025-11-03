#!/usr/bin/env python3
"""
GTM Engineering Blog - Post Card Sorter
Sorts post cards in index.html by publish date (newest first).

Reads all posts from posts/ directory, extracts publish dates, then reorders
the post cards in index.html to match chronological order (newest to oldest).

Usage:
    python scripts/sort-post-cards.py

Exit codes:
    0: Success (post cards sorted)
    1: Error occurred
"""

import re
import sys
from datetime import datetime
from pathlib import Path

# Import shared utilities
from lib.html_parser import get_all_posts


def extract_post_slug_from_card(card_html: str) -> str | None:
    """
    Extract the post slug from a post card HTML block.

    Args:
        card_html: HTML string of a post card

    Returns:
        Post slug (filename without .html) or None
    """
    # Look for href="posts/SLUG.html" pattern
    match = re.search(r'posts/([^"]+?)\.html', card_html)
    if match:
        return match.group(1)
    return None


def extract_post_cards(content) -> list[tuple[str, str]]:
    """
    Extract all post card HTML blocks from index.html content.

    Args:
        content: Full HTML content of index.html

    Returns:
        List of (slug, card_html) tuples
    """
    post_cards = []

    # Find the regular blog posts section
    regular_posts_marker = "<!-- Regular Blog Posts -->"
    marker_pos = content.find(regular_posts_marker)

    if marker_pos == -1:
        print("❌ Could not find '<!-- Regular Blog Posts -->' marker")
        return post_cards

    # Find the closing </div> for blog-grid (flexible pattern)
    # Start searching after the marker
    search_start = marker_pos
    # Use flexible regex instead of exact string match
    pattern_end = r"</div>\s*</div>\s*</section>"
    match = re.search(pattern_end, content[search_start : search_start + 50000])

    if not match:
        print("❌ Could not find end of blog-grid section")
        return post_cards

    blog_grid_end = search_start + match.start()

    # Extract the section containing post cards
    cards_section = content[marker_pos:blog_grid_end]

    # Extract individual post cards using regex
    # Pattern: <article...class="post-card"...>...</article> (flexible attribute order)
    pattern = r"<article[^>]*\bpost-card\b[^>]*>.*?</article>"
    matches = re.finditer(pattern, cards_section, re.DOTALL)

    for match in matches:
        card_html = match.group(0)
        slug = extract_post_slug_from_card(card_html)

        if slug:
            post_cards.append((slug, card_html))

    return post_cards


def sort_post_cards(posts_dir: Path, index_path: Path) -> bool:
    """
    Sort post cards in index.html by publish date.

    Args:
        posts_dir: Path to posts directory
        index_path: Path to index.html file

    Returns:
        True if successful, False otherwise
    """
    # Get all posts with metadata sorted by date
    posts = get_all_posts(posts_dir, sort_by_date=True)

    if not posts:
        print("❌ No posts found in posts directory")
        return False

    print(f"📚 Found {len(posts)} posts with metadata")

    # Create lookup dict: slug -> publish_date
    post_dates = {post["filename"]: post["publish_date"] for post in posts}

    # Read index.html
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Could not read index.html: {e}")
        return False

    # Extract post cards
    post_cards = extract_post_cards(content)

    if not post_cards:
        print("❌ No post cards found in index.html")
        return False

    print(f"📇 Found {len(post_cards)} post cards in index.html")

    # Sort post cards by publish date (newest first)
    def get_publish_date(card_tuple: tuple[str, str]) -> datetime | None:
        slug, _ = card_tuple
        return post_dates.get(slug, None)

    # Filter out cards without matching posts
    valid_cards = [(slug, html) for slug, html in post_cards if slug in post_dates]
    orphan_cards = [(slug, html) for slug, html in post_cards if slug not in post_dates]

    if orphan_cards:
        print(f"⚠️  Warning: {len(orphan_cards)} post cards without matching posts:")
        for slug, _ in orphan_cards:
            print(f"   - {slug}")

    # Sort valid cards by date
    sorted_cards = sorted(valid_cards, key=get_publish_date, reverse=True)

    # Add orphan cards at the end (preserve them even if no matching post)
    sorted_cards.extend(orphan_cards)

    # Show sorting order
    print_limit = 10
    print("\n📅 Sorted order (newest to oldest):")
    for i, (slug, _) in enumerate(sorted_cards[:print_limit], 1):
        date = post_dates.get(slug)
        date_str = date.strftime("%Y-%m-%d") if date else "Unknown"
        print(f"   {i}. {slug} ({date_str})")
    if len(sorted_cards) > print_limit:
        print(f"   ... and {len(sorted_cards) - print_limit} more")

    # Reconstruct index.html with sorted cards
    regular_posts_marker = "<!-- Regular Blog Posts -->"
    marker_pos = content.find(regular_posts_marker)

    # Find where post cards section ends (flexible pattern)
    search_start = marker_pos
    pattern_end = r"</div>\s*</div>\s*</section>"
    match = re.search(pattern_end, content[search_start : search_start + 50000])

    if not match:
        print("❌ Could not find end of blog-grid section for reconstruction")
        return False

    blog_grid_end = search_start + match.start()

    # Build new content
    before_cards = content[: marker_pos + len(regular_posts_marker)]
    after_cards = content[blog_grid_end:]

    # Join sorted card HTML (preserve original formatting)
    # Each card already has proper indentation, so just join with newlines
    card_separator = "\n                        "
    sorted_cards_html = card_separator.join([html for _, html in sorted_cards])

    # Reconstruct full HTML
    new_content = before_cards + card_separator + sorted_cards_html + card_separator + after_cards

    # Write back to file
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("\n✅ Post cards sorted by publish date (newest first)")
        return True
    except Exception as e:
        print(f"❌ Could not write index.html: {e}")
        return False


def main() -> None:
    """Main function to sort post cards."""
    print("🔄 GTM Engineering Blog - Post Card Sorter")
    print("=" * 50)

    # Get project root directory
    project_root = Path(__file__).parent.parent
    posts_dir = project_root / "posts"
    index_path = project_root / "index.html"

    # Validate paths
    if not posts_dir.exists():
        print(f"❌ Posts directory not found: {posts_dir}")
        sys.exit(1)

    if not index_path.exists():
        print(f"❌ index.html not found: {index_path}")
        sys.exit(1)

    # Sort post cards
    success = sort_post_cards(posts_dir, index_path)

    if success:
        sys.exit(0)
    else:
        print("\n❌ Failed to sort post cards")
        sys.exit(1)


if __name__ == "__main__":
    main()
