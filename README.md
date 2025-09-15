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

### Create a new post

```bash
python scripts/new-post.py            # publish-ready file into posts/
python scripts/new-post.py --draft    # draft into drafts/ (noindex)
```

Drafts are available at `/drafts/` behind Basic Auth. Publish later:

```bash
python scripts/publish-draft.py <slug> [--featured]
```

If not using drafts, add the card to the homepage:

```bash
python scripts/add-post-card.py <slug> --auto --mode regular
```

### Updating styles

- Edit `styles.css` (CSS variables and utilities provided)

### Adding images

- Place image assets in `assets/` and reference them relatively (e.g. `../assets/image.webp`)

### Navigation

- Update links in header/footer of `index.html` and the post template (`.templates/post-template.html`)

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
