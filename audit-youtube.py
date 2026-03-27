#!/usr/bin/env python3
"""Audit all YouTube embeds across tool pages and articles."""

import os
import re
from collections import defaultdict

ROOT = "/Users/mike/zovo-workspaces/zovo-tools"

# Find all HTML files
html_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip hidden dirs, node_modules, .git
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
    for f in filenames:
        if f.endswith('.html'):
            html_files.append(os.path.join(dirpath, f))

print(f"Total HTML files found: {len(html_files)}")

# Extract YouTube video IDs
pattern = re.compile(r'youtube\.com/embed/([A-Za-z0-9_-]{5,15})')

video_id_files = defaultdict(list)  # video_id -> [file_paths]
files_with_embeds = 0
total_embeds = 0

for fpath in html_files:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
    except:
        continue

    matches = pattern.findall(content)
    if matches:
        files_with_embeds += 1
        total_embeds += len(matches)
        for vid in matches:
            rel_path = os.path.relpath(fpath, ROOT)
            video_id_files[vid].append(rel_path)

print(f"\nFiles with YouTube embeds: {files_with_embeds}")
print(f"Total embed instances: {total_embeds}")
print(f"Unique video IDs: {len(video_id_files)}")

# Sort by frequency
sorted_ids = sorted(video_id_files.items(), key=lambda x: -len(x[1]))

print("\n" + "="*80)
print("ALL VIDEO IDs BY FREQUENCY")
print("="*80)

generic_count = 0
for vid, files in sorted_ids:
    count = len(files)
    marker = " *** LIKELY GENERIC ***" if count >= 10 else ""
    if count >= 10:
        generic_count += 1
    print(f"\n{vid} — {count} uses{marker}")
    if count <= 20:
        for f in files:
            print(f"  - {f}")
    else:
        for f in files[:5]:
            print(f"  - {f}")
        print(f"  ... and {count - 5} more")

print("\n" + "="*80)
print(f"SUMMARY: {generic_count} video IDs used 10+ times (likely generic/placeholder)")
print("="*80)

# Check for known placeholders
known_placeholders = ['dQw4w9WgXcQ', 'VIDEO_ID', 'xxxxx', 'XXXXX', 'placeholder', 'example']
print("\nKnown placeholder check:")
for p in known_placeholders:
    if p in video_id_files:
        print(f"  FOUND: {p} used {len(video_id_files[p])} times")
    else:
        print(f"  Not found: {p}")

# Categorize tools by directory name for mapping
print("\n" + "="*80)
print("GENERIC IDs WITH TOOL CATEGORIES")
print("="*80)
for vid, files in sorted_ids:
    if len(files) >= 10:
        print(f"\n--- {vid} ({len(files)} uses) ---")
        for f in sorted(files):
            print(f"  {f}")
