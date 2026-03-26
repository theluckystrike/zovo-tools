import re

pages = [
    'turkish-lira-to-usd',
    'html-email-builder',
]

for slug in pages:
    path = f'/Users/mike/zovo-workspaces/zovo-tools/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    # Find ALL occurrences of name="description" or name='description'
    all_matches = list(re.finditer(r'name=["\']description["\']', content, re.IGNORECASE))
    print(f'\n=== {slug} ({len(all_matches)} occurrences) ===')
    for m in all_matches:
        start = max(0, m.start() - 50)
        end = min(len(content), m.end() + 100)
        context = content[start:end]
        print(f'  Position {m.start()}: ...{context}...')
