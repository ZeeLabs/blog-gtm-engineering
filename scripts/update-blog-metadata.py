#!/usr/bin/env python3
"""
GTM Engineering Blog - Metadata Updater
Simple script to keep blog-posts-data.js updated for related posts.

This script helps non-technical users ensure their posts appear in related articles
without having to manually edit the JavaScript file.

USAGE:
    python scripts/update-blog-metadata.py [post-name]        # Interactive mode
    python scripts/update-blog-metadata.py --all              # Process all posts (CI/CD)
    python scripts/update-blog-metadata.py --all --silent     # Silent mode (CI/CD)

FLAGS:
    --all      Process all posts automatically
    --silent   Suppress output for CI/CD usage
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Import shared HTML parser
sys.path.insert(0, str(Path(__file__).parent))
from lib.html_parser import parse_post_metadata


def create_post_data_object(metadata, post_filename):
    """Create the blog posts data object format."""

    return {
        "title": metadata["title"],
        "url": f"{post_filename}.html",
        "excerpt": metadata["description"],
        "date": metadata["publish_date"].strftime("%B %d, %Y"),  # Use actual publish date
        "image": metadata["image"],
        "imageAlt": metadata.get("image_alt", f"Featured image for {metadata['title']}"),  # Use actual alt text
        "tags": metadata["tags"],
        "category": metadata["tags"][0] if metadata["tags"] else "Strategy",
    }


def update_blog_posts_data(project_root, post_data, post_filename):
    """Update the blog-posts-data.js file with new post data."""

    data_file = project_root / "js" / "blog-posts-data.js"

    if not data_file.exists():
        print(f"❌ Blog posts data file not found: {data_file}")
        return False

    # Read the current JavaScript file
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Could not read data file: {e}")
        return False

    # Extract the blogPostsData array (between const blogPostsData = [ and ]);
    pattern = r"const blogPostsData = (\[(?:[^[\]]|\[(?:[^[\]]|\[[^[\]]*\])*\])*\]);"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        print("❌ Could not find blogPostsData array in the file")
        return False

    # Get the full array including brackets
    full_array = match.group(1)

    # Parse the existing data
    try:
        # Remove comments
        clean_content = re.sub(r"//.*$", "", full_array, flags=re.MULTILINE)

        # Try parsing as-is (might already be valid JSON from previous run)
        try:
            existing_posts = json.loads(clean_content)
        except json.JSONDecodeError:
            # Not valid JSON, try converting from JavaScript object syntax
            # Step 1: Replace unquoted property names with quoted ones
            clean_content = re.sub(r"(\s*)(\w+)(\s*):", r'\1"\2"\3:', clean_content)

            # Step 2: Replace single quotes with double quotes
            clean_content = clean_content.replace("'", '"')

            # Step 3: Normalize whitespace
            clean_content = re.sub(r"\s+", " ", clean_content).strip()

            # Try parsing again
            existing_posts = json.loads(clean_content)
    except (json.JSONDecodeError, Exception) as e:
        # If all parsing fails, start with empty array
        print(f"⚠️  Could not parse existing data (will rebuild): {e}")
        existing_posts = []

    # Remove existing entry with same URL
    existing_posts = [post for post in existing_posts if post.get("url") != f"{post_filename}.html"]

    # Add new post at the beginning (most recent first)
    existing_posts.insert(0, post_data)

    # Rebuild the JavaScript file with proper const declaration
    new_content = (
        content[: match.start()]
        + "const blogPostsData = "
        + json.dumps(existing_posts, indent=2)
        + ";"
        + content[match.end() :]
    )

    # Write back to file
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Updated blog posts data: {data_file}")
        return True
    except Exception as e:
        print(f"❌ Could not write updated data file: {e}")
        return False


def rebuild_blog_posts_data(project_root, posts_list):
    """
    Rebuild the entire blog-posts-data.js file with all posts.
    Used in --all mode for efficient bulk updates.

    Args:
        project_root: Path to project root
        posts_list: List of post data objects to write

    Returns:
        bool: True if successful, False otherwise
    """
    data_file = project_root / "js" / "blog-posts-data.js"

    if not data_file.exists():
        print(f"❌ Blog posts data file not found: {data_file}")
        return False

    # Read the current JavaScript file
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Could not read data file: {e}")
        return False

    # Extract the blogPostsData array pattern
    pattern = r"const blogPostsData = (\[(?:[^[\]]|\[(?:[^[\]]|\[[^[\]]*\])*\])*\]);"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        print("❌ Could not find blogPostsData array in the file")
        return False

    # Rebuild the JavaScript file with all posts
    new_content = (
        content[: match.start()]
        + "const blogPostsData = "
        + json.dumps(posts_list, indent=2)
        + ";"
        + content[match.end() :]
    )

    # Write back to file
    try:
        with open(data_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Rebuilt blog posts data: {data_file}")
        return True
    except Exception as e:
        print(f"❌ Could not write updated data file: {e}")
        return False


def get_available_posts(posts_dir):
    """Get list of available posts in the posts directory."""
    available = []
    if posts_dir.exists():
        for post_file in posts_dir.glob("*.html"):
            available.append(post_file.stem)
    return available


def show_help():
    """Show help and usage instructions."""
    print("🚀 GTM Engineering Blog - Metadata Updater")
    print("=" * 50)
    print()
    print("This tool updates the related posts system with your new post.")
    print("Use this AFTER publishing your post.")
    print()
    print("USAGE:")
    print("  python scripts/update-blog-metadata.py [post-name]")
    print()
    print("EXAMPLE:")
    print("  python scripts/update-blog-metadata.py my-new-post")
    print()
    print("If no post-name is given, you can choose from available posts.")
    print()


def main():
    """Main function with support for interactive and CI/CD modes."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Update blog-posts-data.js with post metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "post_name",
        nargs="?",
        help="Post filename (without .html extension)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all posts automatically (CI/CD mode)",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress output for CI/CD usage",
    )
    args = parser.parse_args()

    # Determine output mode
    verbose = not args.silent

    if verbose:
        print("🚀 GTM Engineering Blog - Metadata Updater")
        print("=" * 50)
        print()

    # Get project directories
    project_root = Path(__file__).parent.parent
    posts_dir = project_root / "posts"

    # Process all posts mode
    if args.all:
        available_posts = get_available_posts(posts_dir)

        if not available_posts:
            if verbose:
                print("❌ No posts found in the posts/ directory")
            sys.exit(1)

        if verbose:
            print(f"📂 Processing {len(available_posts)} posts...")
            print()

        # Collect all post data first
        all_posts_data = []
        fail_count = 0

        for post_filename in available_posts:
            post_path = posts_dir / f"{post_filename}.html"

            # Use shared HTML parser
            metadata_dict = parse_post_metadata(post_path)
            if not metadata_dict:
                if verbose:
                    print(f"⚠️  Skipping {post_filename}: Could not parse metadata")
                fail_count += 1
                continue

            # Convert to old format for compatibility
            metadata = {
                "title": metadata_dict["title"],
                "description": metadata_dict["description"],
                "author": metadata_dict["author"],
                "image": metadata_dict["image"],
                "image_alt": metadata_dict.get("image_alt", ""),
                "publish_date": metadata_dict["publish_date"],
                "tags": metadata_dict["tags"],
            }

            # Create post data object
            post_data = create_post_data_object(metadata, post_filename)
            all_posts_data.append(post_data)

            if verbose:
                print(f"✅ Parsed: {post_filename}")

        # Rebuild the entire blog posts data file in one operation
        success_count = 0
        if all_posts_data:
            if rebuild_blog_posts_data(project_root, all_posts_data):
                success_count = len(all_posts_data)
            else:
                fail_count += len(all_posts_data)

        if verbose:
            print()
            print(f"📊 Results: {success_count} updated, {fail_count} failed")

        sys.exit(0 if fail_count == 0 else 1)

    # Single post mode (interactive or specified)
    if args.post_name:
        post_filename = args.post_name
        if post_filename.endswith(".html"):
            post_filename = post_filename[:-5]  # Remove .html extension
    else:
        # Interactive mode
        available_posts = get_available_posts(posts_dir)

        if not available_posts:
            print("❌ No posts found in the posts/ directory")
            print("💡 Make sure your post is published first!")
            print("   Publish with: python scripts/publish-draft.py your-post-name")
            sys.exit(1)

        print("📝 Available posts:")
        for i, post in enumerate(available_posts, 1):
            print(f"   {i}. {post}")
        print()

        try:
            choice = input("Enter number or post name: ").strip()
            if choice.isdigit():
                post_filename = available_posts[int(choice) - 1]
            else:
                post_filename = choice
        except (ValueError, IndexError):
            print("❌ Invalid choice")
            sys.exit(1)

    # Process single post
    post_path = posts_dir / f"{post_filename}.html"

    # Check if post exists
    if not post_path.exists():
        if verbose:
            print(f"❌ Post not found: {post_path}")
            print("💡 Make sure the post is published first!")
            print("   Publish with: python scripts/publish-draft.py your-post-name")
        sys.exit(1)

    # Extract metadata using shared parser
    if verbose:
        print(f"📄 Extracting metadata from: {post_filename}.html")

    metadata_dict = parse_post_metadata(post_path)
    if not metadata_dict:
        if verbose:
            print("❌ Could not extract metadata from post")
        sys.exit(1)

    # Convert to old format for compatibility
    metadata = {
        "title": metadata_dict["title"],
        "description": metadata_dict["description"],
        "author": metadata_dict["author"],
        "image": metadata_dict["image"],
        "image_alt": metadata_dict.get("image_alt", ""),
        "publish_date": metadata_dict["publish_date"],
        "tags": metadata_dict["tags"],
    }

    # Show what we found
    if verbose:
        print("\n📊 Found metadata:")
        print(f"   Title: {metadata['title']}")
        print(f"   Author: {metadata['author']}")
        print(f"   Date: {metadata['publish_date'].strftime('%B %d, %Y')}")
        print(f"   Description: {metadata['description'][:50]}...")
        print(f"   Tags: {', '.join(metadata['tags'])}")
        print(f"   Image: {metadata['image']}")
        print(f"   Image Alt: {metadata['image_alt'][:50]}...")
        print()

    # Create post data object
    post_data = create_post_data_object(metadata, post_filename)

    # Update the blog posts data file
    if update_blog_posts_data(project_root, post_data, post_filename):
        if verbose:
            print("🎉 Metadata updated successfully!")
            print()
            print("✅ Your post will now appear in related articles")
            print("✅ Related posts section is working correctly")
            print()
            print(f"💡 Next: Test your post at /posts/{post_filename}.html")
            print("💡 Related posts should appear at the bottom of your article")
    else:
        if verbose:
            print("❌ Failed to update metadata")
        sys.exit(1)


if __name__ == "__main__":
    main()
