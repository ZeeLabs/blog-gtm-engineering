#!/usr/bin/env python3
"""
GTM Engineering Blog - HTML Parser Library
Shared utilities for extracting metadata from blog post HTML files.

Used by:
- generate-sitemap.py
- generate-rss-feed.py
- update-blog-metadata.py
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


def extract_meta_tag(content: str, name: str, property_name: Optional[str] = None) -> Optional[str]:
    """
    Extract content from meta tag by name or property.

    Args:
        content: HTML content
        name: Meta tag name attribute
        property_name: Meta tag property attribute (for og: tags)

    Returns:
        Meta tag content or None
    """
    if property_name:
        # Try property attribute (for og:image, article:published_time, etc.)
        pattern = rf'<meta\s+property=["\']({re.escape(property_name)})["\']\s+content=(["\'])([^"]*?)\2'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(3).strip()

        # Try reversed attribute order
        pattern = rf'<meta\s+content=(["\'])([^"]*?)\1\s+property=["\']({re.escape(property_name)})["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(2).strip()

    if name:
        # Try name attribute
        pattern = rf'<meta\s+name=["\']({re.escape(name)})["\']\s+content=(["\'])([^"]*?)\2'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(3).strip()

        # Try reversed attribute order
        pattern = rf'<meta\s+content=(["\'])([^"]*?)\1\s+name=["\']({re.escape(name)})["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(2).strip()

    return None


def extract_title(content: str) -> Optional[str]:
    """Extract title from <title> tag or <h1>, removing site suffix."""
    # Try <title> tag first
    title_match = re.search(r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove site suffix like " - GTM Engineering" or " | GTM Engineering"
        title = re.sub(r"\s*[-|]\s*GTM Engineering.*$", "", title, flags=re.IGNORECASE)
        return title.strip()

    # Fallback to <h1>
    h1_match = re.search(r"<h1[^>]*>([^<]+)</h1>", content, re.IGNORECASE)
    if h1_match:
        return h1_match.group(1).strip()

    return None


def extract_description(content: str, fallback_title: Optional[str] = None) -> str:
    """Extract meta description, fallback to title."""
    desc = extract_meta_tag(content, "description")
    if desc:
        return desc

    # Fallback to title if provided
    if fallback_title:
        return fallback_title

    return "GTM Engineering Blog Post"


def extract_author(content: str) -> str:
    """Extract author from meta tag, default to Jorge Macias."""
    author = extract_meta_tag(content, "author")
    if author:
        return author
    return "Jorge Macias"


def extract_keywords(content: str) -> list[str]:
    """Extract keywords from meta tag and convert to list."""
    keywords = extract_meta_tag(content, "keywords")
    if keywords:
        # Split by comma, clean up, take first 3
        tags = [tag.strip().title() for tag in keywords.split(",")[:3] if tag.strip()]
        return tags if tags else ["Strategy"]
    return ["Strategy"]


def extract_og_image(content: str, default_image: str = "../assets/gtm-revenue-system-illustration.webp") -> str:
    """Extract Open Graph image URL, convert to relative path."""
    og_image = extract_meta_tag(content, None, "og:image")
    if og_image:
        # Convert full URL to relative path
        if "blog.gtm-engineering.io" in og_image:
            og_image = og_image.split("blog.gtm-engineering.io")[-1]
        return og_image
    return default_image


def extract_image_alt(content: str, default_title: str = "") -> str:
    """
    Extract image alt text from og:image:alt meta tag.
    Falls back to twitter:image:alt, then to default.
    """
    # Try og:image:alt first
    image_alt = extract_meta_tag(content, None, "og:image:alt")
    if image_alt:
        return image_alt

    # Try twitter:image:alt
    image_alt = extract_meta_tag(content, "twitter:image:alt")
    if image_alt:
        return image_alt

    # Fallback to generic alt text
    if default_title:
        return f"Featured image for {default_title}"
    return "Blog post featured image"


def extract_json_ld_date(content: str) -> Optional[datetime]:
    """
    Extract datePublished from JSON-LD schema.

    Looks for <script type="application/ld+json"> and parses datePublished field.
    Handles both direct objects and @graph arrays.

    Args:
        content: HTML content

    Returns:
        datetime object or None if not found
    """
    import json

    # Find JSON-LD script tags
    pattern = r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

    for match in matches:
        try:
            # Parse JSON
            data = json.loads(match)

            # Check for @graph array (common in Schema.org structured data)
            if "@graph" in data:
                graph_items = data["@graph"]
                if isinstance(graph_items, list):
                    # Look for BlogPosting or Article in graph
                    for item in graph_items:
                        if isinstance(item, dict):
                            item_type = item.get("@type", "")
                            if item_type in ["BlogPosting", "Article", "NewsArticle"]:
                                date_published = item.get("datePublished")
                                if date_published:
                                    # Parse ISO 8601 date
                                    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                                        try:
                                            return datetime.strptime(date_published, fmt)
                                        except ValueError:
                                            continue

            # Also check direct object (not in @graph)
            date_published = data.get("datePublished")
            if date_published:
                # Parse ISO 8601 date
                for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                    try:
                        return datetime.strptime(date_published, fmt)
                    except ValueError:
                        continue
        except (json.JSONDecodeError, Exception):
            # Skip malformed JSON
            continue

    return None


def extract_publish_date(content: str, file_path: Optional[Path] = None) -> datetime:
    """
    Extract publish date from HTML metadata.

    Priority order:
    1. article:published_time meta tag
    2. datePublished from JSON-LD schema
    3. File modification time
    4. Current time (fallback)

    Args:
        content: HTML content
        file_path: Path to HTML file (for mtime fallback)

    Returns:
        datetime object
    """
    # Try article:published_time meta tag
    pub_date = extract_meta_tag(content, None, "article:published_time")
    if pub_date:
        # Parse ISO 8601 date
        try:
            # Handle various formats: 2025-10-17T00:00:00Z, 2025-10-17, etc.
            for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                try:
                    return datetime.strptime(pub_date, fmt)
                except ValueError:
                    continue
        except Exception:
            pass

    # Try JSON-LD datePublished
    json_ld_date = extract_json_ld_date(content)
    if json_ld_date:
        return json_ld_date

    # Fallback to file modification time
    if file_path and file_path.exists():
        mtime = file_path.stat().st_mtime
        return datetime.fromtimestamp(mtime)

    # Ultimate fallback: current time
    return datetime.now()


def extract_content_excerpt(content: str, max_paragraphs: int = 3) -> str:
    """
    Extract first few paragraphs of content for RSS feed.

    Args:
        content: HTML content
        max_paragraphs: Maximum number of paragraphs to extract

    Returns:
        HTML string with first N paragraphs
    """
    # Find content after <!-- BLOG_POST_CONTENT_HERE --> marker or in main/article tags

    # Try to find content after the marker
    marker = "<!-- BLOG_POST_CONTENT_HERE -->"
    if marker in content:
        content_after_marker = content.split(marker, 1)[1]
        # Extract content until next major closing tag or script
        # Look for paragraphs
        paragraphs = re.findall(r"<p[^>]*>.*?</p>", content_after_marker, re.DOTALL | re.IGNORECASE)
    else:
        # Fallback: extract all paragraphs
        paragraphs = re.findall(r"<p[^>]*>.*?</p>", content, re.DOTALL | re.IGNORECASE)

    # Take first N paragraphs
    excerpt_paragraphs = paragraphs[:max_paragraphs]

    if excerpt_paragraphs:
        return "\n\n".join(excerpt_paragraphs)

    # Ultimate fallback: meta description
    return f"<p>{extract_description(content)}</p>"


def parse_post_metadata(file_path: Path) -> Optional[Dict]:
    """
    Parse all metadata from a blog post HTML file.

    Args:
        file_path: Path to HTML file

    Returns:
        Dictionary with metadata or None on error
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Could not read {file_path}: {e}")
        return None

    # Extract all metadata
    title = extract_title(content)
    if not title:
        print(f"⚠️  Warning: No title found in {file_path.name}")
        title = file_path.stem.replace("-", " ").title()

    description = extract_description(content, title)
    author = extract_author(content)
    keywords = extract_keywords(content)
    image = extract_og_image(content)
    image_alt = extract_image_alt(content, title)
    publish_date = extract_publish_date(content, file_path)
    excerpt = extract_content_excerpt(content)

    return {
        "title": title,
        "description": description,
        "author": author,
        "keywords": keywords,
        "tags": keywords,  # Alias for compatibility
        "image": image,
        "image_alt": image_alt,
        "publish_date": publish_date,
        "excerpt": excerpt,
        "filename": file_path.stem,
        "url": f"{file_path.stem}.html",
        "full_url": f"https://blog.gtm-engineering.io/posts/{file_path.stem}.html",
    }


def get_all_posts(posts_dir: Path, sort_by_date: bool = True) -> list[Dict]:
    """
    Get metadata for all posts in directory.

    Args:
        posts_dir: Path to posts directory
        sort_by_date: Sort by publish date (newest first)

    Returns:
        List of post metadata dictionaries
    """
    posts = []

    if not posts_dir.exists():
        print(f"❌ Posts directory not found: {posts_dir}")
        return posts

    for post_file in posts_dir.glob("*.html"):
        metadata = parse_post_metadata(post_file)
        if metadata:
            posts.append(metadata)

    if sort_by_date:
        # Sort by publish_date, newest first
        posts.sort(key=lambda p: p["publish_date"], reverse=True)

    return posts


if __name__ == "__main__":
    # Test the parser
    from pathlib import Path

    posts_dir = Path(__file__).parent.parent.parent / "posts"
    print(f"Testing HTML parser on posts in: {posts_dir}\n")

    posts = get_all_posts(posts_dir)

    print(f"Found {len(posts)} posts:\n")
    for post in posts:
        print(f"📄 {post['title']}")
        print(f"   Date: {post['publish_date'].strftime('%Y-%m-%d')}")
        print(f"   Author: {post['author']}")
        print(f"   Tags: {', '.join(post['tags'])}")
        print(f"   Image: {post['image']}")
        print()
