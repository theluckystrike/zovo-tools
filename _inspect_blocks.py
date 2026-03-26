import re, json
with open('/Users/mike/zovo-workspaces/zovo-tools/ai-seo-analyzer/index.html', 'r') as f:
    content = f.read()
pattern = r'<script\s+type=["\']application/ld\+json["\']>\s*(.*?)\s*</script>'
blocks = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
print(f'Found {len(blocks)} blocks')
for i, b in enumerate(blocks):
    print(f'--- Block {i} (first 300 chars) ---')
    print(b[:300])
    try:
        json.loads(b)
        print("VALID JSON")
    except json.JSONDecodeError as e:
        print(f"INVALID: {e}")
    print()
