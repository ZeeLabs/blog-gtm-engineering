#!/usr/bin/env python3
"""
GTM Engineering Blog - Post Card Generator
Simple script to generate post cards for index.html from existing HTML posts.
Supports promoting posts to featured status and proper image handling.
"""

import re
import sys
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def get_color_scheme():
    """Return a random color scheme for the post card."""
    schemes = [
        {"color1": "10b981", "color2": "059669", "label": "GTM Strategy"},
        {"color1": "f59e0b", "color2": "d97706", "label": "RevOps Stack"},
        {"color1": "8b5cf6", "color2": "7c3aed", "label": "Data Stack"},
        {"color1": "ef4444", "color2": "dc2626", "label": "Sales Velocity"},
        {"color1": "06b6d4", "color2": "0891b2", "label": "Analytics"},
        {"color1": "ec4899", "color2": "db2777", "label": "Growth"},
        {"color1": "f97316", "color2": "ea580c", "label": "Automation"},
    ]
    import random
    
    scheme = random.choice(schemes)
    return scheme["color1"], scheme["color2"], scheme["label"]


def extract_meta_from_html(html_content):
    """Extract metadata from existing HTML post."""
    data = {}
    
    # Extract title from <title> tag or h1
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove " - GTM Engineering" suffix if present
        title = re.sub(r'\s*-\s*GTM Engineering.*$', '', title)
        data['title'] = title
    else:
        # Fallback to h1
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
        if h1_match:
            data['title'] = h1_match.group(1).strip()
    
    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if desc_match:
        data['description'] = desc_match.group(1).strip()
    
    # Extract author
    author_match = re.search(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if author_match:
        data['author'] = author_match.group(1).strip()
    else:
        data['author'] = "Jorge Macias"  # Default
    
    # Extract Open Graph image for proper image display
    og_image_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if og_image_match:
        image_url = og_image_match.group(1).strip()
        # Convert full URL to relative path if it's from the same domain
        if 'blog.gtm-engineering.io' in image_url:
            image_url = image_url.split('blog.gtm-engineering.io')[-1]
        data['image_url'] = image_url
    
    # Extract keywords for tags
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if keywords_match:
        keywords = keywords_match.group(1).strip()
        # Convert keywords to tags (first 3)
        tags = [tag.strip() for tag in keywords.split(',')[:3]]
        data['tags'] = [tag.title() for tag in tags if tag.strip()]
    
    if not data.get('tags'):
        data['tags'] = ['Strategy']
    
    return data


def create_post_card_html(post_data, filename, is_featured=False):
    """Generate HTML for the blog post card to add to index.html."""
    color1, color2, card_label = get_color_scheme()
    
    # Use actual image if available, otherwise use gradient background
    if post_data.get('image_url'):
        image_html = f'''<div class="post-card-image" role="img" aria-label="{post_data["title"]} post thumbnail">
                    <img
                        src="{post_data['image_url']}"
                        alt="{post_data['title']} illustration"
                        style="width: 100%; height: 100%; object-fit: cover;"
                    />
                </div>'''
    else:
        image_html = f'''<div
                class="post-card-image"
                style="
                  background: linear-gradient(135deg, #{color1} 0%, #{color2} 100%);
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  color: white;
                  font-size: 1.2rem;
                  font-weight: bold;
                "
                role="img"
                aria-label="{post_data["title"]} post thumbnail"
              >
                {card_label}
              </div>'''
    
    card_content = f'''              <div class="post-card-content">
                <h3 class="post-card-title">
                  <a href="posts/{filename}.html"
                    >{post_data["title"]}</a
                  >
                </h3>
                <p class="post-card-excerpt">
                  {post_data["description"]}
                </p>
                <div class="post-card-meta">
                  <span class="post-card-date">
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true"
                    >
                      <rect
                        x="3"
                        y="4"
                        width="18"
                        height="18"
                        rx="2"
                        ry="2"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                      <line
                        x1="16"
                        y1="2"
                        x2="16"
                        y2="6"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                      <line
                        x1="8"
                        y1="2"
                        x2="8"
                        y2="6"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                      <line
                        x1="3"
                        y1="10"
                        x2="21"
                        y2="10"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                    </svg>
                    {datetime.now().strftime("%B %d, %Y")}
                  </span>
                  <span class="post-card-author">
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true"
                    >
                      <path
                        d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                      <circle
                        cx="12"
                        cy="7"
                        r="4"
                        stroke="currentColor"
                        stroke-width="2"
                      />
                    </svg>
                    {post_data["author"]}
                  </span>
                </div>
                <div class="post-card-tags">
                  {" ".join([f'<a href="#" class="post-tag">{tag}</a>' for tag in post_data["tags"]])}
                </div>
              </div>'''
    
    if is_featured:
        return f'''<!-- Featured Post -->
                        <article class="featured-post">
                            <div class="post-card">
                {image_html}
{card_content}
            </article>'''
    else:
        return f'''            <article class="post-card">
              {image_html}
{card_content}
            </article>'''


def extract_current_featured_post(content):
    """Extract the current featured post HTML to move it to regular posts."""
    # Find the featured post section
    featured_start = content.find('<!-- Featured Post -->')
    if featured_start == -1:
        # Look for direct featured-post class
        featured_start = content.find('<article class="featured-post">')
    
    if featured_start == -1:
        return None, content
    
    # Find the end of the featured post article
    article_count = 0
    pos = featured_start
    while pos < len(content):
        if content[pos:].startswith('<article'):
            article_count += 1
        elif content[pos:].startswith('</article>'):
            article_count -= 1
            if article_count == 0:
                featured_end = pos + len('</article>')
                break
        pos += 1
    else:
        return None, content
    
    # Extract the featured post HTML
    featured_html = content[featured_start:featured_end]
    
    # Convert featured post to regular post format
    # Remove the featured-post wrapper and convert to regular post-card
    regular_post_html = re.sub(r'<!-- Featured Post -->\s*', '', featured_html)
    regular_post_html = re.sub(r'<article class="featured-post">\s*<div class="post-card">', 
                              '<article class="post-card">', regular_post_html)
    regular_post_html = re.sub(r'</article>\s*$', '</article>', regular_post_html)
    
    # Remove the featured post from content
    remaining_content = content[:featured_start] + content[featured_end:]
    
    return regular_post_html.strip(), remaining_content


def promote_post_to_featured(new_featured_html, index_path):
    """Promote new post to featured and move current featured to regular posts."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract current featured post
        current_featured_html, content_without_featured = extract_current_featured_post(content)
        
        # Find where to insert the new featured post
        blog_grid_start = content_without_featured.find('<div class="blog-grid">')
        if blog_grid_start == -1:
            print("❌ Could not find blog-grid section")
            return False
        
        featured_insertion_point = content_without_featured.find('>', blog_grid_start) + 1
        
        # Find where to insert regular posts (after comment)
        regular_insertion_point = content_without_featured.find('<!-- Regular Blog Posts -->')
        if regular_insertion_point == -1:
            print("❌ Could not find regular posts insertion point")
            return False
        
        regular_insertion_point += len('<!-- Regular Blog Posts -->')
        
        # Build new content
        new_content = (
            content_without_featured[:featured_insertion_point] + 
            '\n                        ' + new_featured_html + '\n\n                        ' +
            content_without_featured[featured_insertion_point:regular_insertion_point]
        )
        
        # Add current featured post as regular post (if it exists)
        if current_featured_html:
            new_content += '\n                        ' + current_featured_html + '\n\n'
        
        new_content += content_without_featured[regular_insertion_point:]
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error promoting post to featured: {e}")
        return False


def add_regular_post_to_index(card_html, index_path):
    """Add the post card to regular posts section in index.html."""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the insertion point for regular posts
        insertion_point = content.find('<!-- Regular Blog Posts -->')
        
        if insertion_point == -1:
            print("❌ Could not find insertion point in index.html")
            print("💡 Look for '<!-- Regular Blog Posts -->' comment")
            return False
        
        insertion_point += len('<!-- Regular Blog Posts -->')
        
        # Insert the card HTML after the comment
        new_content = (
            content[:insertion_point] + 
            '\n                        ' + card_html + '\n\n' +
            content[insertion_point:]
        )
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating index.html: {e}")
        return False


def main():
    """Main function to generate post card and add to index."""
    print("🎯 GTM Engineering Blog - Post Card Generator")
    print("=" * 50)
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    posts_dir = project_root / "posts"
    index_path = project_root / "index.html"
    
    if not index_path.exists():
        print(f"❌ index.html not found at {index_path}")
        sys.exit(1)
    
    # Get post filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename.endswith('.html'):
            filename = filename[:-5]  # Remove .html extension
    else:
        print("📝 Available posts:")
        for post_file in posts_dir.glob("*.html"):
            print(f"  - {post_file.stem}")
        print()
        filename = input("📄 Enter post filename (without .html): ").strip()
    
    if not filename:
        print("❌ Filename is required!")
        sys.exit(1)
    
    post_path = posts_dir / f"{filename}.html"
    
    if not post_path.exists():
        print(f"❌ Post not found at {post_path}")
        sys.exit(1)
    
    try:
        # Read the HTML post
        with open(post_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract metadata
        post_data = extract_meta_from_html(html_content)
        
        if not post_data.get('title'):
            print("❌ Could not extract title from HTML post")
            print("💡 Make sure the post has a <title> tag or <h1> tag")
            sys.exit(1)
        
        print(f"📖 Title: {post_data['title']}")
        print(f"👤 Author: {post_data['author']}")
        print(f"📝 Description: {post_data.get('description', 'N/A')[:50]}...")
        print(f"🏷️  Tags: {', '.join(post_data['tags'])}")
        if post_data.get('image_url'):
            print(f"🖼️  Image: {post_data['image_url']}")
        else:
            print("🎨 Image: Will use gradient background")
        
        # Ask user what to do
        print("\n🎯 Options:")
        print("1. Promote to FEATURED POST (moves current featured to regular)")
        print("2. Add as regular post")
        print("3. Save HTML to file for manual addition")
        
        choice = input("\nChoose option (1/2/3): ").strip()
        
        if choice == "1":
            # Generate featured post HTML
            card_html = create_post_card_html(post_data, filename, is_featured=True)
            if promote_post_to_featured(card_html, index_path):
                print(f"✅ Post promoted to FEATURED on index.html")
                print("🎉 Your blog post is now the featured article!")
            else:
                print("❌ Failed to promote post to featured")
                sys.exit(1)
        
        elif choice == "2":
            # Generate regular post HTML
            card_html = create_post_card_html(post_data, filename, is_featured=False)
            if add_regular_post_to_index(card_html, index_path):
                print(f"✅ Post card added as regular post to index.html")
                print("🎉 Your blog post card is now live!")
            else:
                print("❌ Failed to add card to index.html")
                sys.exit(1)
        
        elif choice == "3":
            # Save to temporary files (both versions)
            featured_card = create_post_card_html(post_data, filename, is_featured=True)
            regular_card = create_post_card_html(post_data, filename, is_featured=False)
            
            featured_path = project_root / f"featured-post-{filename}.html"
            regular_path = project_root / f"regular-post-{filename}.html"
            
            with open(featured_path, 'w', encoding='utf-8') as f:
                f.write(featured_card)
            with open(regular_path, 'w', encoding='utf-8') as f:
                f.write(regular_card)
            
            print(f"✅ Featured post HTML saved to: {featured_path}")
            print(f"✅ Regular post HTML saved to: {regular_path}")
            print("📋 Use the appropriate HTML for your needs")
        
        else:
            print("❌ Invalid choice")
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error processing post: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()