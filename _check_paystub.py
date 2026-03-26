import re
path = '/Users/mike/zovo-workspaces/zovo-tools/pay-stub-creator/index.html'
with open(path, 'r') as f:
    content = f.read()

head_end = content.find('</head>')
print(f'</head> at: {head_end}')

pattern = r'<meta\s+[^>]*?name=["\']description["\'][^>]*?>'
matches = list(re.finditer(pattern, content, re.IGNORECASE))
print(f'Total meta desc: {len(matches)}')
for m in matches:
    in_head = "HEAD" if m.start() < head_end else "BODY"
    print(f'  {in_head} pos {m.start()}: {m.group(0)[:120]}')
