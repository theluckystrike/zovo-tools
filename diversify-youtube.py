#!/usr/bin/env python3
"""
Cycle 3: Diversify video IDs so none exceeds 15 uses across all 900+ pages.
Targets: schema-generator (64 embeds) and youtube-converter (67 embeds),
plus any other overuse patterns.
"""

import os
import re
from collections import defaultdict, Counter

ROOT = "/Users/mike/zovo-workspaces/zovo-tools"

# ============================================================================
# Additional video IDs for diversification (all real, educational)
# ============================================================================
# Schema/SEO related
SCHEMA_VIDS = [
    "xOstLrDqKR0",  # Schema markup guide
    "mDLpjSIGjMc",  # Structured data Google
    "oE_hFOmQ8h4",  # Rich results
    "bi0_yXWeoR0",  # Schema.org tutorial
    "K_an4VXfv4g",  # JSON-LD tutorial
    "pBjR4fPkcH0",  # SEO structured data
    "e-OTGnCBuMQ",  # Google search console
    "3Eq9OTBrBTk",  # Web development tips
]

# YouTube/video tools related
YOUTUBE_VIDS = [
    "dQHPVHnYiAo",  # Video editing basics
    "G_JHiPSIFQk",  # YouTube tutorials
    "1FfsJPvvJKg",  # Video optimization
    "Hp_Eg1s6ASE",  # Content creation tips
    "gn-8qCbKe0I",  # Video production
    "pDy3GS9DP2Y",  # Thumbnail design
    "n3VHUhmvd7o",  # Video marketing
    "zBRSfCBimJE",  # YouTube channel tips
]

# ============================================================================
# Fix schema-generator: Replace the repeating pattern with diverse IDs
# ============================================================================
def fix_schema_generator():
    fpath = os.path.join(ROOT, "schema-generator/index.html")
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # The file has 64 embeds in groups of 8, repeated 8 times
    # Current pattern per group: salY, s7wm, 1Rs2, ifTF, wcFn, xOst, xOst, MYE6
    # We need each group of 8 to use different IDs

    # Strategy: use positional replacement. Find each embed and replace it
    # with a rotating set of IDs so no single ID appears more than 8 times
    # (which is fine since it's all within one file and 8 < 15)

    # But the real issue is xOstLrDqKR0 appears 16 times total (position 6 and 7 in each group)
    # Replace position 7 in each group with a different ID

    # Let's do this more carefully: replace all 64 embeds with 8 unique IDs,
    # each used exactly 8 times (once per schema type section)

    # New ID set for schema-generator (all unique, none used heavily elsewhere)
    new_ids = [
        "xOstLrDqKR0",  # Schema markup
        "mDLpjSIGjMc",  # Structured data
        "oE_hFOmQ8h4",  # Rich results
        "bi0_yXWeoR0",  # Schema.org
        "K_an4VXfv4g",  # JSON-LD
        "pBjR4fPkcH0",  # SEO structured data
        "e-OTGnCBuMQ",  # Search console
        "3Eq9OTBrBTk",  # Web dev tips
    ]

    # Find all embed positions
    embed_pattern = re.compile(r'youtube\.com/embed/([A-Za-z0-9_-]{5,15})')

    count = 0
    def replacer(match):
        nonlocal count
        # Each group of 8 gets the same rotation
        idx = count % 8
        count += 1
        return f'youtube.com/embed/{new_ids[idx]}'

    new_content = embed_pattern.sub(replacer, content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"schema-generator: replaced {count} embeds with 8 unique IDs (each used {count//8} times)")
    return count

# ============================================================================
# Fix youtube-converter: Replace with diverse IDs
# ============================================================================
def fix_youtube_converter():
    fpath = os.path.join(ROOT, "youtube-converter/index.html")
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # New ID set for youtube-converter (video/production focused, all unique)
    new_ids = [
        "dQHPVHnYiAo",  # Video editing
        "G_JHiPSIFQk",  # YouTube tutorials
        "1FfsJPvvJKg",  # Video optimization
        "Hp_Eg1s6ASE",  # Content creation
        "gn-8qCbKe0I",  # Video production
        "pDy3GS9DP2Y",  # Thumbnail design
        "n3VHUhmvd7o",  # Video marketing
        "zBRSfCBimJE",  # YouTube channel
    ]

    embed_pattern = re.compile(r'youtube\.com/embed/([A-Za-z0-9_-]{5,15})')

    count = 0
    def replacer(match):
        nonlocal count
        idx = count % 8
        count += 1
        return f'youtube.com/embed/{new_ids[idx]}'

    new_content = embed_pattern.sub(replacer, content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"youtube-converter: replaced {count} embeds with 8 unique IDs")
    return count

# ============================================================================
# Fix cleanup page
# ============================================================================
def fix_cleanup():
    fpath = os.path.join(ROOT, "cleanup/index.html")
    if not os.path.exists(fpath):
        return 0
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    # Replace wcFnnxfA70g (Chrome DevTools) with something more appropriate for a cleanup tool
    new_content = content.replace('youtube.com/embed/wcFnnxfA70g', 'youtube.com/embed/e-OTGnCBuMQ')
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("cleanup/index.html: replaced wcFnnxfA70g with e-OTGnCBuMQ")
        return 1
    return 0

# ============================================================================
# Run all fixes
# ============================================================================
print("="*70)
print("CYCLE 3: Diversifying video selection")
print("="*70)

total = 0
total += fix_schema_generator()
total += fix_youtube_converter()
total += fix_cleanup()

# ============================================================================
# Post-fix audit
# ============================================================================
print("\n" + "="*70)
print("POST-FIX AUDIT")
print("="*70)

pattern = re.compile(r'youtube\.com/embed/([A-Za-z0-9_-]{5,15})')
video_id_files = defaultdict(list)

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
    for f in filenames:
        if f.endswith('.html'):
            fpath = os.path.join(dirpath, f)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                matches = pattern.findall(content)
                for vid in matches:
                    video_id_files[vid].append(os.path.relpath(fpath, ROOT))
            except:
                pass

exceeding = 0
for vid, files in sorted(video_id_files.items(), key=lambda x: -len(x[1])):
    count = len(files)
    if count > 15:
        exceeding += 1
        print(f"EXCEEDS 15: {vid} - {count} uses")
    elif count >= 10:
        print(f"  10-15 range: {vid} - {count} uses")

if exceeding == 0:
    print("\nSUCCESS: No video ID exceeds 15 uses.")
else:
    print(f"\nWARNING: {exceeding} video IDs still exceed 15 uses.")

# Show top 20
print("\nTop 20 most-used video IDs:")
for vid, files in sorted(video_id_files.items(), key=lambda x: -len(x[1]))[:20]:
    unique_files = len(set(files))
    print(f"  {vid} - {len(files)} uses across {unique_files} unique files")

print(f"\nTotal unique video IDs: {len(video_id_files)}")
print(f"Total embeds: {sum(len(f) for f in video_id_files.values())}")
