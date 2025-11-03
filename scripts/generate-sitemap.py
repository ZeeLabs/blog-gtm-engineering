#!/usr/bin/env python3
"""
GTM Engineering Blog - Sitemap Generator
Automatically generates sitemap.xml from all published blog posts.

Extracts publish dates from HTML meta tags (article:published_time)
and creates a properly formatted XML sitemap for search engines.

USAGE:
    python scripts/generate-sitemap.py [--output sitemap.xml] [--base-url https://blog.gtm-engineering.io]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

# Import shared HTML parser
sys.path.insert(0, str(Path(__file__).parent))
from lib.html_parser import get_all_posts


def create_sitemap(posts: list[dict], base_url: str) -> str:
    """
    Create XML sitemap from posts metadata.

    Args:
        posts: List of post metadata dictionaries
        base_url: Base URL of the website

    Returns:
        Pretty-printed XML string
    """
    # Create root element
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    # Add homepage
    homepage = SubElement(urlset, "url")
    SubElement(homepage, "loc").text = f"{base_url}/"
    SubElement(homepage, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    SubElement(homepage, "changefreq").text = "weekly"
    SubElement(homepage, "priority").text = "1.0"

    # Add all posts (already sorted by date, newest first)
    for post in posts:
        url_elem = SubElement(urlset, "url")
        SubElement(url_elem, "loc").text = post["full_url"]
        SubElement(url_elem, "lastmod").text = post["publish_date"].strftime("%Y-%m-%d")
        SubElement(url_elem, "changefreq").text = "monthly"
        SubElement(url_elem, "priority").text = "0.8"

    # Convert to pretty-printed XML
    xml_string = tostring(urlset, encoding="unicode")

    # Pretty print using minidom
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="  ")

    # Remove extra blank lines and XML declaration duplicates
    lines = [line for line in pretty_xml.split("\n") if line.strip()]

    return "\n".join(lines)


def main():
    """Generate sitemap.xml from all published posts."""
    parser = argparse.ArgumentParser(
        description="Generate sitemap.xml for GTM Engineering Blog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output",
        default="sitemap.xml",
        help="Output file path (default: sitemap.xml)",
    )
    parser.add_argument(
        "--base-url",
        default="https://blog.gtm-engineering.io",
        help="Base URL of the website (default: https://blog.gtm-engineering.io)",
    )
    parser.add_argument(
        "--posts-dir",
        type=Path,
        help="Posts directory (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    print("🗺️  GTM Engineering Blog - Sitemap Generator")
    print("=" * 50)
    print()

    # Determine posts directory
    if args.posts_dir:
        posts_dir = args.posts_dir
    else:
        project_root = Path(__file__).parent.parent
        posts_dir = project_root / "posts"

    if not posts_dir.exists():
        print(f"❌ Posts directory not found: {posts_dir}")
        sys.exit(1)

    print(f"📂 Scanning posts directory: {posts_dir}")

    # Get all posts metadata
    posts = get_all_posts(posts_dir, sort_by_date=True)

    if not posts:
        print("⚠️  No posts found!")
        sys.exit(1)

    print(f"✅ Found {len(posts)} posts")
    print()
    print("📄 Posts by date (newest first):")
    for i, post in enumerate(posts, 1):
        print(f"   {i}. {post['title']}")
        print(f"      Date: {post['publish_date'].strftime('%Y-%m-%d')} | URL: {post['url']}")

    print()
    print("🔨 Generating sitemap...")

    # Generate sitemap XML
    sitemap_xml = create_sitemap(posts, args.base_url)

    # Determine output path
    if Path(args.output).is_absolute():
        output_path = Path(args.output)
    else:
        project_root = Path(__file__).parent.parent
        output_path = project_root / args.output

    # Write sitemap
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sitemap_xml)
        print(f"✅ Sitemap generated: {output_path}")
        print()
        print("📊 Sitemap stats:")
        print(f"   Total URLs: {len(posts) + 1} (1 homepage + {len(posts)} posts)")
        print(f"   Latest post: {posts[0]['publish_date'].strftime('%Y-%m-%d')}")
        print(f"   Oldest post: {posts[-1]['publish_date'].strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"❌ Failed to write sitemap: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
