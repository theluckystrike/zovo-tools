#!/usr/bin/env python3
"""
Cycle 4: Final verification of all YouTube embeds.
Checks:
1. Every youtube.com/embed/ has an 11-character video ID
2. No ID used more than 15 times
3. Zero placeholder IDs (dQw4w9WgXcQ, VIDEO_ID, xxxxx, etc.)
4. All iframe elements have loading="lazy" and allowfullscreen
"""

import os
import re
from collections import defaultdict

ROOT = "/Users/mike/zovo-workspaces/zovo-tools"

# Known placeholder/joke IDs to flag
PLACEHOLDER_IDS = {
    "dQw4w9WgXcQ",  # Rickroll
    "VIDEO_ID",
    "xxxxx",
    "XXXXX",
    "placeholder",
    "example",
    "test12345",
    "00000000000",
    "aaaaaaaaaaa",
    "xxxxxxxxxxx",
}

issues = []
total_embeds = 0
total_iframes = 0
files_checked = 0
video_id_files = defaultdict(list)
missing_lazy = []
missing_allowfullscreen = []
bad_length_ids = []
placeholder_found = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
    for f in filenames:
        if f.endswith('.html'):
            fpath = os.path.join(dirpath, f)
            rel_path = os.path.relpath(fpath, ROOT)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except:
                continue

            files_checked += 1

            # Check 1: Extract all video IDs
            embed_matches = re.findall(r'youtube\.com/embed/([A-Za-z0-9_-]+)', content)
            for vid in embed_matches:
                total_embeds += 1
                video_id_files[vid].append(rel_path)

                # Check length
                if len(vid) != 11:
                    bad_length_ids.append((rel_path, vid, len(vid)))

                # Check placeholder
                if vid in PLACEHOLDER_IDS:
                    placeholder_found.append((rel_path, vid))

            # Check 4: iframe attributes for YouTube embeds
            iframe_pattern = re.compile(r'<iframe[^>]*youtube\.com/embed/[^>]*>', re.IGNORECASE)
            for iframe_match in iframe_pattern.finditer(content):
                total_iframes += 1
                iframe_tag = iframe_match.group()

                if 'loading="lazy"' not in iframe_tag and "loading='lazy'" not in iframe_tag:
                    missing_lazy.append(rel_path)

                if 'allowfullscreen' not in iframe_tag:
                    missing_allowfullscreen.append(rel_path)

# ============================================================================
# REPORT
# ============================================================================
print("="*80)
print("CYCLE 4: FINAL VERIFICATION REPORT")
print("="*80)

print(f"\nFiles checked: {files_checked}")
print(f"Total YouTube embeds found: {total_embeds}")
print(f"Total YouTube iframes found: {total_iframes}")
print(f"Unique video IDs: {len(video_id_files)}")

# Check 1: ID length
print(f"\n--- CHECK 1: Video ID Length (should be 11 chars) ---")
if bad_length_ids:
    print(f"FAIL: {len(bad_length_ids)} IDs with wrong length:")
    for fpath, vid, length in bad_length_ids:
        print(f"  {fpath}: '{vid}' (length={length})")
else:
    print("PASS: All video IDs are 11 characters.")

# Check 2: Frequency limit
print(f"\n--- CHECK 2: Frequency Limit (max 15 uses) ---")
exceeding = [(vid, files) for vid, files in video_id_files.items() if len(files) > 15]
if exceeding:
    print(f"FAIL: {len(exceeding)} IDs exceed 15 uses:")
    for vid, files in sorted(exceeding, key=lambda x: -len(x[1])):
        print(f"  {vid}: {len(files)} uses")
else:
    print("PASS: No video ID exceeds 15 uses.")
    # Show top 5
    top5 = sorted(video_id_files.items(), key=lambda x: -len(x[1]))[:5]
    for vid, files in top5:
        print(f"  Top: {vid} = {len(files)} uses")

# Check 3: Placeholder IDs
print(f"\n--- CHECK 3: Placeholder ID Check ---")
if placeholder_found:
    print(f"FAIL: {len(placeholder_found)} placeholder IDs found:")
    for fpath, vid in placeholder_found:
        print(f"  {fpath}: {vid}")
else:
    print("PASS: Zero placeholder IDs found.")

# Check 4a: loading="lazy"
print(f"\n--- CHECK 4a: loading='lazy' Attribute ---")
unique_missing_lazy = list(set(missing_lazy))
if unique_missing_lazy:
    print(f"NEEDS FIX: {len(unique_missing_lazy)} files missing loading='lazy':")
    for f in sorted(unique_missing_lazy)[:30]:
        print(f"  {f}")
    if len(unique_missing_lazy) > 30:
        print(f"  ... and {len(unique_missing_lazy) - 30} more")
else:
    print("PASS: All YouTube iframes have loading='lazy'.")

# Check 4b: allowfullscreen
print(f"\n--- CHECK 4b: allowfullscreen Attribute ---")
unique_missing_afs = list(set(missing_allowfullscreen))
if unique_missing_afs:
    print(f"NEEDS FIX: {len(unique_missing_afs)} files missing allowfullscreen:")
    for f in sorted(unique_missing_afs)[:30]:
        print(f"  {f}")
    if len(unique_missing_afs) > 30:
        print(f"  ... and {len(unique_missing_afs) - 30} more")
else:
    print("PASS: All YouTube iframes have allowfullscreen.")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
all_pass = True
if bad_length_ids:
    all_pass = False
if exceeding:
    all_pass = False
if placeholder_found:
    all_pass = False

if all_pass and not unique_missing_lazy and not unique_missing_afs:
    print("ALL CHECKS PASSED. YouTube embed quality is clean.")
else:
    if all_pass:
        print("Core checks PASSED (IDs valid, no duplicates, no placeholders).")
    if unique_missing_lazy:
        print(f"  - {len(unique_missing_lazy)} iframes need loading='lazy' added")
    if unique_missing_afs:
        print(f"  - {len(unique_missing_afs)} iframes need allowfullscreen added")
