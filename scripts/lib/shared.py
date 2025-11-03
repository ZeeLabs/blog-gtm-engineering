#!/usr/bin/env python3
"""
Shared utilities for GTM Engineering Blog scripts.
Centralized common functions to reduce code duplication.
"""

import html
import json
import random
import re
from datetime import datetime


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def estimate_reading_time(content, strip_html=False):
    """
    Estimate reading time based on word count (average 200 words per minute).

    Args:
        content: Text or HTML content
        strip_html: If True, removes HTML tags before counting words

    Returns:
        int: Estimated reading time in minutes
    """
    if strip_html:
        content = strip_html_tags(content)
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return minutes


def strip_html_tags(html_content):
    """
    Remove HTML tags from content for accurate word counting.

    Args:
        html_content: HTML string

    Returns:
        str: Plain text without HTML tags
    """
    html_content = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)
    html_content = re.sub(r"<[^>]+>", "", html_content)
    html_content = html.unescape(html_content)
    html_content = re.sub(r"\s+", " ", html_content)

    return html_content.strip()


def get_current_date():
    """Get current date in both display and ISO formats."""
    return {
        "display": datetime.now().strftime("%B %d, %Y"),
        "iso": datetime.now().strftime("%Y-%m-%d"),
    }


def validate_slug(slug):
    """
    Validate slug format: lowercase, alphanumeric, hyphens only, no leading/trailing hyphens.

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
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


def validate_description_length(description):
    """
    Validate meta description is within SEO best practice range (150-160 chars).

    Returns:
        bool: True if length is acceptable
    """
    if len(description) < 120:
        print(f"⚠️  Warning: Description is short ({len(description)} chars). Consider 150-160 for SEO.")
    elif len(description) > 160:
        print(f"⚠️  Warning: Description is long ({len(description)} chars). Consider trimming to 160.")
        return False
    return True


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

    scheme = random.choice(schemes)
    return scheme["color1"], scheme["color2"], scheme["label"]


def inject_noindex_meta(html_content):
    """
    Insert a noindex/nofollow meta tag into <head> for draft posts.

    Args:
        html_content: HTML string to modify

    Returns:
        str: Modified HTML with noindex meta tag
    """
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


def parse_faq_json(json_str):
    """
    Parse and validate FAQ JSON input.

    Expected format:
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Question text",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Answer text"
          }
        }
      ]
    }

    Args:
        json_str: JSON string containing FAQ data

    Returns:
        list: List of FAQ dictionaries with 'question' and 'answer' keys

    Raises:
        ValueError: If JSON is invalid or missing required fields
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    # Validate structure
    if "@type" not in data or data["@type"] != "FAQPage":
        raise ValueError("JSON must have '@type': 'FAQPage'")

    if "mainEntity" not in data or not isinstance(data["mainEntity"], list):
        raise ValueError("JSON must have 'mainEntity' array")

    # Extract FAQs
    faqs = []
    for idx, item in enumerate(data["mainEntity"], 1):
        if "@type" not in item or item["@type"] != "Question":
            raise ValueError(f"FAQ item {idx} must have '@type': 'Question'")

        if "name" not in item:
            raise ValueError(f"FAQ item {idx} missing 'name' (question text)")

        if "acceptedAnswer" not in item or "@type" not in item["acceptedAnswer"]:
            raise ValueError(f"FAQ item {idx} missing 'acceptedAnswer'")

        if "text" not in item["acceptedAnswer"]:
            raise ValueError(f"FAQ item {idx} missing answer 'text'")

        question = item["name"].strip()
        answer = item["acceptedAnswer"]["text"].strip()

        if not question:
            raise ValueError(f"FAQ item {idx} has empty question")

        if not answer:
            raise ValueError(f"FAQ item {idx} has empty answer")

        # Validate lengths (same as interactive mode)
        if len(answer) < 50:
            print(f"⚠️  FAQ {idx} answer is short ({len(answer)} chars). Consider more detail for better SEO.")
        elif len(answer) > 500:
            print(f"⚠️  FAQ {idx} answer is long ({len(answer)} chars). Consider being more concise.")

        faqs.append({"question": question, "answer": answer})

    if not faqs:
        raise ValueError("No valid FAQs found in JSON")

    return faqs


def parse_schema_json(json_str, schema_type):
    """
    Parse and validate custom schema JSON input (BlogPosting or ItemList).

    Args:
        json_str: JSON string containing schema data
        schema_type: Expected schema type ('BlogPosting' or 'ItemList')

    Returns:
        dict: Validated schema dictionary

    Raises:
        ValueError: If JSON is invalid or wrong schema type
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    # Validate schema type
    if "@type" not in data:
        raise ValueError("Schema must have '@type' field")

    if data["@type"] != schema_type:
        raise ValueError(f"Expected schema type '{schema_type}', got '{data['@type']}'")

    # Basic validation for required fields
    if schema_type == "BlogPosting":
        required_fields = ["headline", "author", "datePublished"]
        for field in required_fields:
            if field not in data:
                print(f"⚠️  Warning: BlogPosting schema missing recommended field '{field}'")

    elif schema_type == "ItemList":
        if "itemListElement" not in data:
            raise ValueError("ItemList schema must have 'itemListElement' array")

    return data


def generate_faq_schema_json(faqs):
    """
    Generate FAQ schema JSON from FAQ list.

    Args:
        faqs: List of FAQ dictionaries with 'question' and 'answer' keys

    Returns:
        str: JSON string for FAQ schema
    """
    if not faqs:
        return ""

    faq_items = []
    for faq in faqs:
        faq_items.append(
            {"@type": "Question", "name": faq["question"], "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]}}
        )

    schema = {"@type": "FAQPage", "mainEntity": faq_items}

    return json.dumps(schema, indent=12)  # 12 spaces for proper template indentation
