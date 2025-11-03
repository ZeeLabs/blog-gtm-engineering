# Quick Start Guide - Refactored Blog System

## TL;DR

```bash
# Create new post (3 modes available)
python scripts/new-post.py                    # Direct publish
python scripts/new-post.py --draft            # Draft mode
python scripts/new-post.py --markdown         # Markdown helper

# Publish draft (auto-updates metadata now!)
python scripts/publish-draft.py my-post       # Regular post
python scripts/publish-draft.py my-post --featured  # Featured post

# That's it! Metadata updates automatically.
```

---

## What's New?

### ✅ Unified Post Creation

-   **One tool** instead of two (`new-post.py` replaces `convert-markdown-to-html.py`)
-   **Three modes:** publish, draft, markdown
-   **Custom slugs:** Optional manual URL override

### ✅ Automatic Metadata Updates

-   **No manual step** - `publish-draft.py` now auto-updates `blog-posts-data.js`
-   **Related posts work** automatically
-   **Graceful fallback** if metadata update fails

### ✅ Better Code Quality

-   **Shared utilities** eliminate duplication
-   **Centralized manifest** management
-   **Cleaner, maintainable** codebase

---

## Publishing Workflow

### Direct Publish (No Approval Needed)

```bash
# 1. Create post
python scripts/new-post.py
# Follow prompts: title, author, excerpt, tags, etc.

# 2. Edit content
# Open posts/your-post-slug.html
# Replace <!-- BLOG_POST_CONTENT_HERE --> with your HTML

# 3. Add to homepage
python scripts/add-post-card.py your-post-slug --featured

# 4. Commit & push
git add .
git commit -m "feat(blog): add new post - Your Title"
git push origin main
```

### Draft Workflow (With Approval)

```bash
# 1. Create draft
python scripts/new-post.py --draft
# Creates in drafts/ with noindex tag

# 2. Edit content
# Open drafts/your-post-slug.html
# Replace content marker with your HTML

# 3. Share for review
# URL: /drafts/your-post-slug.html

# 4. Publish when approved
python scripts/publish-draft.py your-post-slug --featured
# Automatically:
# - Moves to posts/
# - Adds to homepage
# - Updates metadata
# - Removes noindex

# 5. Commit & push
git add .
git commit -m "feat(blog): publish draft - Your Title"
git push origin main
```

### Markdown Conversion Workflow

```bash
# 1. Create draft with markdown helper
python scripts/new-post.py --markdown
# Shows AI conversion prompt

# 2. Convert markdown to HTML
# Copy your markdown
# Use AI prompt (shown in output)
# Paste result into draft file

# 3. Publish when ready
python scripts/publish-draft.py your-post-slug

# 4. Commit & push
git add .
git commit -m "feat(blog): publish post - Your Title"
git push origin main
```

---

## New Features

### Custom Slug Override

```bash
$ python scripts/new-post.py

📝 Post title: The Ultimate Guide to Sales Automation
📄 Filename will be: the-ultimate-guide-to-sales-automation.html
Use this slug? (Y/n/custom): custom

✏️  Enter custom slug: sales-automation-guide
✅ Using custom slug: sales-automation-guide
```

### Markdown Mode

```bash
$ python scripts/new-post.py --markdown

🎨 Markdown mode enabled: will create draft with AI conversion helper

# After creation, shows:
🤖 AI CONVERSION PROMPT:
Convert this markdown content to clean HTML...
[Full prompt provided]

🎯 HOW TO EDIT:
1. Open: drafts/your-slug.html
2. Find: <!-- BLOG_POST_CONTENT_HERE -->
3. Replace with AI-converted HTML
4. Publish with: python scripts/publish-draft.py your-slug
```

### Automatic Metadata Updates

```bash
$ python scripts/publish-draft.py my-post

✅ Moved draft to posts: /path/to/posts/my-post.html
✅ Removed from drafts manifest
✅ Added post card to index.html

📊 Updating blog metadata for related posts...
✅ Updated blog metadata

🎉 Post published successfully!
📝 Post URL: /posts/my-post.html
```

---

## Command Reference

### `new-post.py`

```bash
# Create published post directly
python scripts/new-post.py

# Create draft (with noindex)
python scripts/new-post.py --draft
python scripts/new-post.py -d       # Short form

# Create draft with markdown helper
python scripts/new-post.py --markdown
python scripts/new-post.py -m         # Short form
```

### `publish-draft.py`

```bash
# Publish as regular post
python scripts/publish-draft.py my-post

# Publish as featured post (top of homepage)
python scripts/publish-draft.py my-post --featured
```

### `add-post-card.py`

```bash
# Add regular post to homepage
python scripts/add-post-card.py my-post --auto

# Add as featured post
python scripts/add-post-card.py my-post --auto --mode featured
```

---

## Migration from Old System

### Old Commands → New Commands

```bash
# Markdown conversion (old)
python scripts/convert-markdown-to-html.py
↓
# Markdown conversion (new)
python scripts/new-post.py --markdown

# Publishing (old - manual metadata update)
python scripts/publish-draft.py my-post
python scripts/update-blog-metadata.py my-post  # Manual!
↓
# Publishing (new - automatic)
python scripts/publish-draft.py my-post
# Metadata updates automatically!
```

---

## Troubleshooting

### Issue: "Module not found: lib.shared"

**Solution:**

```bash
# Ensure scripts/lib/ exists
ls scripts/lib/

# Should show:
# __init__.py
# shared.py
# manifest.py

# If missing, pull latest changes
git pull origin main
```

### Issue: "Slug validation failed"

**Solution:**
Slugs must be:

-   Lowercase only
-   Letters, numbers, hyphens only
-   No leading/trailing hyphens
-   No consecutive hyphens

Valid: `my-blog-post-2024`
Invalid: `My_Blog-Post!!`

### Issue: "Draft not found"

**Solution:**

```bash
# Check drafts directory
ls drafts/

# Verify slug matches filename (without .html)
python scripts/publish-draft.py my-post
# Looks for: drafts/my-post.html
```

---

## CI/CD Integration

**No changes needed!** The CI/CD workflow remains unchanged:

```yaml
# GitHub Actions still works as before
- ensure-noindex.py # Validates drafts
- build-draft-manifest.py # Syncs manifest
- sitemap/RSS generation # Automatic
- sort-post-cards.py # Automatically sorts homepage post cards by publish date
```

**Note:** Post cards are automatically sorted chronologically (newest first) based on the `article:published_time` meta tag.

---

## Best Practices

### 1. Always Use Custom Slugs for SEO

```bash
# Good: Short, keyword-rich slug
sales-automation-guide

# Avoid: Auto-generated, too long
the-ultimate-comprehensive-guide-to-sales-automation-2024
```

### 2. Test Locally Before Pushing

```bash
# Serve locally
cd web
python -m http.server 8000

# Visit: http://localhost:8000
# Check: post renders correctly, links work
```

### 3. Validate Before Publishing

```bash
# Manual validation checklist:
# ✓ Content marker replaced (<!-- BLOG_POST_CONTENT_HERE -->)
# ✓ Featured image exists in assets/
# ✓ Meta tags present (<title>, <meta name="description">, etc.)
# ✓ Test locally: python -m http.server 8000
```

### 4. Use Drafts for Client Approval

```bash
# Create draft
python scripts/new-post.py --draft

# Share URL: /drafts/my-post.html
# Password protected automatically

# Publish when approved
python scripts/publish-draft.py my-post --featured
```

---

## FAQ

**Q: What happened to `convert-markdown-to-html.py`?**
A: Deleted - merged into `new-post.py --markdown`. Use the new command instead.

**Q: What if metadata update fails?**
A: Non-critical. Publish continues. You'll see a warning with manual command to retry.

**Q: Do I need to update CI/CD?**
A: No changes needed. All CI/CD scripts work as before.

**Q: Can I roll back changes?**
A: Yes. See `REFACTORING_SUMMARY.md` for rollback instructions.

**Q: Where's the old code?**
A: Git history. Use `git checkout HEAD~1 scripts/filename.py` to restore.

---

## Getting Help

1. **Read full details:** `REFACTORING_SUMMARY.md`
2. **Check module docs:** `scripts/lib/shared.py`, `scripts/lib/manifest.py`
3. **Test in staging:** Always test before production
4. **Check git history:** Compare with previous versions if needed

---

**Updated:** 2025-10-30
**Version:** 2.0.0 (Refactored)
