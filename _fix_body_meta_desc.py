#!/usr/bin/env python3
"""
Fix pages that have meta description tags in the body but not in the head.
Remove the body occurrences (they're from duplicate HTML templates).
Also handle pay-stub-creator which had many duplicates.
"""
import re

pages_to_fix = [
    'cover-letter-generator',
    'html-css-playground',
    'privacy-policy-generator',
    'screenshot-to-code',
    'pay-stub-creator',
]

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

for slug in pages_to_fix:
    path = f'{BASE}/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    head_end = content.find('</head>')
    if head_end == -1:
        print(f'{slug}: no </head> found, skipping')
        continue

    # Find ALL meta description tags
    pattern = r'<meta\s+[^>]*?name=["\']description["\'][^>]*?>'
    matches = list(re.finditer(pattern, content, re.IGNORECASE))

    head_matches = [m for m in matches if m.start() < head_end]
    body_matches = [m for m in matches if m.start() >= head_end]

    if not body_matches:
        print(f'{slug}: no body meta descriptions to remove')
        continue

    # Remove body meta descriptions (from end to start to preserve positions)
    body_matches.sort(key=lambda m: m.start(), reverse=True)
    for m in body_matches:
        content = content[:m.start()] + content[m.end():]

    # If there are duplicate head meta descriptions, keep the best one
    if len(head_matches) > 1:
        best = max(head_matches, key=lambda m: len(m.group(0)))
        for m in sorted(head_matches, key=lambda m: m.start(), reverse=True):
            if m.start() != best.start():
                content = content[:m.start()] + content[m.end():]

    with open(path, 'w') as f:
        f.write(content)
    print(f'{slug}: removed {len(body_matches)} body meta desc tags, kept {len(head_matches)} in head')
