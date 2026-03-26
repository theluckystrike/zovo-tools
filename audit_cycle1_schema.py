#!/usr/bin/env python3
"""
Cycle 1: Schema Markup Validation Audit
Scans all tool pages for JSON-LD schema markup quality issues.
"""

import os
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")
REPORT = {
    "total_pages_scanned": 0,
    "pages_with_schema": 0,
    "pages_without_schema": 0,
    "valid_json_blocks": 0,
    "invalid_json_blocks": 0,
    "duplicate_faq_pages": 0,
    "missing_context": 0,
    "missing_type": 0,
    "missing_name_on_webapp": 0,
    "fixes_applied": 0,
    "issues": [],
    "pages_without_schema_list": [],
}

def find_tool_pages():
    """Find all tool and article index.html files."""
    pages = []
    for entry in sorted(os.listdir(BASE_DIR)):
        full = BASE_DIR / entry
        if full.is_dir() and (full / "index.html").exists():
            # Skip known non-tool directories
            if entry in ("cleanup", "recovery_documentation", "categories", "articles"):
                continue
            pages.append(full / "index.html")

    # Also scan articles
    articles_dir = BASE_DIR / "articles"
    if articles_dir.exists():
        for entry in sorted(os.listdir(articles_dir)):
            full = articles_dir / entry
            if full.is_dir() and (full / "index.html").exists():
                pages.append(full / "index.html")

    return pages

def extract_json_ld(html_content):
    """Extract all JSON-LD blocks from HTML."""
    pattern = r'<script\s+type=["\']application/ld\+json["\']>\s*(.*?)\s*</script>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    return matches

def try_fix_json(raw_json):
    """Attempt to fix common JSON issues."""
    fixed = raw_json.strip()

    # Remove trailing commas before } or ]
    fixed = re.sub(r',\s*([}\]])', r'\1', fixed)

    # Fix unclosed brackets - count opening vs closing
    open_braces = fixed.count('{')
    close_braces = fixed.count('}')
    open_brackets = fixed.count('[')
    close_brackets = fixed.count(']')

    if open_braces > close_braces:
        fixed += '}' * (open_braces - close_braces)
    if open_brackets > close_brackets:
        fixed += ']' * (open_brackets - close_brackets)

    # Try to parse
    try:
        parsed = json.loads(fixed)
        return fixed, parsed
    except json.JSONDecodeError:
        return None, None

def validate_page(filepath):
    """Validate all JSON-LD blocks in a single page."""
    page_issues = []
    page_fixes = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        page_issues.append(f"Could not read file: {e}")
        return page_issues, page_fixes, content if 'content' in dir() else ""

    blocks = extract_json_ld(content)

    if not blocks:
        REPORT["pages_without_schema"] += 1
        rel_path = str(filepath.relative_to(BASE_DIR))
        REPORT["pages_without_schema_list"].append(rel_path)
        return page_issues, page_fixes, content

    REPORT["pages_with_schema"] += 1

    faq_blocks = []
    webapp_blocks = []
    parsed_blocks = []

    for i, block in enumerate(blocks):
        # Try to parse as-is
        try:
            parsed = json.loads(block)
            REPORT["valid_json_blocks"] += 1
            parsed_blocks.append((i, block, parsed))
        except json.JSONDecodeError as e:
            # Try to fix
            fixed_str, fixed_parsed = try_fix_json(block)
            if fixed_parsed:
                REPORT["valid_json_blocks"] += 1
                page_issues.append(f"Block {i}: Invalid JSON fixed (was: {str(e)[:80]})")
                # Apply fix in content
                content = content.replace(
                    f'>{block}</script>',
                    f'>{fixed_str}</script>',
                    1
                )
                page_fixes.append("fixed_json")
                REPORT["fixes_applied"] += 1
                parsed_blocks.append((i, fixed_str, fixed_parsed))
            else:
                REPORT["invalid_json_blocks"] += 1
                page_issues.append(f"Block {i}: Broken JSON that could not be auto-fixed: {str(e)[:100]}")
                # Remove the broken block
                broken_script = f'<script type="application/ld+json">{block}</script>'
                if broken_script in content:
                    content = content.replace(broken_script, '', 1)
                    page_fixes.append("removed_broken_block")
                    REPORT["fixes_applied"] += 1
                    page_issues.append(f"Block {i}: Removed unfixable broken JSON-LD block")

    # Validate required fields and check for duplicates
    for i, block_str, parsed in parsed_blocks:
        schema_type = None
        if isinstance(parsed, dict):
            if "@context" not in parsed:
                REPORT["missing_context"] += 1
                page_issues.append(f"Block {i}: Missing @context")
            if "@type" not in parsed:
                REPORT["missing_type"] += 1
                page_issues.append(f"Block {i}: Missing @type")
            else:
                schema_type = parsed["@type"]

            if schema_type == "FAQPage":
                faq_blocks.append((i, block_str, parsed))
            if schema_type == "WebApplication":
                if "name" not in parsed:
                    REPORT["missing_name_on_webapp"] += 1
                    page_issues.append(f"Block {i}: WebApplication schema missing 'name' field")
                    webapp_blocks.append((i, block_str, parsed))
        elif isinstance(parsed, list):
            # Some schemas use an array at root
            for item in parsed:
                if isinstance(item, dict):
                    if "@type" not in item:
                        REPORT["missing_type"] += 1
                    if item.get("@type") == "FAQPage":
                        faq_blocks.append((i, block_str, item))

    # Handle duplicate FAQPage schemas - keep only the one with most questions
    if len(faq_blocks) > 1:
        REPORT["duplicate_faq_pages"] += 1
        page_issues.append(f"Found {len(faq_blocks)} duplicate FAQPage schemas")

        # Find the best one (most mainEntity questions)
        best_idx = 0
        best_count = 0
        for idx, (block_i, block_str, parsed_faq) in enumerate(faq_blocks):
            entities = parsed_faq.get("mainEntity", [])
            count = len(entities) if isinstance(entities, list) else 0
            if count > best_count:
                best_count = count
                best_idx = idx

        # Remove all but the best
        for idx, (block_i, block_str, parsed_faq) in enumerate(faq_blocks):
            if idx != best_idx:
                removal_target = f'<script type="application/ld+json">{block_str}</script>'
                # Also try with extra whitespace variations
                removal_target_ws = f'<script type="application/ld+json"> {block_str} </script>'
                if removal_target in content:
                    content = content.replace(removal_target, '', 1)
                    page_fixes.append("removed_duplicate_faq")
                    REPORT["fixes_applied"] += 1
                    page_issues.append(f"Removed duplicate FAQPage schema (block {block_i}), kept best with {best_count} questions")
                elif removal_target_ws in content:
                    content = content.replace(removal_target_ws, '', 1)
                    page_fixes.append("removed_duplicate_faq")
                    REPORT["fixes_applied"] += 1

    return page_issues, page_fixes, content

def main():
    pages = find_tool_pages()
    print(f"Found {len(pages)} pages to scan")

    files_modified = 0
    all_issues = []

    for filepath in pages:
        REPORT["total_pages_scanned"] += 1
        rel_path = str(filepath.relative_to(BASE_DIR))

        issues, fixes, new_content = validate_page(filepath)

        if issues:
            all_issues.append((rel_path, issues))

        if fixes:
            # Write back fixed content
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    original = f.read()
                if new_content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_modified += 1
            except Exception as e:
                print(f"  ERROR writing {rel_path}: {e}")

    # Print report
    print("\n" + "=" * 70)
    print("CYCLE 1: SCHEMA MARKUP VALIDATION REPORT")
    print("=" * 70)
    print(f"Total pages scanned:        {REPORT['total_pages_scanned']}")
    print(f"Pages with schema:          {REPORT['pages_with_schema']}")
    print(f"Pages without schema:       {REPORT['pages_without_schema']}")
    print(f"Valid JSON-LD blocks:       {REPORT['valid_json_blocks']}")
    print(f"Invalid JSON-LD blocks:     {REPORT['invalid_json_blocks']}")
    print(f"Duplicate FAQPage schemas:  {REPORT['duplicate_faq_pages']}")
    print(f"Missing @context:           {REPORT['missing_context']}")
    print(f"Missing @type:              {REPORT['missing_type']}")
    print(f"Missing name on WebApp:     {REPORT['missing_name_on_webapp']}")
    print(f"Fixes applied:              {REPORT['fixes_applied']}")
    print(f"Files modified:             {files_modified}")

    if all_issues:
        print(f"\n--- ISSUES FOUND ({len(all_issues)} pages) ---")
        for rel_path, issues in all_issues:
            print(f"\n  {rel_path}:")
            for issue in issues:
                print(f"    - {issue}")

    if REPORT["pages_without_schema_list"]:
        print(f"\n--- PAGES WITHOUT SCHEMA ({len(REPORT['pages_without_schema_list'])}) ---")
        for p in REPORT["pages_without_schema_list"][:20]:
            print(f"  {p}")
        if len(REPORT["pages_without_schema_list"]) > 20:
            print(f"  ... and {len(REPORT['pages_without_schema_list']) - 20} more")

    # Save full report as JSON
    report_path = BASE_DIR / "audit_cycle1_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "stats": {k: v for k, v in REPORT.items() if k != "issues" and k != "pages_without_schema_list"},
            "pages_without_schema": REPORT["pages_without_schema_list"],
            "issues": [(p, i) for p, i in all_issues],
        }, f, indent=2)
    print(f"\nFull report saved to: {report_path}")

if __name__ == "__main__":
    main()
