import re

pages = [
    'cover-letter-generator',
    'html-css-playground',
    'privacy-policy-generator',
    'screenshot-to-code',
]

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

for slug in pages:
    path = f'{BASE}/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    # Find remaining meta description tags
    pattern = r'<meta\s+[^>]*?name=["\']description["\'][^>]*?>'
    matches = list(re.finditer(pattern, content, re.IGNORECASE))

    print(f'\n=== {slug} ({len(matches)} meta desc tags remaining) ===')
    head_end = content.find('</head>')
    print(f'  </head> at position: {head_end}')
    for m in matches:
        in_head = "HEAD" if m.start() < head_end else "BODY"
        print(f'  Position {m.start()} ({in_head}): {m.group(0)[:120]}...')
