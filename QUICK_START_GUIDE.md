# How to Publish a Blog Post

This guide shows you how to publish a new blog post to the GTM Engineering blog. Everything is automated—you just place your files in the right locations, and the system handles the rest.

**⏱️ Time Estimate:** 5-10 minutes
**✅ Prerequisites:** You have your blog content written and featured image (WebP format) ready

---

## 📚 Understanding the Basics

Before we begin, let's clarify a few key terms:

### What is a "Slug"?

A **slug** is a URL-friendly version of your post title. It's what appears in the web address.

**Example:**

-   Post title: "GTM Engineering vs Revenue Operations for Startups"
-   Slug: `gtm-engineering-vs-revenue-operations-for-startups`

**Rules for slugs:**

-   Use lowercase letters only
-   Replace spaces with hyphens (`-`)
-   Remove special characters (!, ?, &, etc.)
-   Keep it descriptive but concise

### What is a "Commit"?

A **commit** is like saving your work in version control. When you commit files, you're telling GitHub "these are my changes, please save them."

### What is "Push"?

**Push** means uploading your commits from your local computer to GitHub's servers (only relevant if using command-line).

---

## 🎨 Creating Your HTML File (Recommended Method)

The easiest way to create your blog post HTML is using our **Google Gemini Gem**. This AI assistant converts your markdown content into a ready-to-use HTML file using our blog template.

### 🔗 Access the Gem

**[Open GTM Engineering Blog Post Generator](https://gemini.google.com/gem/1ze2i---UwT2rpDDlkg3bq1ztNS6cO3Dn?usp=sharing)**

### 📝 What You Need to Prepare

Before using the Gem, have these ready:

-   **Post title** (for meta title)
-   **Description** (150-160 characters for SEO)
-   **URL slug** (lowercase with hyphens, e.g., `/my-post-slug`)
-   **Blog content** (written in markdown format)
-   **Optional schema blocks** (the Gem can add these for SEO if needed)

### 💡 How to Use It

1. **Open the Gem link** above
2. **Copy and paste** your content in this format:

````markdown
---
**Meta Title:** `Your Compelling Post Title`
**Meta Description:** `A clear, engaging description of your post (150-160 chars)`
**URL Slug:** `/your-post-slug`
---

# Your Main Heading

Your blog post content goes here in markdown format.

## A Subheading

More content...

-   Bullet points work
-   Lists are supported
-   **Bold** and _italic_ formatting too

---

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Your Post Title",
  "description": "Your post description",
  "datePublished": "2025-11-03"
}
</script>
```

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Your question here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Your answer here."
      }
    }
  ]
}
</script>
```
````

**💡 Optional but recommended:** Include the schema blocks at the end (shown above) if your post has structured content like FAQs. These help search engines understand your content better.

3. **Send the message** to the Gem
4. **Copy the generated HTML** - The Gem outputs a complete HTML file ready to use
5. **Save it** as `your-post-slug.html` (matching your slug)

### ✅ What You Get

The Gem generates a complete HTML file with:

-   All required meta tags pre-filled
-   Your content properly formatted
-   The correct blog template structure
-   Ready to upload to the `posts/` folder

**Alternative:** If you prefer to work directly with HTML, you can copy the template from `.templates/post-template.html` and fill it in manually.

---

## ✅ Before You Start - Checklist

Make sure you have everything ready:

-   [ ] HTML file is created (using our Gemini Gem recommended above or from `.templates/post-template.html`)
-   [ ] Featured image is in WebP format (`.webp` extension)
-   [ ] Both files use the **same slug** (matching names)
    -   Example: `my-post.html` and `my-post.webp`
-   [ ] All metadata is filled in (publish date, keywords, description—see section below)

---

## 🚀 Publishing Methods (Choose One)

Pick the method you're most comfortable with:

<table>
<tr>
<th width="50%">📱 Method A: GitHub Web Interface (Beginner-Friendly)</th>
<th width="50%">⌨️ Method B: Command Line (For Developers)</th>
</tr>
<tr>
<td valign="top">

**Step 1: Upload Your HTML File**

1. Go to the repository on GitHub.com: [blog-gtm-engineering](https://github.com/zeelabs/blog-gtm-engineering)
2. Navigate to the `posts/` folder
3. Click **"Add file"** → **"Upload files"**
4. Drag and drop your `your-post-slug.html` file
5. Scroll down and add a commit message:
    ```
    Add new post: [Your Post Title]
    ```
6. Click **"Commit changes"**

**Step 2: Upload Your Featured Image**

1. Navigate to the `assets/` folder
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop your `your-post-slug.webp` file
4. Add a commit message:
    ```
    Add image for: [Your Post Title]
    ```
5. Click **"Commit changes"**

**Step 3: Wait for Automation**

-   GitHub Actions runs automatically (takes 1-2 minutes)
-   Check the **"Actions"** tab to see progress
-   When complete, your post will appear on the homepage!

</td>
<td valign="top">

**Step 1: Place Files Locally**

Make sure you've cloned the repository:

```bash
git clone https://github.com/zeelabs/blog-gtm-engineering.git
cd blog-gtm-engineering
```

Copy your files to the correct locations:

```bash
# Replace 'your-post-slug' with your actual slug
cp your-post-slug.html posts/
cp your-post-slug.webp assets/
```

**Step 2: Commit and Push**

Stage your files:

```bash
git add posts/your-post-slug.html assets/your-post-slug.webp
```

Commit with a descriptive message:

```bash
git commit -m "Add new post: [Your Post Title]"
```

Push to the main branch:

```bash
git push origin main
```

**Step 3: Wait for Automation**

-   GitHub Actions runs automatically
-   Check the repository's "Actions" tab online
-   Visit the blog to see your published post!

</td>
</tr>
</table>

---

## 🏷️ Required Metadata (Copy-Paste Examples)

Your HTML file **must** include these meta tags in the `<head>` section. Copy these examples and replace the placeholder values:

### 1. Publish Date _(When the post goes live)_

```html
<meta property="article:published_time" content="2025-11-03T00:00:00+00:00" />
```

**💡 Tip:** Use the format `YYYY-MM-DDTHH:MM:SS+00:00`. For today's date, visit [currentmillis.com](https://currentmillis.com/) or use the current date.

**Example for November 3, 2025:**

```html
<meta property="article:published_time" content="2025-11-03T00:00:00+00:00" />
```

---

### 2. Keywords _(For related articles and SEO)_

```html
<meta name="keywords" content="GTM Engineering, Startups, Marketing Automation, Revenue Operations" />
```

**💡 Tip:** Use 3-6 relevant keywords, separated by commas. These help generate "related articles" at the bottom of your post.

---

### 3. Description _(For search engines and social media)_

```html
<meta
    name="description"
    content="Learn how GTM Engineering transforms startup growth through automation, data systems, and cross-functional alignment."
/>
```

**💡 Tip:** Keep it 150-160 characters for optimal SEO. Make it compelling—this appears in Google search results!

---

### 4. Author

```html
<meta name="author" content="Jorge Macias" />
```

**💡 Tip:** Use your full name as it should appear on the blog.

---

### 5. Featured Image _(For social sharing)_

```html
<meta property="og:image" content="https://blog.gtm-engineering.io/assets/your-post-slug.webp" />
```

**💡 Tip:** Replace `your-post-slug` with your actual slug. This image appears when people share your post on social media.

---

## 🤖 What Happens Automatically

After you commit and push your files, GitHub Actions automatically:

1. **✅ Updates `sitemap.xml`** - Helps Google find and index your post
2. **✅ Updates `feed.xml`** - Adds your post to the RSS feed for subscribers
3. **✅ Adds post card to homepage** - Your post appears in the blog listing
4. **✅ Sorts posts by date** - Newest posts appear first
5. **✅ Promotes to featured post** - If your post is the most recent, it becomes the featured post at the top
6. **✅ Generates related articles** - Matches your keywords with other posts to suggest related content

**You don't need to do anything!** Just wait 1-2 minutes and refresh the blog homepage.

---

## ✅ Verifying Your Post

After the automation completes, verify everything worked:

### Step 1: Check the Homepage

1. Visit [blog.gtm-engineering.io](https://blog.gtm-engineering.io)
2. Look for your post card on the homepage
3. If it's the newest post, it should be in the "Featured Post" section at the top

### Step 2: View the Full Post

1. Click on your post card
2. Verify the content displays correctly
3. Check that your featured image appears

### Step 3: Check Related Articles

1. Scroll to the bottom of your post
2. Verify that "Related Articles" section appears
3. If no related articles appear, it means no other posts share your keywords yet

### Step 4: Verify Sitemap & RSS

-   **Sitemap:** Visit [blog.gtm-engineering.io/sitemap.xml](https://blog.gtm-engineering.io/sitemap.xml)
-   **RSS Feed:** Visit [blog.gtm-engineering.io/feed.xml](https://blog.gtm-engineering.io/feed.xml)

Your post should appear in both!

---

## 🐛 Common Issues & Solutions

### Problem: Post Not Showing on Homepage

**Possible causes and solutions:**

✅ **Check file location:** Make sure your HTML file is in the `posts/` folder, NOT `drafts/`

✅ **Verify publish date:** Ensure the `article:published_time` meta tag is present and valid:

```html
<meta property="article:published_time" content="2025-11-03T00:00:00+00:00" />
```

✅ **Check GitHub Actions:** Go to the "Actions" tab in the repository and check if the workflow completed successfully. If there's a red X, click it to see error details.

---

### Problem: Image Not Displaying

**Possible causes and solutions:**

✅ **Check file location:** Confirm your image is in the `assets/` folder

✅ **Verify filename match:** Make sure the image filename exactly matches your post slug:

-   Post: `my-post.html`
-   Image: `my-post.webp` _(NOT `my-post.png` or `My-Post.webp`)_

✅ **Check file format:** Ensure the image is WebP format (`.webp` extension). Convert PNG/JPG to WebP using online tools like [cloudconvert.com](https://cloudconvert.com/webp-converter)

✅ **Verify meta tag:** Check that your `og:image` meta tag has the correct path:

```html
<meta property="og:image" content="https://blog.gtm-engineering.io/assets/my-post.webp" />
```

---

### Problem: Related Articles Not Appearing

**Possible causes and solutions:**

✅ **Check keywords meta tag:** Ensure you have a `keywords` meta tag with relevant keywords:

```html
<meta name="keywords" content="GTM Engineering, Startups, RevOps" />
```

✅ **Wait for automation:** Related articles are generated during the GitHub Actions workflow. Wait 2-3 minutes after pushing.

✅ **Check other posts:** If you're the first post with certain keywords, no related articles will appear until other posts share those keywords.

---

### Problem: Automation Failed (Red X in Actions Tab)

**Possible causes and solutions:**

✅ **Check error logs:** Click on the failed workflow in the Actions tab to see detailed error messages

✅ **Common errors:**

-   **HTML parsing error:** Make sure your HTML is valid (no unclosed tags)
-   **Missing metadata:** Ensure all required meta tags are present
-   **File naming issue:** Verify filenames use lowercase and hyphens only

✅ **Manual retry:** You can re-run the failed workflow by clicking "Re-run all jobs" in the Actions tab

---

## 🆘 Need Help?

If you're stuck or encounter issues:

-   **📚 Full documentation:** See `CLAUDE.local.md` for detailed technical information
-   **🤖 Automation scripts:** See `scripts/README.md` for how the automation works
-   **💬 Contact support:** Reach out to [Jorge Macias](mailto:jorge@zeelabs.com)
-   **🐛 Report bugs:** [Open an issue on GitHub](https://github.com/zeelabs/blog-gtm-engineering/issues)

---

## 📋 Quick Reference Card

**Print this section for quick access!**

### File Placement Checklist

-   [ ] `posts/your-slug.html` - Blog post HTML file
-   [ ] `assets/your-slug.webp` - Featured image (WebP format)
-   [ ] Slugs match exactly (same name, different extensions)

### Required Meta Tags

```html
<meta property="article:published_time" content="YYYY-MM-DDTHH:MM:SS+00:00" />
<meta name="keywords" content="keyword1, keyword2, keyword3" />
<meta name="description" content="150-160 character description" />
<meta name="author" content="Your Name" />
<meta property="og:image" content="https://blog.gtm-engineering.io/assets/your-slug.webp" />
```

### Publishing (Web UI)

1. Upload HTML to `posts/` folder
2. Upload image to `assets/` folder
3. Wait for GitHub Actions (1-2 min)
4. Verify at blog.gtm-engineering.io

### Publishing (Command Line)

```bash
git add posts/your-slug.html assets/your-slug.webp
git commit -m "Add new post: [Title]"
git push origin main
```

### Automation Does This Automatically

✅ Sitemap update
✅ RSS feed update
✅ Homepage card creation
✅ Post sorting by date
✅ Featured post promotion
✅ Related articles generation

### Quick Verification

1. Visit [blog.gtm-engineering.io](https://blog.gtm-engineering.io)
2. Find your post card
3. Click and verify content
4. Check related articles at bottom

---

**🎉 That's it! Happy blogging!**
