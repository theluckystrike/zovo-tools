import re

path = '/Users/mike/zovo-workspaces/zovo-tools/acceleration-calculator/index.html'
with open(path, 'r') as f:
    content = f.read()

# Find all og:title occurrences
count = content.count('og:title')
print(f'og:title occurrences: {count}')

# Find it in context
idx = content.find('og:title')
if idx >= 0:
    print(f'Context: ...{content[max(0,idx-150):idx+150]}...')
else:
    print('NOT FOUND')

# Also check one that was previously detected
path2 = '/Users/mike/zovo-workspaces/zovo-tools/bmi-calculator/index.html'
with open(path2, 'r') as f:
    content2 = f.read()
count2 = content2.count('og:title')
print(f'\nbmi-calculator og:title occurrences: {count2}')
idx2 = content2.find('og:title')
if idx2 >= 0:
    print(f'Context: ...{content2[max(0,idx2-100):idx2+100]}...')
