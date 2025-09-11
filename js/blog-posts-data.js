/**
 * Centralized Blog Posts Data
 *
 * This file contains all blog post metadata used for related posts functionality.
 * When adding new blog posts, simply add the post data here and it will be
 * automatically available across all existing blog post pages.
 *
 * To add a new post:
 * 1. Add the post object to the blogPostsData array below
 * 2. Ensure the new blog post file includes the related posts functionality
 *
 * Post object structure:
 * {
 *   title: "Post Title",
 *   url: "post-filename.html",
 *   excerpt: "Brief description for related posts",
 *   date: "Month DD, YYYY",
 *   image: "../assets/image-name.webp",
 *   imageAlt: "Alt text for the image",
 *   tags: ["Tag1", "Tag2", "Tag3"],
 *   category: "Main Category"
 * }
 */

const blogPostsData = [
    {
        title: 'What is GTM Marketing? An Engineering Approach to Growth',
        url: 'what-is-gtm-marketing-engineering-approach.html',
        excerpt:
            'Discover what GTM marketing means for startups. Learn why a traditional gtm strategy fails and how an engineering approach to data and automation drives real growth.',
        date: 'September 04, 2025',
        image: '../assets/gtm-engineering-vs-marketing-system.webp',
        imageAlt:
            'Abstract illustration showing a chaotic tangle of lines transforming into a clean, orderly system of gears and data flows',
        tags: ['GTM Strategy', 'GTM Engineering', 'Startups'],
        category: 'GTM Strategy',
    },
    {
        title: 'GTM Engineering vs. Revenue Operations: The Definitive Guide for Startups',
        url: 'gtm-engineering-vs-revenue-operations-for-startups.html',
        excerpt:
            "What's the difference between GTM Engineering and Revenue Operations? A YC founder breaks down which discipline your startup needs to build a scalable revenue machine.",
        date: 'September 04, 2025',
        image: '../assets/gtm-engineering-vs-revops.webp',
        imageAlt:
            'Abstract 3D illustration showing GTM Engineering as clean, scalable building blocks and RevOps as a complex dashboard of dials',
        tags: ['GTM Engineering', 'RevOps', 'Startups'],
        category: 'GTM Engineering',
    },
    {
        title: "What is a Go-to-Market Strategy? A Founder's Playbook",
        url: 'what-is-a-go-to-market-strategy-founders-playbook.html',
        excerpt:
            "A founder's guide to building a go-to-market strategy that actually works. Learn the YC-tested principles to build a scalable revenue system for your startup.",
        date: 'September 04, 2025',
        image: '../assets/gtm-revenue-system-illustration.webp',
        imageAlt:
            '3D isometric illustration of GTM strategy components including ICP, Sales, Marketing modules with a person optimizing the system',
        tags: ['GTM Strategy', 'Startups', 'Revenue System'],
        category: 'Go-to-Market Strategy',
    },
];

/**
 * Related Posts Functionality
 *
 * This function generates related posts for the current page based on:
 * - Shared tags (higher weight: 3 points per shared tag)
 * - Same category (2 points)
 * - Falls back to most recent posts if not enough related content
 *
 * @param {string} currentPostUrl - The filename of the current post
 * @returns {Array} Array of related post objects sorted by relevance
 */
function getRelatedPosts(currentPostUrl) {
    // Find current post
    const currentPost = blogPostsData.find((post) => post.url === currentPostUrl);

    if (!currentPost) {
        console.warn(`Current post not found: ${currentPostUrl}`);
        return [];
    }

    // Calculate relevance scores for other posts
    const scoredPosts = blogPostsData
        .filter((post) => post.url !== currentPostUrl)
        .map((post) => {
            let score = 0;

            // Score based on shared tags (higher weight)
            const sharedTags = post.tags.filter((tag) => currentPost.tags.includes(tag));
            score += sharedTags.length * 3;

            // Score based on same category
            if (post.category === currentPost.category) {
                score += 2;
            }

            return { ...post, relevanceScore: score };
        })
        .sort((a, b) => b.relevanceScore - a.relevanceScore)
        .slice(0, 3); // Take top 3

    // If we don't have enough related posts, fill with most recent
    while (scoredPosts.length < 3) {
        const remainingPosts = blogPostsData.filter(
            (post) => post.url !== currentPostUrl && !scoredPosts.find((sp) => sp.url === post.url)
        );
        if (remainingPosts.length > 0) {
            scoredPosts.push(remainingPosts[0]);
        } else {
            break;
        }
    }

    return scoredPosts;
}

/**
 * Render Related Posts
 *
 * This function renders the related posts HTML into the specified container.
 * Call this function after the DOM is loaded.
 *
 * @param {string} containerId - The ID of the container element (default: 'related-posts-grid')
 */
function renderRelatedPosts(containerId = 'related-posts-grid') {
    // Get current post URL from the page
    const currentPostUrl = window.location.pathname.split('/').pop();

    // Get related posts
    const relatedPosts = getRelatedPosts(currentPostUrl);

    // Find the container element
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Related posts container not found: ${containerId}`);
        return;
    }

    // Render the posts
    container.innerHTML = relatedPosts
        .map(
            (post) => `
        <article class="related-post-card">
            <a href="${post.url}" class="related-post-image" aria-label="Read: ${post.title}">
                <img src="${post.image}" alt="${post.imageAlt}" />
            </a>
            <div class="related-post-content">
                <h3 class="related-post-title">
                    <a href="${post.url}">${post.title}</a>
                </h3>
                <p class="related-post-excerpt">${post.excerpt}</p>
                <div class="related-post-meta">
                    <span class="related-post-date">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                            <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
                            <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
                            <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
                        </svg>
                        ${post.date}
                    </span>
                </div>
                <div class="related-post-tags">
                    ${post.tags.map((tag) => `<span class="post-tag">${tag}</span>`).join('')}
                </div>
            </div>
        </article>
    `
        )
        .join('');
}

// Auto-initialize related posts when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    renderRelatedPosts();
});
