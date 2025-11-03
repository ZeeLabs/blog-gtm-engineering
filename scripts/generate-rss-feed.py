#!/usr/bin/env python3
"""
GTM Engineering Blog - RSS Feed Generator
Automatically generates feed.xml from all published blog posts.

Extracts full post metadata including publish dates, content excerpts,
and generates a properly formatted RSS 2.0 feed for subscribers.

USAGE:
    python scripts/generate-rss-feed.py [--output feed.xml] [--base-url https://blog.gtm-engineering.io]
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


def format_rfc822_date(dt: datetime) -> str:
    """
    Format datetime to RFC 822 format for RSS pubDate.

    Args:
        dt: datetime object

    Returns:
        RFC 822 formatted date string (e.g., "Fri, 17 Oct 2025 00:00:00 GMT")
    """
    # RSS 2.0 uses RFC 822 date format
    # Day, DD Mon YYYY HH:MM:SS TZ
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    weekday = weekdays[dt.weekday()]
    month = months[dt.month - 1]

    return f"{weekday}, {dt.day:02d} {month} {dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"


def create_rss_feed(posts: list[dict], base_url: str) -> str:
    """
    Create RSS 2.0 feed from posts metadata.

    Args:
        posts: List of post metadata dictionaries
        base_url: Base URL of the website

    Returns:
        Pretty-printed XML string
    """
    # Create root element
    rss = Element("rss")
    rss.set("version", "2.0")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    # Create channel
    channel = SubElement(rss, "channel")

    # Channel metadata
    SubElement(channel, "title").text = "GTME Blog - GTM Engineering"
    SubElement(
        channel, "description"
    ).text = "Expert insights on go-to-market strategies, RevOps, and scaling B2B growth"
    SubElement(channel, "link").text = f"{base_url}/"
    SubElement(channel, "language").text = "en-US"
    SubElement(channel, "copyright").text = "GTM Engineering"
    SubElement(channel, "managingEditor").text = "hello@gtm-engineering.io (Jorge Macias)"
    SubElement(channel, "webMaster").text = "hello@gtm-engineering.io (Jorge Macias)"

    # Build dates (use most recent post date or current date)
    build_date = posts[0]["publish_date"] if posts else datetime.now()
    SubElement(channel, "lastBuildDate").text = format_rfc822_date(build_date)
    SubElement(channel, "pubDate").text = format_rfc822_date(build_date)

    SubElement(channel, "generator").text = "GTM Engineering Blog System"
    SubElement(channel, "docs").text = "https://www.rssboard.org/rss-specification"
    SubElement(channel, "ttl").text = "1440"

    # Atom self-link
    atom_link = SubElement(channel, "atom:link")
    atom_link.set("href", f"{base_url}/feed.xml")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    # Channel image
    image = SubElement(channel, "image")
    SubElement(
        image, "url"
    ).text = "https://images.squarespace-cdn.com/content/v1/67f6a2abaec6f26633e3ec6b/b7425771-777b-4948-9af1-4b28287183a8/GTM+Logo+Horizontal+Sharp.png?format=1500w"
    SubElement(image, "title").text = "GTME Blog - GTM Engineering"
    SubElement(image, "link").text = f"{base_url}/"
    SubElement(image, "width").text = "1500"
    SubElement(image, "height").text = "500"
    SubElement(image, "description").text = "GTM Engineering Logo"

    # Add items for each post
    for post in posts:
        item = SubElement(channel, "item")

        SubElement(item, "title").text = post["title"]
        SubElement(item, "link").text = post["full_url"]
        SubElement(item, "description").text = post["description"]

        # Content excerpt (encoded HTML)
        content_encoded = SubElement(item, "content:encoded")
        content_encoded.text = post["excerpt"]

        # Publish date
        SubElement(item, "pubDate").text = format_rfc822_date(post["publish_date"])

        # GUID (permalink)
        guid = SubElement(item, "guid")
        guid.set("isPermaLink", "true")
        guid.text = post["full_url"]

        # Author
        SubElement(item, "dc:creator").text = post["author"]

        # Categories (tags)
        for tag in post["tags"]:
            SubElement(item, "category").text = tag

        # Enclosure (featured image)
        if post["image"]:
            enclosure = SubElement(item, "enclosure")
            # Convert relative path to full URL
            image_url = post["image"]
            if image_url.startswith("../assets/"):
                image_url = f"{base_url}/assets/{image_url.replace('../assets/', '')}"
            elif image_url.startswith("/assets/"):
                image_url = f"{base_url}{image_url}"

            enclosure.set("url", image_url)
            # Determine type from extension
            if image_url.endswith(".webp"):
                enclosure.set("type", "image/webp")
            elif image_url.endswith(".png"):
                enclosure.set("type", "image/png")
            elif image_url.endswith(".jpg") or image_url.endswith(".jpeg"):
                enclosure.set("type", "image/jpeg")
            else:
                enclosure.set("type", "image/webp")  # Default
            enclosure.set("length", "0")  # Length not critical for images

    # Convert to string
    xml_string = tostring(rss, encoding="unicode")

    # Pretty print using minidom
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="    ")

    # Remove extra blank lines
    lines = [line for line in pretty_xml.split("\n") if line.strip()]

    return "\n".join(lines)


def main():
    """Generate feed.xml from all published posts."""
    parser = argparse.ArgumentParser(
        description="Generate RSS feed for GTM Engineering Blog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output",
        default="feed.xml",
        help="Output file path (default: feed.xml)",
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

    print("📡 GTM Engineering Blog - RSS Feed Generator")
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
        print(f"      Date: {post['publish_date'].strftime('%Y-%m-%d')} | Author: {post['author']}")
        print(f"      Tags: {', '.join(post['tags'])}")

    print()
    print("🔨 Generating RSS feed...")

    # Generate RSS feed XML
    feed_xml = create_rss_feed(posts, args.base_url)

    # Determine output path
    if Path(args.output).is_absolute():
        output_path = Path(args.output)
    else:
        project_root = Path(__file__).parent.parent
        output_path = project_root / args.output

    # Write feed
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(feed_xml)
        print(f"✅ RSS feed generated: {output_path}")
        print()
        print("📊 Feed stats:")
        print(f"   Total items: {len(posts)}")
        print(f"   Latest post: {posts[0]['publish_date'].strftime('%Y-%m-%d')}")
        print(f"   Oldest post: {posts[-1]['publish_date'].strftime('%Y-%m-%d')}")
        print(f"   Build date: {format_rfc822_date(posts[0]['publish_date'])}")
    except Exception as e:
        print(f"❌ Failed to write feed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
