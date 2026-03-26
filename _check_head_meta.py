import re

pages = ['cover-letter-generator', 'html-css-playground', 'privacy-policy-generator', 'screenshot-to-code']
BASE = '/Users/mike/zovo-workspaces/zovo-tools'

for slug in pages:
    path = f'{BASE}/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    head_end = content.find('</head>')
    head = content[:head_end] if head_end > 0 else content[:5000]

    # Check if "description" appears anywhere in head
    desc_count = head.lower().count('description')
    print(f'\n=== {slug} ===')
    print(f'  Head length: {head_end}')
    print(f'  "description" in head: {desc_count} times')

    # Find any meta tag with description in head
    for m in re.finditer(r'description', head, re.IGNORECASE):
        start = max(0, m.start() - 100)
        end = min(len(head), m.end() + 50)
        print(f'  Found at {m.start()}: ...{head[start:end]}...')
