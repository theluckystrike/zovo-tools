import re, json
from collections import Counter

BASE = '/Users/mike/zovo-workspaces/zovo-tools'
with open(f'{BASE}/audit_cycle4_report.json', 'r') as f:
    data = json.load(f)

# Analyze skip patterns
skip_patterns = Counter()
for path, issues in data['issues']:
    for issue in issues:
        if '-> h' in issue and 'h' in issue:
            # Extract the skip pattern like "h1 -> h3"
            m = re.search(r'(h\d) -> (h\d)', issue)
            if m:
                skip_patterns[f'{m.group(1)} -> {m.group(2)}'] += 1

print("Skip pattern frequency:")
for pattern, count in skip_patterns.most_common():
    print(f"  {pattern}: {count}")
