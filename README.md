# GTM Engineering Blog

A professional blog site that matches the GTM Engineering website design and branding.

## Structure

```
blog/
├── index.html          # Main blog listing page
├── styles.css          # Complete CSS framework
├── posts/              # Individual blog posts
│   └── *.html         # Blog post files
├── assets/             # Images, icons, and other resources
└── README.md          # This file
```

## Features

### Design & Branding

-   Matches GTM Engineering website color scheme and typography
-   Responsive design optimized for mobile and desktop
-   Professional, clean aesthetic with focus on readability
-   GTM Engineering blue (#3873C1) as primary brand color

### Header & Navigation

-   GTM Engineering logo (text-based)
-   Navigation menu: Services, Case Studies, Proof, GTME Blog
-   Blue "Book Call" CTA button linking to Calendly
-   Mobile-responsive hamburger menu

### Blog Functionality

-   Featured post section with larger display
-   Grid layout for blog post cards
-   Category filtering (basic implementation)
-   Post metadata: date, author, tags
-   Hover effects and smooth transitions
-   SEO-optimized structure

### Footer

-   Blue footer matching main site theme
-   Links to LinkedIn, Case Studies, Services, Proof
-   Copyright notice and Privacy Policy link
-   Structured footer with four columns

## Sample Content

The blog includes sample posts covering GTM engineering topics:

-   "Building Scalable Outbound Engines That Actually Convert" (full post)
-   "Clay Workflows That Actually Drive Revenue"
-   "RevOps Setup for Startups: The 90-Day Playbook"
-   "Modern GTM Data Infrastructure: Beyond Salesforce"
-   "5 Levers That Actually Improve Sales Velocity"
-   "Attribution Modeling for B2B: What Actually Works"

## Technical Details

### CSS Framework

-   CSS custom properties for consistent theming
-   Mobile-first responsive design
-   Grid and flexbox layouts
-   Comprehensive utility classes
-   Accessibility features (focus states, screen reader support)
-   Print styles included

### Performance

-   Semantic HTML structure
-   Optimized for Core Web Vitals
-   Lightweight CSS (no external frameworks)
-   Efficient image placeholders

### SEO

-   Proper meta tags and structured data
-   Semantic HTML elements
-   Accessible markup with ARIA labels
-   Fast loading times

## Usage

### Create a new post (Manual Workflow)

**Quick workflow** - Create HTML file directly:

1. Create `posts/my-post.html` using `.templates/post-template.html`
2. Add `assets/my-post.webp` featured image
3. Commit and push to `main` branch
4. **Automatic CI/CD handles**:
    - ✅ Sitemap.xml updated
    - ✅ RSS feed.xml updated
    - ✅ Blog metadata (related articles) updated
    - ✅ Homepage post card added
    - ✅ Most recent post auto-featured

**Script-assisted workflow** - Using helper scripts:

```bash
python scripts/new-post.py            # publish-ready file into posts/
python scripts/new-post.py --draft    # draft into drafts/ (noindex)
```

Drafts are available at `/drafts/` behind Basic Auth. Publish later:

```bash
python scripts/publish-draft.py <slug> [--featured]
```

If not using drafts, manually add the card to the homepage:

```bash
python scripts/add-post-card.py <slug> --auto --mode regular
```

### Automated CI/CD Workflow

The blog has a **unified GitHub Actions workflow** (`.github/workflows/blog-automation.yml`) that automatically:

1. **Draft Protection**: Ensures all drafts have `noindex` meta tags
2. **Sitemap Generation**: Creates `sitemap.xml` from all posts (sorted by publish date)
3. **RSS Feed Generation**: Creates `feed.xml` with full post content
4. **Metadata Updates**: Updates `js/blog-posts-data.js` for related articles
5. **Homepage Updates**: Adds missing post cards to `index.html`
6. **Featured Post**: Automatically promotes the most recent post to featured section

**Triggers**: Any push to `main` branch affecting:

-   `posts/**` - Blog post files
-   `drafts/**` - Draft files
-   `scripts/**` - Automation scripts
-   `assets/**` - Images and resources
-   `.templates/**` - Post templates

**Manual triggers** (local testing):

```bash
# Generate sitemap.xml
python scripts/generate-sitemap.py

# Generate feed.xml (RSS)
python scripts/generate-rss-feed.py

# Update all post metadata
python scripts/update-blog-metadata.py --all

# Update specific post metadata
python scripts/update-blog-metadata.py my-post
```

### Updating styles

-   Edit `styles.css` (CSS variables and utilities provided)

### Adding images

-   Place image assets in `assets/` and reference them relatively (e.g. `../assets/image.webp`)

### Navigation

-   Update links in header/footer of `index.html` and the post template (`.templates/post-template.html`)

## Browser Support

-   Modern browsers (Chrome, Firefox, Safari, Edge)
-   Internet Explorer 11+ (with fallbacks)
-   Mobile browsers (iOS Safari, Android Chrome)

## Accessibility

-   WCAG 2.1 AA compliant
-   Keyboard navigation support
-   Screen reader optimized
-   High contrast mode support
-   Reduced motion preferences respected
