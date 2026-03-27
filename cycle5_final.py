#!/usr/bin/env python3
"""Final comprehensive quality metrics."""
import os, re, statistics
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

AI_WORDS = ["comprehensive","delve","delves","delving","leverage","leverages","leveraging","leveraged","landscape","landscapes","utilize","utilizes","utilizing","utilized","utilization","streamline","streamlines","streamlining","streamlined","robust","cutting-edge","cutting edge","game-changer","game changer","game-changing","synergy","synergies","paradigm","paradigms","holistic","empower","empowers","empowering","empowered","unlock","unlocks","unlocking","harness","harnessing","harnessed","elevate","elevates","elevating","elevated","pivotal","transformative","innovative","revolutionary","revolutionize","revolutionizes","revolutionizing"]

def extract_visible_text(html):
    text = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE)
    text = re.sub(r'<style[\s\S]*?</style>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<!--[\s\S]*?-->', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    return text

def scan_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    vis = extract_visible_text(html)
    ns = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    ns = re.sub(r'<style[\s\S]*?</style>', '', ns, flags=re.IGNORECASE)
    sb = len(re.findall(r'<strong\b[^>]*>', ns, re.IGNORECASE))
    for m in re.finditer(r'<b[\s>]', ns, re.IGNORECASE):
        if re.match(r'<b\s[^>]*>|<b>', ns[m.start():], re.IGNORECASE):
            sb += 1
    ed = vis.count('\u2014') + vis.count('\u2013')
    aw = 0
    for w in AI_WORDS:
        aw += len(re.findall(r'\b' + re.escape(w) + r'\b', vis, re.IGNORECASE))
    ca = len(re.findall(r'\bClaude\b', html)) + len(re.findall(r'\bAnthropic\b', html)) + len(re.findall(r'Co-Authored-By', html, re.IGNORECASE))
    wc = len(re.findall(r'\b[a-zA-Z]{2,}\b', vis))
    return sb, ed, aw, ca, wc

exclude = {'articles','categories','cleanup','recovery_documentation','.git','node_modules','__pycache__','.claude'}

# Articles
af = [(d, os.path.join(BASE_DIR,'articles',d,'index.html')) for d in sorted(os.listdir(os.path.join(BASE_DIR,'articles'))) if os.path.isfile(os.path.join(BASE_DIR,'articles',d,'index.html'))]
# Tools
tf = [(d, os.path.join(BASE_DIR,d,'index.html')) for d in sorted(os.listdir(BASE_DIR)) if d not in exclude and not d.startswith('.') and not d.startswith('_') and os.path.isfile(os.path.join(BASE_DIR,d,'index.html'))]

print("="*70)
print("FINAL QUALITY METRICS")
print("="*70)

asb=aed=aaw=aca=0; awcs=[]
for n,p in af:
    sb,ed,aw,ca,wc = scan_file(p)
    asb+=sb; aed+=ed; aaw+=aw; aca+=ca; awcs.append(wc)

tsb=ted=taw=tca=0; twcs=[]
for i,(n,p) in enumerate(tf):
    if (i+1)%200==0: print(f"  {i+1}/{len(tf)}...")
    sb,ed,aw,ca,wc = scan_file(p)
    tsb+=sb; ted+=ed; taw+=aw; tca+=ca; twcs.append(wc)
    if sb>0 or aw>0:
        print(f"  ISSUE: {n}: {sb} strong/b, {aw} AI words")

print(f"\nARTICLES ({len(af)}):")
print(f"  Strong/B: {asb} | Em-dashes: {aed} | AI words: {aaw} | Claude: {aca}")
print(f"  Words: min={min(awcs):,} max={max(awcs):,} avg={int(statistics.mean(awcs)):,} total={sum(awcs):,}")

print(f"\nTOOLS ({len(tf)}):")
print(f"  Strong/B: {tsb} | Em-dashes: {ted} | AI words: {taw} | Claude: {tca}")
print(f"  Words: min={min(twcs):,} max={max(twcs):,} avg={int(statistics.mean(twcs)):,} total={sum(twcs):,}")

gs=asb+tsb; gd=aed+ted; ga=aaw+taw; gc=aca+tca
print(f"\n{'='*70}")
print(f"GRAND TOTAL ({len(af)+len(tf)} pages)")
print(f"{'='*70}")
print(f"  Strong/B tags:     {gs:4d} {'PASS' if gs==0 else 'FAIL'}")
print(f"  Em-dashes:         {gd:4d} {'PASS' if gd==0 else 'FAIL'}")
print(f"  AI buzzwords:      {ga:4d} {'PASS' if ga==0 else 'FAIL'}")
print(f"  Claude/Anthropic:  {gc:4d} {'PASS' if gc==0 else 'FAIL'}")
print(f"  Total words:       {sum(awcs)+sum(twcs):,}")
print(f"\n  RESULT: {'ALL CHECKS PASSED' if gs+gd+ga+gc==0 else 'ISSUES REMAIN'}")
print(f"{'='*70}")
