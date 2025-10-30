#!/usr/bin/env python3
"""
GTM Engineering Blog - New Post Creator
Simple script to create new blog posts from template with interactive prompts.
"""

import json
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


def estimate_reading_time(content):
    """Estimate reading time based on word count (average 200 words per minute)."""
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return minutes


def create_post_card_html(post_data):
    """Generate HTML for the blog post card to add to index.html."""
    return f'''
            <article class="post-card">
              <div
                class="post-card-image"
                style="
                  background: linear-gradient(135deg, #{post_data["color1"]} 0%, #{post_data["color2"]} 100%);
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
                {post_data["card_label"]}
              </div>
              <div class="post-card-content">
                <h3 class="post-card-title">
                  <a href="posts/{post_data["filename"]}.html"
                    >{post_data["title"]}</a
                  >
                </h3>
                <p class="post-card-excerpt">
                  {post_data["excerpt"]}
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
                    {post_data["date"]}
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
              </div>
            </article>'''


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


def validate_description_length(description):
    """Validate meta description is within SEO best practice range (150-160 chars)."""
    if len(description) < 120:
        print(f"⚠️  Warning: Description is short ({len(description)} chars). Consider 150-160 for SEO.")
    elif len(description) > 160:
        print(f"⚠️  Warning: Description is long ({len(description)} chars). Consider trimming to 160.")
        return False
    return True


def get_author_info():
    """Get author information including bio/social URL for E-E-A-T."""
    author = input("👤 Author name (default: Jorge Macias): ").strip() or "Jorge Macias"

    if author == "Jorge Macias":
        author_url = "https://www.linkedin.com/in/jorge-b-macias"
        print(f"📝 Using default LinkedIn: {author_url}")
    else:
        author_url = input("🔗 Author bio/LinkedIn URL (for E-E-A-T): ").strip()
        if not author_url:
            print("⚠️  Warning: No author URL provided. This helps with E-E-A-T for SEO.")

    return author, author_url


def get_faq_data():
    """Get FAQ data for rich snippets and improved SEO."""
    print("\n🙋 FAQ Section (optional - improves SEO with rich snippets)")
    print("=" * 60)

    add_faq = input("Add FAQ section? This helps with rich snippets (y/N): ").strip().lower()

    if add_faq != "y":
        return []

    print("\n📝 Enter 3 FAQs (questions should match likely search queries):")
    print("⚠️  CRITICAL: FAQ content must be visible on the page (Google requirement)")

    faqs = []
    for i in range(1, 4):
        print(f"\n--- FAQ {i} ---")
        question = input(f"❓ Question {i}: ").strip()
        if not question:
            print("Skipping remaining FAQs...")
            break

        answer = input(f"✅ Answer {i}: ").strip()
        if not answer:
            print("⚠️  Empty answer, skipping this FAQ")
            continue

        # Validate answer length
        if len(answer) < 50:
            print(f"⚠️  Answer is short ({len(answer)} chars). Consider more detail for better SEO.")
        elif len(answer) > 500:
            print(f"⚠️  Answer is long ({len(answer)} chars). Consider being more concise.")

        faqs.append({"question": question, "answer": answer})

    if faqs:
        print(f"\n✅ Added {len(faqs)} FAQs for rich snippet optimization")
        print("💡 Remember: FAQ content must appear visibly on your page!")

    return faqs


def create_faq_html(faqs):
    """Generate HTML for FAQ section that must be visible on page."""
    if not faqs:
        return ""

    html = """
        <!-- FAQ Section (Required for Schema.org compliance) -->
        <section class="faq-section">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-container">
"""

    for i, faq in enumerate(faqs, 1):
        html += f"""
                <div class="faq-item">
                    <h3 class="faq-question">{faq["question"]}</h3>
                    <div class="faq-answer">
                        <p>{faq["answer"]}</p>
                    </div>
                </div>
"""

    html += """
            </div>
        </section>

        <style>
        .faq-section {
            margin: 3rem 0;
            padding: 2rem;
            background-color: #f8f9fa;
            border-radius: 8px;
        }

        .faq-section h2 {
            color: #2563eb;
            margin-bottom: 2rem;
            font-size: 1.75rem;
        }

        .faq-item {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: white;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .faq-question {
            color: #1e40af;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
        }

        .faq-answer p {
            color: #374151;
            line-height: 1.6;
            margin: 0;
        }
        </style>
"""

    return html


def inject_noindex_meta(html_content):
    """Insert a noindex/nofollow meta tag into <head> for draft posts."""
    # Only add if not already present
    if re.search(r'<meta\s+name="robots"', html_content, re.IGNORECASE):
        return html_content
    return re.sub(
        r"(<head[^>]*>)",
        r'\1\n        <meta name="robots" content="noindex,nofollow" />',
        html_content,
        count=1,
        flags=re.IGNORECASE,
    )


def update_drafts_manifest(project_root: Path, post_data: dict):
    """Create/update drafts/drafts.json with this draft's metadata."""
    drafts_dir = project_root / "drafts"
    drafts_dir.mkdir(exist_ok=True)
    manifest_path = drafts_dir / "drafts.json"

    # Load existing manifest
    manifest = []
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(manifest, list):
                manifest = []
        except Exception:
            manifest = []

    # Remove existing entry with same slug
    manifest = [item for item in manifest if item.get("slug") != post_data["filename"]]

    # Add new entry
    manifest.append(
        {
            "slug": post_data["filename"],
            "title": post_data["title"],
            "url": f"{post_data['filename']}.html",
            "author": post_data["author"],
            "excerpt": post_data["excerpt"],
            "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )

    # Sort newest first
    try:
        manifest.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
    except Exception:
        pass

    # Write manifest
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def create_post_metadata(title, author, author_url, excerpt, keywords, tags, reading_time, faqs, custom_slug=None):
    """Create centralized post metadata to prevent inconsistency issues."""
    current_date = datetime.now().strftime("%B %d, %Y")
    current_date_iso = datetime.now().strftime("%Y-%m-%d")
    filename = custom_slug if custom_slug else slugify(title)
    default_image = "gtm-revenue-system-illustration.webp"
    default_image_alt = (
        "3D isometric illustration of GTM strategy components including ICP, Sales, "
        "Marketing modules with a person optimizing the system"
    )

    # Get and validate description
    description = input("🔍 Meta description (150-160 chars optimal): ").strip()
    if not description:
        description = excerpt[:150] + "..." if len(excerpt) > 150 else excerpt

    validate_description_length(description)

    # Generate color scheme
    color1, color2, card_label = get_color_scheme()

    return {
        "title": title,
        "filename": filename,
        "author": author,
        "author_url": author_url,
        "date": current_date,
        "date_iso": current_date_iso,
        "description": description,
        "keywords": keywords,
        "excerpt": excerpt,
        "tags": tags,
        "category": tags[0] if tags else "Strategy",
        "reading_time": reading_time,
        "color1": color1,
        "color2": color2,
        "card_label": card_label,
        "faqs": faqs,
        # Images
        "featured_image": default_image,
        "featured_image_alt": default_image_alt,
        "hero_image": default_image,
        "hero_image_alt": default_image_alt,
        # Social
        "twitter_handle": "gtmengineering",
    }


def print_publishing_checklist(post_data):
    """Print a checklist to prevent inconsistency issues during publishing."""
    print("\n📋 Pre-Publishing Checklist:")
    print("=" * 40)
    print(f"✓ Title: {post_data['title']}")
    print(f"✓ Description: {post_data['description']} ({len(post_data['description'])} chars)")
    print(f"✓ Author: {post_data['author']}")
    if post_data.get("author_url"):
        print(f"✓ Author URL: {post_data['author_url']}")
    else:
        print("⚠️  Author URL: Not provided (affects E-E-A-T)")
    print(f"✓ Keywords: {post_data['keywords']}")
    print(f"✓ Category: {post_data['category']}")
    print(f"✓ Tags: {', '.join(post_data['tags'])}")
    print(f"✓ Reading time: {post_data['reading_time']} min")
    print("\n⚡ All meta fields will be auto-populated consistently!")


def validate_slug(slug):
    """Validate slug format: lowercase, alphanumeric, hyphens only, no leading/trailing hyphens."""
    if not slug:
        return False, "Slug cannot be empty"

    # Check for valid characters (lowercase, numbers, hyphens)
    if not re.match(r"^[a-z0-9-]+$", slug):
        return False, "Use lowercase letters, numbers, and hyphens only"

    # Check for leading/trailing hyphens
    if slug.startswith("-") or slug.endswith("-"):
        return False, "Slug cannot start or end with hyphens"

    # Check for consecutive hyphens
    if "--" in slug:
        return False, "Slug cannot contain consecutive hyphens"

    return True, ""


def check_slug_exists(project_root, slug, save_as_draft):
    """Check if slug already exists in posts or drafts."""
    posts_dir = project_root / "posts"
    drafts_dir = project_root / "drafts"

    # Check posts directory
    if (posts_dir / f"{slug}.html").exists():
        return True, "posts"

    # Check drafts directory
    if (drafts_dir / f"{slug}.html").exists():
        return True, "drafts"

    return False, None


def get_custom_slug(project_root, auto_slug, save_as_draft):
    """Prompt user for custom slug with validation."""
    while True:
        custom = input("\n✏️  Enter custom slug (lowercase, alphanumeric + hyphens only): ").strip()

        if not custom:
            print("❌ Slug cannot be empty. Try again or press Ctrl+C to cancel.")
            continue

        # Validate format
        is_valid, error_msg = validate_slug(custom)
        if not is_valid:
            print(f"❌ Invalid slug format: {error_msg}")
            continue

        # Check for conflicts
        exists, location = check_slug_exists(project_root, custom, save_as_draft)
        if exists:
            print(f"⚠️  Slug '{custom}' already exists in {location}/")
            retry = input("Try a different slug? (y/N): ").strip().lower()
            if retry != "y":
                print("❌ Cancelled.")
                sys.exit(1)
            continue

        return custom


def main():
    """Main function to create new blog post."""
    print("🚀 GTM Engineering Blog - New Post Creator")
    print("=" * 50)

    # Draft mode flag (keep simple, no argparse to avoid breaking interactive flow)
    save_as_draft = ("--draft" in sys.argv) or ("-d" in sys.argv)
    if save_as_draft:
        print("📝 Draft mode enabled: post will be saved under drafts/ and marked noindex")

    # Get project root directory
    project_root = Path(__file__).parent.parent
    template_path = project_root / ".templates" / "post-template.html"

    if not template_path.exists():
        print(f"❌ Post template not found at {template_path}")
        sys.exit(1)

    # Gather post information
    try:
        title = input("\n📝 Post title: ").strip()
        if not title:
            print("❌ Title is required!")
            sys.exit(1)

        # Generate auto-slug and offer customization
        auto_slug = slugify(title)
        print(f"📄 Filename will be: {auto_slug}.html")

        # Prompt for custom slug
        slug_choice = input("Use this slug? (Y/n/custom): ").strip().lower()

        if slug_choice == "n":
            print("❌ Cancelled. Please restart with a different title.")
            sys.exit(0)
        elif slug_choice == "custom":
            final_slug = get_custom_slug(project_root, auto_slug, save_as_draft)
            print(f"✅ Using custom slug: {final_slug}")
        else:
            # Default: use auto-generated slug
            final_slug = auto_slug
            print(f"✅ Using slug: {final_slug}")

        author, author_url = get_author_info()

        excerpt = input("📖 Brief excerpt (2-3 sentences): ").strip()
        if not excerpt:
            print("❌ Excerpt is required!")
            sys.exit(1)

        keywords = input("🏷️  Keywords (comma-separated): ").strip()
        if not keywords:
            keywords = "GTM engineering, go-to-market, RevOps"

        tags_input = input("🏷️  Tags (comma-separated): ").strip()
        if not tags_input:
            tags = ["Strategy"]
        else:
            tags = [tag.strip() for tag in tags_input.split(",")]

        reading_time = input("⏱️  Reading time estimate (default: 5 min): ").strip() or "5"

        # Get FAQ data for rich snippets
        faqs = get_faq_data()

        # Create centralized post metadata
        post_data = create_post_metadata(
            title, author, author_url, excerpt, keywords, tags, reading_time, faqs, custom_slug=final_slug
        )

        print(f"🎨 Color scheme: {post_data['card_label']}")
        print_publishing_checklist(post_data)

    except KeyboardInterrupt:
        print("\n❌ Cancelled by user.")
        sys.exit(1)

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Replace placeholders using centralized data
    replacements = {
        "[BLOG POST TITLE]": post_data["title"],
        "[AUTHOR NAME]": post_data["author"],
        "[AUTHOR_BIO_URL]": post_data.get("author_url", "https://www.linkedin.com/in/jorge-b-macias"),
        "[PUBLICATION DATE]": post_data["date"],
        "[PUBLICATION DATE in YYYY-MM-DD format]": post_data["date_iso"],
        "[LAST MODIFIED DATE in YYYY-MM-DD format]": post_data["date_iso"],
        "[X] min read": f"{post_data['reading_time']} min read",
        "[WRITE A COMPELLING 150-160 CHARACTER DESCRIPTION OF THIS BLOG POST]": post_data["description"],
        "[WRITE A COMPELLING DESCRIPTION FOR SOCIAL SHARING]": post_data["description"],
        "[WRITE A COMPELLING DESCRIPTION FOR TWITTER SHARING]": post_data["description"],
        "[WRITE A COMPELLING DESCRIPTION]": post_data["description"],
        "[KEYWORD1], [KEYWORD2], [KEYWORD3]": post_data["keywords"],
        "[KEYWORD1], [KEYWORD2], [KEYWORD3], GTM engineering, go-to-market": post_data["keywords"]
        + ", GTM engineering, go-to-market",
        "[CATEGORY]": post_data["category"],
        "[TAG]": post_data["tags"][1] if len(post_data["tags"]) > 1 else "GTM",
        "[POST-FILENAME]": post_data["filename"],
        "[POST-TITLE]": post_data["title"],
        # Images
        "[POST-FEATURED-IMAGE]": post_data.get("featured_image", "gtm-revenue-system-illustration.webp"),
        "[HERO-IMAGE-FILENAME]": post_data.get("hero_image", "gtm-revenue-system-illustration.webp"),
        "Jorge Macias": post_data["author"],  # Update default author if different
        # FAQ Schema placeholders
        "[FAQ_QUESTION_1]": post_data["faqs"][0]["question"] if len(post_data["faqs"]) > 0 else "",
        "[FAQ_ANSWER_1]": post_data["faqs"][0]["answer"] if len(post_data["faqs"]) > 0 else "",
        "[FAQ_QUESTION_2]": post_data["faqs"][1]["question"] if len(post_data["faqs"]) > 1 else "",
        "[FAQ_ANSWER_2]": post_data["faqs"][1]["answer"] if len(post_data["faqs"]) > 1 else "",
        "[FAQ_QUESTION_3]": post_data["faqs"][2]["question"] if len(post_data["faqs"]) > 2 else "",
        "[FAQ_ANSWER_3]": post_data["faqs"][2]["answer"] if len(post_data["faqs"]) > 2 else "",
        # FAQ HTML section
        "[FAQ_SECTION_HTML]": create_faq_html(post_data["faqs"]),
    }

    # Apply replacements
    post_content = template_content
    for placeholder, replacement in replacements.items():
        post_content = post_content.replace(placeholder, replacement)

    # Create the new post file
    posts_dir = project_root / ("drafts" if save_as_draft else "posts")
    posts_dir.mkdir(exist_ok=True)  # Ensure posts directory exists
    post_path = posts_dir / f"{post_data['filename']}.html"

    if post_path.exists():
        overwrite = input(f"⚠️  Post '{post_data['filename']}.html' already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("❌ Cancelled.")
            sys.exit(1)

    # If draft, inject noindex meta
    if save_as_draft:
        post_content = inject_noindex_meta(post_content)

    # Write the post file
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(post_content)

    print(f"✅ Created new post: {post_path}")

    # Update drafts manifest if draft
    if save_as_draft:
        update_drafts_manifest(project_root, post_data)

    if not save_as_draft:
        # Generate post card HTML for manual addition to index.html
        post_card_html = create_post_card_html(post_data)

        # Save the post card HTML to a temporary file
        card_path = project_root / f"new-post-card-{post_data['filename']}.html"
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(post_card_html)

        print(f"✅ Generated post card HTML: {card_path}")

    # Instructions
    print("\n🎉 Your new blog post is ready!")
    if save_as_draft:
        slug = post_data["filename"]
        print(f"📝 Edit the content in: drafts/{slug}.html")
        print("\n📋 Next steps:")
        print(f"1. Share the private URL: /drafts/{slug}.html (password required)")
        print(f"2. When approved, publish with: python scripts/publish-draft.py {slug}")
    else:
        print(f"📝 Edit the content in: posts/{post_data['filename']}.html")
        print(f"🔧 Add the post card to index.html (HTML saved to: new-post-card-{post_data['filename']}.html)")
        print("\n📋 Next steps:")
        print("1. Open the new post file and replace placeholder content with your article")
        print("2. Copy the post card HTML from the generated file into index.html")
        print("3. Test locally by opening index.html in your browser")
        print("4. Commit and push to deploy!")
    print("\n🔥 SEO Benefits:")
    print("✓ All meta descriptions auto-populated consistently")
    print("✓ Author E-E-A-T enhanced with bio URL")
    print("✓ Schema.org structured data included")
    print("✓ Social media tags optimized")
    print("\n💡 Tip: All SEO fields are now centrally managed to prevent inconsistencies!")


if __name__ == "__main__":
    main()
