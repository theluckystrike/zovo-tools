#!/usr/bin/env python3
"""
Fix URL references across all tool pages in zovo-tools.

1. Fix canonical URLs missing /free-tools/ prefix
2. Fix bare internal links to known tool slugs missing /free-tools/ prefix
3. Fix og:url meta content missing /free-tools/ prefix
"""

import os
import re
import sys

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Non-tool directories and files to exclude
EXCLUDE = {
    ".git", "articles", "CNAME", "robots.txt", "sitemap.xml",
    "deploy-tool.sh", "add_og_tags.py", "fix_urls.py",
    "c4ded4558ba249bbbd828bbfd67ebe80.txt"
}

def get_tool_slugs():
    """Get all valid tool directory names."""
    slugs = set()
    for entry in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full_path) and entry not in EXCLUDE and not entry.startswith("."):
            slugs.add(entry)
    return slugs

def get_index_files():
    """Get all index.html files in tool directories (and root)."""
    files = []
    # Root index.html
    root_index = os.path.join(BASE_DIR, "index.html")
    if os.path.isfile(root_index):
        files.append(root_index)
    # Tool directory index.html files
    for entry in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full_path) and not entry.startswith("."):
            index_path = os.path.join(full_path, "index.html")
            if os.path.isfile(index_path):
                files.append(index_path)
    return sorted(files)

def fix_file(filepath, tool_slugs):
    """Fix URLs in a single index.html file. Returns dict of changes."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    changes = {
        "canonical": 0,
        "og_url": 0,
        "internal_links": 0,
        "details": []
    }

    # Determine the slug for this file (for canonical/og:url fixes)
    parent_dir = os.path.basename(os.path.dirname(filepath))
    file_slug = parent_dir if parent_dir != "zovo-tools" else None

    # === 1. Fix canonical URLs ===
    # Match: <link rel="canonical" href="https://zovo.one/SLUG"> or href="https://zovo.one/SLUG/"
    # where SLUG is NOT prefixed with free-tools/
    def fix_canonical(match):
        full_match = match.group(0)
        href_val = match.group(1)
        # Skip if already has /free-tools/
        if "/free-tools/" in href_val:
            return full_match
        # Extract slug from URL like https://zovo.one/SLUG or https://zovo.one/SLUG/
        m = re.match(r"https://zovo\.one/([a-z0-9-]+)/?$", href_val)
        if m:
            slug = m.group(1)
            if slug in tool_slugs:
                new_url = f"https://zovo.one/free-tools/{slug}/"
                changes["canonical"] += 1
                changes["details"].append(f"  canonical: {href_val} -> {new_url}")
                return full_match.replace(href_val, new_url)
        return full_match

    content = re.sub(
        r'<link\s+rel="canonical"\s+href="([^"]+)"',
        fix_canonical,
        content
    )

    # === 2. Fix og:url ===
    def fix_og_url(match):
        full_match = match.group(0)
        content_val = match.group(1)
        if "/free-tools/" in content_val:
            return full_match
        m = re.match(r"https://zovo\.one/([a-z0-9-]+)/?$", content_val)
        if m:
            slug = m.group(1)
            if slug in tool_slugs:
                new_url = f"https://zovo.one/free-tools/{slug}/"
                changes["og_url"] += 1
                changes["details"].append(f"  og:url: {content_val} -> {new_url}")
                return full_match.replace(content_val, new_url)
        return full_match

    content = re.sub(
        r'<meta\s+property="og:url"\s+content="([^"]+)"',
        fix_og_url,
        content
    )

    # === 3. Fix bare internal links ===
    # Match href="/SLUG" or href="/SLUG/" where SLUG is a known tool slug
    # Do NOT match:
    #   - href="/" (root)
    #   - href="/free-tools/..." (already correct)
    #   - href="https://..." (external)
    #   - href="#..." (anchor)
    #   - href="/static-tools" or other non-tool paths
    def fix_internal_link(match):
        full_match = match.group(0)
        path = match.group(1)

        # Skip if already has /free-tools/
        if path.startswith("/free-tools/"):
            return full_match

        # Extract slug: /SLUG or /SLUG/
        m = re.match(r"^/([a-z0-9-]+)/?$", path)
        if m:
            slug = m.group(1)
            if slug in tool_slugs:
                new_path = f"/free-tools/{slug}/"
                changes["internal_links"] += 1
                changes["details"].append(f"  href: {path} -> {new_path}")
                return f'href="{new_path}"'
        return full_match

    content = re.sub(
        r'href="(/[a-z0-9][a-z0-9-]*/?)"',
        fix_internal_link,
        content
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return None

def main():
    tool_slugs = get_tool_slugs()
    print(f"Found {len(tool_slugs)} tool directories")

    index_files = get_index_files()
    print(f"Found {len(index_files)} index.html files to process\n")

    total_canonical = 0
    total_og_url = 0
    total_internal = 0
    files_changed = 0

    for filepath in index_files:
        rel_path = os.path.relpath(filepath, BASE_DIR)
        changes = fix_file(filepath, tool_slugs)
        if changes:
            files_changed += 1
            total_canonical += changes["canonical"]
            total_og_url += changes["og_url"]
            total_internal += changes["internal_links"]
            print(f"FIXED: {rel_path}")
            for detail in changes["details"]:
                print(detail)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files modified:        {files_changed}")
    print(f"Canonical URLs fixed:  {total_canonical}")
    print(f"OG URLs fixed:         {total_og_url}")
    print(f"Internal links fixed:  {total_internal}")
    print(f"Total changes:         {total_canonical + total_og_url + total_internal}")

if __name__ == "__main__":
    main()
