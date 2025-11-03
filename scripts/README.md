# Blog Publishing Scripts

Documentation for GTM Engineering blog publishing automation and tools.

---

## Quick Reference

### Core User Commands

```bash
# Create new post (3 modes)
python scripts/new-post.py                # Direct publish
python scripts/new-post.py --draft        # Draft mode
python scripts/new-post.py --markdown     # Markdown helper

# Publish draft (auto-updates metadata)
python scripts/publish-draft.py my-post           # Regular post
python scripts/publish-draft.py my-post --featured  # Featured post
```

---

## Active Scripts (7 Total)

### 🎯 User-Facing Commands

#### `new-post.py`

**Purpose:** Create new blog posts with interactive prompts

**Modes:**

-   Direct publish: `python scripts/new-post.py`
-   Draft mode: `python scripts/new-post.py --draft`
-   Markdown helper: `python scripts/new-post.py --markdown`

**Features:**

-   Custom slug override
-   Auto-generates meta tags
-   **NEW: FAQ JSON input** - Paste complete FAQPage schema or use interactive mode
-   **NEW: Custom BlogPosting schema** - Override default schema with custom JSON
-   **NEW: Custom ItemList schema** - Add structured data for related content
-   **NEW: Dynamic schema generation** - Uses @graph for multiple schemas
-   Color scheme selection
-   Noindex injection for drafts

**FAQ Input Modes:**

-   `y` - Interactive line-by-line (up to 3 FAQs)
-   `json` - Paste complete Schema.org FAQPage JSON (multiline, Ctrl+D to finish)
-   `N` - Skip FAQs

**Depends on:** `lib/shared.py`, `lib/manifest.py`

---

#### `publish-draft.py`

**Purpose:** Publish draft posts to production

**Usage:**

```bash
python scripts/publish-draft.py <slug> [--featured]
```

**What it does:**

1. **NEW: Recalculates reading time** from actual HTML content
2. Updates reading time placeholder in post HTML
3. Moves draft from `drafts/` to `posts/`
4. Removes from drafts manifest
5. Adds post card to `index.html`
6. **Automatically updates blog metadata** (related posts)
7. Shows success message with post URL

**Depends on:** `lib/manifest.py`, `lib/shared.py`, calls `add-post-card.py`, calls `update-blog-metadata.py`

---

### 🤖 CI/CD Automation Scripts

#### `ensure-noindex.py`

**Purpose:** Enforce noindex meta tag on all draft files

**Called by:** `.github/workflows/blog.yml` (on every push)

**What it does:**

-   Scans `drafts/*.html` files
-   Injects `<meta name="robots" content="noindex,nofollow">` if missing
-   Prevents search engines from indexing unpublished content

**Status:** Active CI/CD automation

---

#### `build-draft-manifest.py`

**Purpose:** Rebuild `drafts/drafts.json` from actual files

**Called by:** `.github/workflows/blog.yml` (on every push)

**What it does:**

-   Scans `drafts/` directory
-   Extracts metadata from HTML files
-   Rebuilds manifest with current drafts
-   Sorts by creation date (newest first)

**Status:** Active CI/CD automation

**Note:** Can be replaced with `DraftsManifest.rebuild_from_files()` in future

---

#### `add-post-card.py`

**Purpose:** Add post cards to homepage `index.html`

**Called by:**

-   `.github/workflows/blog.yml` (CI/CD)
-   `.github/workflows/update-blog.yml` (CI/CD)
-   `publish-draft.py` (automatic)

**Modes:**

-   `--auto`: Automation mode (exit codes: 0=success, 1=error, 2=exists)
-   `--mode featured`: Promote to featured section
-   `--mode regular`: Add to regular posts section

**What it does:**

1. Extracts metadata from post HTML
2. Generates styled post card HTML
3. Inserts into `index.html`
4. Handles featured vs regular placement

**Status:** Active (CI/CD + called by other scripts)

---

#### `sort-post-cards.py`

**Purpose:** Automatically sort post cards in homepage by publish date (newest first)

**Called by:** `.github/workflows/blog-automation.yml` (Step 7 - runs after adding cards)

**What it does:**

-   Scans `posts/` directory to extract post slugs and publish dates
-   Reads `index.html` to find all post card HTML blocks
-   Extracts post slugs from `<a href="posts/SLUG.html">` links in cards
-   Sorts cards chronologically by `article:published_time` meta tag (newest first)
-   Orphaned cards (cards without matching post file) are moved to end of list
-   Writes reordered HTML back to `index.html`

**Exit codes:**

-   `0` = Success (cards sorted)
-   `1` = Error (CRITICAL - fails workflow)

**Depends on:** `lib/html_parser.py` (`get_all_posts()` function)

**Status:** Active CI/CD automation (critical for homepage order)

**Note:** Must run AFTER `add-post-card.py` to ensure all cards are present before sorting

---

#### `update-blog-metadata.py`

**Purpose:** Update `js/blog-posts-data.js` for related posts functionality

**Called by:** `publish-draft.py` (automatic)

**What it does:**

-   Extracts post metadata (title, tags, description, image)
-   Updates blog-posts-data.js
-   Enables "Related Articles" section on posts
-   Critical for SEO and post discovery

**Status:** Active (auto-called during publish)

**Note:** Previously manual, now automatic as of refactoring

---

## Shared Libraries

### `lib/shared.py`

**Purpose:** Common utilities used across scripts

**Functions:**

-   `slugify()` - Convert text to URL-friendly slugs
-   `validate_slug()` - Validate slug format
-   `validate_description_length()` - SEO description validation
-   `estimate_reading_time(content, strip_html=False)` - **UPDATED:** Calculate reading time with HTML stripping
-   `strip_html_tags(html_content)` - **NEW:** Remove HTML tags for accurate word counting
-   `parse_faq_json(json_str)` - **NEW:** Parse and validate FAQ JSON input
-   `parse_schema_json(json_str, schema_type)` - **NEW:** Parse and validate custom schemas
-   `generate_faq_schema_json(faqs)` - **NEW:** Generate FAQ schema from FAQ list
-   `get_color_scheme()` - Post card color schemes
-   `inject_noindex_meta()` - Add noindex tags to HTML
-   `get_current_date()` - Standardized date formatting

**Used by:** `new-post.py`, `publish-draft.py`, `add-post-card.py`

---

### `lib/html_parser.py`

**Purpose:** Unified HTML metadata extraction (single source of truth for parsing)

**Key Function:** `parse_post_metadata(file_path)` - Extract all metadata from blog post HTML

**Returns:**

```python
{
    "title": str,              # From <title> or <h1>
    "description": str,        # From meta description
    "author": str,             # From meta author
    "tags": list[str],         # From keywords (first 3, title-cased)
    "image": str,              # From og:image (converted to relative)
    "image_alt": str,          # From og:image:alt or twitter:image:alt
    "publish_date": datetime,  # From article:published_time or JSON-LD
    "excerpt": str,            # First 3 paragraphs of content
    "filename": str,           # Stem without extension
    "url": str,                # Relative: filename.html
    "full_url": str,           # Absolute with domain
}
```

**Features:**

-   Handles reversed attribute order in meta tags
-   Multiple date format support (ISO 8601)
-   **Enhanced date parsing** - Uses `datetime.fromisoformat()` with fallback to format string parsing
-   JSON-LD schema parsing for publish dates
-   File modification time fallback
-   Robust error handling and fallbacks

**Used by:** `add-post-card.py`, `sort-post-cards.py`, `update-blog-metadata.py`, `generate-sitemap.py`, `generate-rss-feed.py`

---

### `lib/manifest.py`

**Purpose:** Centralized manifest management (single source of truth)

**Class:** `DraftsManifest`

**Methods:**

-   `add_entry()` - Add/update draft entry
-   `remove_entry()` - Remove draft entry
-   `get_entry()` - Get specific entry
-   `get_all_entries()` - Get all entries
-   `rebuild_from_files()` - Rebuild manifest from directory
-   `cleanup_orphaned_entries()` - Remove orphaned entries

**Used by:** `new-post.py`, `publish-draft.py`

---

## Script Dependencies Map

```
CI/CD Workflows
├── .github/workflows/blog.yml
│   ├── ensure-noindex.py
│   ├── build-draft-manifest.py
│   └── add-post-card.py
└── .github/workflows/update-blog.yml
    └── add-post-card.py

User Commands
├── new-post.py
│   └── Uses: lib/shared.py, lib/manifest.py
└── publish-draft.py
    ├── Uses: lib/manifest.py
    ├── Calls: add-post-card.py (automatic)
    └── Calls: update-blog-metadata.py (automatic)
```

---

## Recently Deleted Scripts

### `cleanup-draft-manifest.py` ❌ Deleted 2025-10-30

**Reason:** Functionality exists in `lib/manifest.py` as `cleanup_orphaned_entries()`

**Replacement:**

```python
from lib.manifest import DraftsManifest
manifest = DraftsManifest(project_root)
count = manifest.cleanup_orphaned_entries()
```

---

### `convert-markdown-to-html.py` ❌ Deleted 2025-10-30

**Reason:** Merged into `new-post.py --markdown`

**Replacement:**

```bash
# Old command
python scripts/convert-markdown-to-html.py

# New command
python scripts/new-post.py --markdown
```

---

### `publishing-checklist.py` ❌ Deleted 2025-10-30

**Reason:** Optional validation tool never automated

**Replacement:** Manual validation via:

-   Check content marker replaced
-   Verify meta tags present
-   Ensure featured image exists
-   Test locally before pushing

---

## Publishing Workflow

### Full Workflow Diagram

```
1. Create Post
   └── python scripts/new-post.py [--draft|--markdown]
       └── Uses: lib/shared.py, lib/manifest.py

2. Edit Content
   └── Open HTML file in editor
   └── Replace <!-- BLOG_POST_CONTENT_HERE --> marker

3. Publish Draft
   └── python scripts/publish-draft.py <slug> [--featured]
       ├── Moves to posts/
       ├── Removes from drafts manifest (lib/manifest.py)
       ├── Calls: add-post-card.py (automatic)
       └── Calls: update-blog-metadata.py (automatic)

4. Commit & Push
   └── git commit && git push
       └── CI/CD Triggers:
           ├── ensure-noindex.py (draft protection)
           ├── build-draft-manifest.py (sync manifest)
           └── add-post-card.py (homepage sync)

5. Production
   └── Static site deployed
   └── RSS/Sitemap auto-updated
```

---

## Development Guidelines

### Adding New Scripts

1. **Use shared utilities** from `lib/shared.py` and `lib/manifest.py`
2. **Add to CI/CD** if automation is needed (`.github/workflows/`)
3. **Document here** in scripts/README.md
4. **Test locally** before committing

### Modifying Existing Scripts

1. **Check dependencies** - What calls this script?
2. **Preserve exit codes** - CI/CD depends on them
3. **Update documentation** - Keep README current
4. **Test CI/CD** - Verify workflows don't break

---

## Testing Scripts Locally

```bash
# Syntax validation
python3 -m py_compile scripts/<script-name>.py

# Import test
python3 -c "from scripts.lib import shared, manifest"

# Full workflow test
python scripts/new-post.py --draft
# ... edit content ...
python scripts/publish-draft.py test-post

# Clean up test
rm posts/test-post.html
git checkout index.html js/blog-posts-data.js
```

---

## Troubleshooting

### "Module not found: lib.shared"

**Solution:**

```bash
# Verify lib/ exists
ls scripts/lib/

# Should show: __init__.py, shared.py, manifest.py
```

### "Draft not found"

**Solution:**

```bash
# Check drafts directory
ls drafts/

# Verify slug matches filename (without .html)
python scripts/publish-draft.py my-post
# Looks for: drafts/my-post.html
```

### CI/CD Workflow Failing

**Solution:**

1. Check GitHub Actions logs
2. Verify scripts still exist: `ensure-noindex.py`, `build-draft-manifest.py`, `add-post-card.py`
3. Test scripts locally
4. Check for syntax errors

---

## Performance Notes

-   **Shared libraries** add <1ms overhead
-   **Metadata updates** now automatic (saves manual step)
-   **CI/CD unchanged** - same performance as before
-   **Exit codes preserved** - automation compatible

---

## Security Considerations

-   ✅ No external dependencies added
-   ✅ Validation centralized in `lib/shared.py`
-   ✅ No changes to file permissions
-   ✅ Draft protection via noindex enforced in CI/CD

---

## Version History

### v2.2.0 (2025-11-03) - Metadata Extraction Consolidation

**What Changed:**

-   ✅ **Unified metadata extraction** - All scripts now use `lib/html_parser.py` as single source of truth
-   ✅ **Removed duplicate code** - Eliminated ~153 lines of redundant regex parsing
-   ✅ **Improved robustness** - Better handling of edge cases (reversed attributes, multiple date formats)
-   ✅ **Consistent behavior** - All scripts extract metadata the same way
-   ✅ **Added publish date** - Now available in add-post-card.py and update-blog-metadata.py
-   ✅ **Added image alt text** - Extracted from og:image:alt and twitter:image:alt

**Why These Changes:**

1. **Code duplication** - `add-post-card.py` and `update-blog-metadata.py` had nearly identical extraction logic
2. **Maintenance burden** - Bug fixes needed in 3 places, inconsistent implementations
3. **Missing features** - Some scripts had robust parsing, others didn't
4. **Technical debt** - Violated DRY (Don't Repeat Yourself) principle

**Files Modified:**

-   `scripts/add-post-card.py` - Removed 88 lines (local utilities + extraction logic)
-   `scripts/update-blog-metadata.py` - Removed 65 lines (duplicate extraction function)
-   `scripts/README.md` - Updated documentation for unified approach

**Breaking Changes:** None - all scripts maintain backward compatibility

**Benefits:**

-   Future metadata changes only need updating in one place
-   Bug fixes benefit all scripts automatically
-   New fields available everywhere (publish date, image alt)
-   Easier to maintain and debug

### v2.1.0 (2025-10-31) - Schema & Reading Time Improvements

**What Changed:**

-   ✅ **FAQ JSON input** - Paste complete Schema.org FAQPage JSON instead of line-by-line
-   ✅ **Custom BlogPosting schema** - Override default with custom JSON
-   ✅ **Custom ItemList schema** - Add structured data for lists
-   ✅ **Automatic reading time** - Calculated from actual HTML content at publish
-   ✅ **Dynamic schema generation** - Uses @graph for multiple schemas
-   ✅ **BlogPosting type** - Changed from generic "Article" to "BlogPosting"

**Why These Changes:**

1. **FAQ JSON input** - Reduces friction for posts with complex FAQs, enables automation
2. **Custom schemas** - Flexibility for advanced SEO customization
3. **Reading time calc** - Accurate estimates based on actual content, not guesses
4. **Dynamic schemas** - Proper handling of multiple schema types per page

**Breaking Changes:** None - all changes are backward compatible

**Keywords Question Answered:**

-   Keywords are kept as manual input (per user preference)
-   Used for `<meta name="keywords">` tag and Schema.org keywords field
-   While Google doesn't use keywords for ranking, they help with semantic understanding
-   Default fallback: "GTM engineering, go-to-market, RevOps"

### v2.0.0 (2025-10-30) - Refactoring

-   Created shared libraries (`lib/shared.py`, `lib/manifest.py`)
-   Merged `convert-markdown-to-html.py` into `new-post.py --markdown`
-   Auto-metadata updates in `publish-draft.py`
-   Deleted 3 redundant scripts
-   9 scripts → 6 scripts (33% reduction)

### v1.0.0 (Initial)

-   9 independent scripts
-   Manual metadata updates
-   Code duplication across scripts

---

## FAQ JSON Example

When using FAQ JSON input mode, paste this format:

```json
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "What is AI cold calling software?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "AI cold calling software is a category of tools that uses artificial intelligence to automate parts or all of the cold calling process."
            }
        },
        {
            "@type": "Question",
            "name": "Is AI cold calling legal and ethical?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes, when used correctly. The legalities are governed by regulations like the TCPA in the United States."
            }
        }
    ]
}
```

Press Ctrl+D (Unix/Mac) or Ctrl+Z+Enter (Windows) to finish input.

---

**Last Updated:** 2025-10-31
**Total Scripts:** 6 active + 2 shared libraries
**CI/CD Integration:** 3 scripts automated
**User Commands:** 2 main entry points
