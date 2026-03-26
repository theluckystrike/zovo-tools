import re

# Check a few pages with skipped levels to understand the pattern
pages = ['1-rep-max-calculator', 'ai-image-generator', 'bmi-calculator']
BASE = '/Users/mike/zovo-workspaces/zovo-tools'

for slug in pages:
    path = f'{BASE}/{slug}/index.html'
    with open(path, 'r') as f:
        content = f.read()

    pattern = r'<(h[1-6])([^>]*)>(.*?)</\1>'
    headings = []
    for m in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
        tag = m.group(1).lower()
        text = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        level = int(tag[1])
        headings.append((level, text[:80]))

    print(f'\n=== {slug} ({len(headings)} headings) ===')
    prev = 0
    for level, text in headings:
        marker = " *** SKIP" if (prev > 0 and level > prev + 1) else ""
        print(f'  h{level}: {text}{marker}')
        prev = level
