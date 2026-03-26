#!/usr/bin/env python3
"""Fix remaining duplicate meta description tags by keeping only the first occurrence."""
import re

pages = [
    'cover-letter-generator',
    'html-css-playground',
    'html-email-builder',
    'pay-stub-creator',
    'privacy-policy-generator',
    'screenshot-to-code',
    'turkish-lira-to-usd',
]

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

for slug in pages:
    path = f'{BASE}/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    # Find all meta description tags (both attribute orders)
    # We use a broader pattern that handles various attribute combinations
    pattern = r'<meta\s+[^>]*?name=["\']description["\'][^>]*?>'
    matches = list(re.finditer(pattern, content, re.IGNORECASE))

    # Also find reversed order
    pattern2 = r'<meta\s+[^>]*?content=["\'][^"\']*?["\'][^>]*?name=["\']description["\'][^>]*?>'
    matches2 = list(re.finditer(pattern2, content, re.IGNORECASE))

    # Combine and sort by position, deduplicate
    all_matches = []
    seen_positions = set()
    for m in matches + matches2:
        if m.start() not in seen_positions:
            seen_positions.add(m.start())
            all_matches.append(m)
    all_matches.sort(key=lambda m: m.start())

    if len(all_matches) <= 1:
        print(f'{slug}: only {len(all_matches)} meta desc found, skipping')
        continue

    # Keep the first one in the <head> section (before </head> or first <body>)
    head_end = content.find('</head>')
    if head_end == -1:
        head_end = content.find('<body')
    if head_end == -1:
        head_end = 2000  # fallback: assume head is in first 2000 chars

    # Find which matches are in the head vs body
    head_matches = [m for m in all_matches if m.start() < head_end]
    body_matches = [m for m in all_matches if m.start() >= head_end]

    # Keep the best head match (longest content), remove rest
    if head_matches:
        best = max(head_matches, key=lambda m: len(m.group(0)))
    else:
        best = all_matches[0]  # If none in head, keep first

    removals = 0
    # Remove from end to start to preserve positions
    to_remove = [m for m in all_matches if m.start() != best.start()]
    to_remove.sort(key=lambda m: m.start(), reverse=True)

    for m in to_remove:
        content = content[:m.start()] + content[m.end():]
        removals += 1

    with open(path, 'w') as f:
        f.write(content)
    print(f'{slug}: removed {removals} duplicate meta description tags (kept best at pos {best.start()})')
