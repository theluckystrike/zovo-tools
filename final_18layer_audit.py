#!/usr/bin/env python3
"""
Final 18-Layer Comprehensive Audit for zovo-tools.
Checks all tool pages and article pages against all applicable quality layers.
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")
ARTICLES_DIR = BASE_DIR / "articles"

# Directories/files to skip at root level
SKIP_NAMES = {
    ".git", "articles", "node_modules", "__pycache__",
    ".github", ".vscode", ".claude", ".claude-alt",
}

# Non-directory files at root (skip anything without index.html)
SKIP_EXTENSIONS = {".js", ".json", ".xml", ".txt", ".md", ".html", ".css", ".yml", ".yaml", ".ico", ".png", ".jpg", ".svg"}

# ============================================================
# Layer definitions
# ============================================================

TOOL_LAYERS = {
    "L02": r"quickchart\.io|chart-image|chart\.svg|chart\.png|benchmark-chart|chart-container",
    "L03": r"youtube\.com/embed|video-embed|youtu\.be|youtube-video|yt-block",
    "L04": None,  # Word count > 1000
    "L05": r"Last verified|last_verified|last-checked|Michael Lip|author.*Michael|Verified|update-history|eeat-trust",
    "L06": r"schema\.org|itemscope|itemtype|application/ld\+json",
    "L07": r"og:title|meta.*description|og:description",
    "L08": r"<style>|font-family.*Inter|\.jf-|custom-style|style=",
    "L09": r"shields\.io|img\.shields|badge.*flat-square|badge-row",
    "L10": r"PageSpeed|pagespeed|performance.*competitor|Performance.*vs|LCP|lighthouse|Core Web Vitals|pagespeed-section",
    "L11": r"compat-table-section|compat-table|caniuse\.com|browser.*compatibility|Browser Compatibility",
    "L12": r"so-questions-section|so-block|stackoverflow\.com|Stack Overflow",
    "L13": r"wiki-definition-box|wiki-block|wikipedia\.org|Wikipedia",
    "L16": r"npm-dashboard|npmjs\.com/package|npm-section",
    "L17": r"original-research|Original Research|original-research-section|Methodology|Our Testing|Our Analysis|unique findings|tested.*tools|analyzed.*data",
    "L20": r"live-widget|live-stats|usage-count|live-counter|real-time",
}

ARTICLE_LAYERS = {
    "L02": r"quickchart\.io|chart-image|chart\.svg|chart\.png|benchmark-chart|chart-container",
    "L03": r"youtube\.com/embed|video-embed|youtu\.be|youtube-video|yt-block",
    "L05": r"Last verified|last_verified|last-checked|Michael Lip|author.*Michael|Verified|update-history|eeat-trust",
    "L09": r"shields\.io|img\.shields|badge.*flat-square|badge-row",
    "L12": r"so-questions-section|so-block|stackoverflow\.com|Stack Overflow",
    "L13": r"wiki-definition-box|wiki-block|wikipedia\.org|Wikipedia",
    "L14": r"hn-discussion-section|hn-section|news\.ycombinator|Hacker News|hn-block",
}

LAYER_NAMES = {
    "L02": "QuickChart/Benchmark",
    "L03": "YouTube/Video",
    "L04": "Word Count >1000",
    "L05": "E-E-A-T/Trust",
    "L06": "Schema.org/LD+JSON",
    "L07": "Open Graph/Meta",
    "L08": "Custom Styling",
    "L09": "Shields.io Badges",
    "L10": "PageSpeed/LCP",
    "L11": "Browser Compat",
    "L12": "StackOverflow",
    "L13": "Wikipedia",
    "L14": "Hacker News",
    "L16": "npm Dashboard",
    "L17": "Original Research",
    "L20": "Live Widgets",
}


def get_tool_dirs():
    """Find all tool directories (have index.html, not in skip list)."""
    dirs = []
    for entry in sorted(BASE_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in SKIP_NAMES:
            continue
        if entry.name.startswith("."):
            continue
        index_file = entry / "index.html"
        if index_file.exists():
            dirs.append(entry)
    return dirs


def get_article_dirs():
    """Find all article directories."""
    dirs = []
    if not ARTICLES_DIR.exists():
        return dirs
    for entry in sorted(ARTICLES_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        index_file = entry / "index.html"
        if index_file.exists():
            dirs.append(entry)
    return dirs


def count_words(html_content):
    """Rough word count: strip tags, count words."""
    text = re.sub(r"<[^>]+>", " ", html_content)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())


def check_layer(content, pattern):
    """Check if content matches a layer pattern."""
    if pattern is None:
        return False
    return bool(re.search(pattern, content, re.IGNORECASE))


def audit_page(filepath, layers, is_tool=True):
    """Audit a single page against its applicable layers."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e), "results": {}}

    results = {}
    for layer_id, pattern in layers.items():
        if layer_id == "L04":
            # Special: word count check
            wc = count_words(content)
            results[layer_id] = wc > 1000
            results["_word_count"] = wc
        else:
            results[layer_id] = check_layer(content, pattern)

    return {"results": results, "size": len(content)}


def run_audit():
    """Run the full audit across all tools and articles."""
    tool_dirs = get_tool_dirs()
    article_dirs = get_article_dirs()

    print(f"Found {len(tool_dirs)} tool pages")
    print(f"Found {len(article_dirs)} article pages")
    print()

    # Track per-layer counts
    tool_layer_pass = defaultdict(int)
    tool_layer_fail = defaultdict(list)
    tool_total = len(tool_dirs)

    article_layer_pass = defaultdict(int)
    article_layer_fail = defaultdict(list)
    article_total = len(article_dirs)

    # Audit tools
    tool_results = {}
    for td in tool_dirs:
        filepath = td / "index.html"
        result = audit_page(filepath, TOOL_LAYERS, is_tool=True)
        tool_results[td.name] = result
        for layer_id in TOOL_LAYERS:
            if layer_id == "L04" and result["results"].get(layer_id, False):
                tool_layer_pass[layer_id] += 1
            elif layer_id == "L04":
                tool_layer_fail[layer_id].append(td.name)
            elif result["results"].get(layer_id, False):
                tool_layer_pass[layer_id] += 1
            else:
                tool_layer_fail[layer_id].append(td.name)

    # Audit articles
    article_results = {}
    for ad in article_dirs:
        filepath = ad / "index.html"
        result = audit_page(filepath, ARTICLE_LAYERS, is_tool=False)
        article_results[ad.name] = result
        for layer_id in ARTICLE_LAYERS:
            if result["results"].get(layer_id, False):
                article_layer_pass[layer_id] += 1
            else:
                article_layer_fail[layer_id].append(ad.name)

    # Print tool layer report
    print("=" * 80)
    print("TOOL PAGES AUDIT REPORT")
    print("=" * 80)
    print(f"{'Layer':<6} {'Name':<25} {'Pass':>6} {'Fail':>6} {'Total':>6} {'Rate':>8}")
    print("-" * 80)

    tool_layer_ids = sorted(TOOL_LAYERS.keys(), key=lambda x: int(x[1:]))
    for lid in tool_layer_ids:
        name = LAYER_NAMES.get(lid, lid)
        p = tool_layer_pass[lid]
        f = len(tool_layer_fail[lid])
        rate = f"{p/tool_total*100:.1f}%" if tool_total > 0 else "N/A"
        print(f"{lid:<6} {name:<25} {p:>6} {f:>6} {tool_total:>6} {rate:>8}")

    # Print article layer report
    print()
    print("=" * 80)
    print("ARTICLE PAGES AUDIT REPORT")
    print("=" * 80)
    print(f"{'Layer':<6} {'Name':<25} {'Pass':>6} {'Fail':>6} {'Total':>6} {'Rate':>8}")
    print("-" * 80)

    article_layer_ids = sorted(ARTICLE_LAYERS.keys(), key=lambda x: int(x[1:]))
    for lid in article_layer_ids:
        name = LAYER_NAMES.get(lid, lid)
        p = article_layer_pass[lid]
        f = len(article_layer_fail[lid])
        rate = f"{p/article_total*100:.1f}%" if article_total > 0 else "N/A"
        print(f"{lid:<6} {name:<25} {p:>6} {f:>6} {article_total:>6} {rate:>8}")

    # Show failing tools per layer (first 10)
    print()
    print("=" * 80)
    print("FAILURES DETAIL (first 20 per layer)")
    print("=" * 80)

    print("\n--- TOOL FAILURES ---")
    for lid in tool_layer_ids:
        fails = tool_layer_fail[lid]
        if fails:
            print(f"\n{lid} ({LAYER_NAMES.get(lid, lid)}): {len(fails)} failures")
            for f in fails[:20]:
                print(f"  - {f}")
            if len(fails) > 20:
                print(f"  ... and {len(fails)-20} more")

    print("\n--- ARTICLE FAILURES ---")
    for lid in article_layer_ids:
        fails = article_layer_fail[lid]
        if fails:
            print(f"\n{lid} ({LAYER_NAMES.get(lid, lid)}): {len(fails)} failures")
            for f in fails[:20]:
                print(f"  - {f}")
            if len(fails) > 20:
                print(f"  ... and {len(fails)-20} more")

    # Save full results to JSON
    output = {
        "tool_count": tool_total,
        "article_count": article_total,
        "tool_layer_failures": {k: v for k, v in tool_layer_fail.items()},
        "article_layer_failures": {k: v for k, v in article_layer_fail.items()},
        "tool_layer_pass_counts": dict(tool_layer_pass),
        "article_layer_pass_counts": dict(article_layer_pass),
    }

    with open(BASE_DIR / "final_audit_cycle1.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nFull results saved to final_audit_cycle1.json")

    return output


if __name__ == "__main__":
    run_audit()
