#!/usr/bin/env python3
"""Fix missing loading='lazy' on YouTube iframes."""

import os
import re

ROOT = "/Users/mike/zovo-workspaces/zovo-tools"

files_to_fix = [
    "apa-format-checker/index.html",
    "api-request-builder/index.html",
    "bmi-prime-calculator/index.html",
    "circuit-breaker-sizing-calculator/index.html",
    "completing-the-square-calculator/index.html",
    "cooking-converter/index.html",
    "css-clip-path-generator/index.html",
    "fuel-cost-calculator/index.html",
    "graphing-scientific-calculator/index.html",
    "html-email-builder/index.html",
    "interest-rate-calculator/index.html",
    "mixed-fraction-calculator/index.html",
    "mla-citation-generator/index.html",
    "mortgage-quote-calculator/index.html",
    "paycheck-calculator-arkansas/index.html",
    "paycheck-calculator-kansas/index.html",
    "paycheck-calculator-oklahoma/index.html",
    "paycheck-calculator-south-carolina/index.html",
    "paycheck-estimator/index.html",
    "recycling-guide/index.html",
    "regex-generator/index.html",
    "shoe-size-converter/index.html",
    "student-loan-calculator/index.html",
    "svg-animator/index.html",
    "tax-refund-calculator/index.html",
    "trademark-search/index.html",
    "western-union-exchange-rate-calculator/index.html",
]

fixed = 0
for rel_path in files_to_fix:
    fpath = os.path.join(ROOT, rel_path)
    if not os.path.exists(fpath):
        print(f"  SKIP (not found): {rel_path}")
        continue

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find YouTube iframes missing loading="lazy"
    # Pattern: <iframe ...youtube.com/embed/... without loading="lazy"
    def add_lazy(match):
        tag = match.group()
        if 'youtube.com/embed/' in tag and 'loading=' not in tag:
            # Add loading="lazy" before the closing >
            tag = tag.rstrip('>').rstrip('/')
            tag = tag.rstrip()
            tag += ' loading="lazy">'
            return tag
        return match.group()

    new_content = re.sub(r'<iframe[^>]*youtube\.com/embed/[^>]*>', add_lazy, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"  Fixed: {rel_path}")
    else:
        print(f"  No change needed: {rel_path}")

print(f"\nFixed {fixed} files with missing loading='lazy'")
