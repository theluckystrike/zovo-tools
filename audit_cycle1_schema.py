#!/usr/bin/env python3
"""
Cycle 1: Schema Markup Validation Audit
Scans all tool pages for JSON-LD schema markup quality issues.
Fixes broken JSON, removes duplicates, cleans up junk blocks.
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
    "pages_without_schema_list": [],
}

def find_tool_pages():
    """Find all tool and article index.html files."""
    pages = []
    for entry in sorted(os.listdir(BASE_DIR)):
        full = BASE_DIR / entry
        if full.is_dir() and (full / "index.html").exists():
            if entry in ("cleanup", "recovery_documentation", "categories"):
                continue
            if entry == "articles":
                continue  # handled below
            pages.append(full / "index.html")

    articles_dir = BASE_DIR / "articles"
    if articles_dir.exists():
        for entry in sorted(os.listdir(articles_dir)):
            full = articles_dir / entry
            if full.is_dir() and (full / "index.html").exists():
                pages.append(full / "index.html")

    return pages

def extract_json_ld_with_positions(html_content):
    """Extract all JSON-LD blocks with their start/end positions in the HTML."""
    pattern = r'<script\s+type=["\']application/ld\+json["\']>\s*(.*?)\s*</script>'
    results = []
    for m in re.finditer(pattern, html_content, re.DOTALL | re.IGNORECASE):
        results.append({
            "full_match": m.group(0),
            "json_content": m.group(1),
            "start": m.start(),
            "end": m.end(),
        })
    return results

def try_fix_json(raw_json):
    """Attempt to fix common JSON issues."""
    fixed = raw_json.strip()

    # If it contains escaped </script> tags or HTML after JSON, try to extract just the JSON part
    # Look for the pattern where valid JSON ends and junk begins
    if '<\\/' in fixed or '</' in fixed:
        # Try to find where the JSON object/array ends
        brace_depth = 0
        bracket_depth = 0
        in_string = False
        escape_next = False
        for i, c in enumerate(fixed):
            if escape_next:
                escape_next = False
                continue
            if c == '\\':
                escape_next = True
                continue
            if c == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '{':
                brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0 and bracket_depth == 0:
                    candidate = fixed[:i+1]
                    try:
                        parsed = json.loads(candidate)
                        return candidate, parsed
                    except:
                        pass
            elif c == '[':
                bracket_depth += 1
            elif c == ']':
                bracket_depth -= 1
                if bracket_depth == 0 and brace_depth == 0:
                    candidate = fixed[:i+1]
                    try:
                        parsed = json.loads(candidate)
                        return candidate, parsed
                    except:
                        pass

    # Remove trailing commas before } or ]
    fixed = re.sub(r',\s*([}\]])', r'\1', fixed)

    # Fix unclosed brackets
    open_braces = fixed.count('{')
    close_braces = fixed.count('}')
    open_brackets = fixed.count('[')
    close_brackets = fixed.count(']')

    if open_braces > close_braces:
        fixed += '}' * (open_braces - close_braces)
    if open_brackets > close_brackets:
        fixed += ']' * (open_brackets - close_brackets)

    try:
        parsed = json.loads(fixed)
        return fixed, parsed
    except json.JSONDecodeError:
        return None, None

def validate_page(filepath):
    """Validate all JSON-LD blocks in a single page."""
    page_issues = []
    modified = False

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        page_issues.append(f"Could not read file: {e}")
        return page_issues, False, ""

    original_content = content
    blocks = extract_json_ld_with_positions(content)

    if not blocks:
        REPORT["pages_without_schema"] += 1
        rel_path = str(filepath.relative_to(BASE_DIR))
        REPORT["pages_without_schema_list"].append(rel_path)
        return page_issues, False, content

    REPORT["pages_with_schema"] += 1

    faq_blocks = []  # (full_match, parsed)
    blocks_to_remove = []  # full_match strings to remove

    for i, block_info in enumerate(blocks):
        raw = block_info["json_content"]
        full_match = block_info["full_match"]

        # Try to parse as-is
        try:
            parsed = json.loads(raw)
            REPORT["valid_json_blocks"] += 1
        except json.JSONDecodeError as e:
            # Try to fix
            fixed_str, fixed_parsed = try_fix_json(raw)
            if fixed_parsed:
                REPORT["valid_json_blocks"] += 1
                # Replace the block with the fixed version
                new_script = f'<script type="application/ld+json">{fixed_str}</script>'
                content = content.replace(full_match, new_script, 1)
                modified = True
                REPORT["fixes_applied"] += 1
                page_issues.append(f"Block {i}: Fixed invalid JSON ({str(e)[:60]})")
                parsed = fixed_parsed
            else:
                REPORT["invalid_json_blocks"] += 1
                # Remove the broken block entirely
                blocks_to_remove.append(full_match)
                page_issues.append(f"Block {i}: Removed unfixable broken JSON-LD ({str(e)[:60]})")
                REPORT["fixes_applied"] += 1
                continue

        # Validate required fields
        if isinstance(parsed, dict):
            if "@context" not in parsed:
                REPORT["missing_context"] += 1
                page_issues.append(f"Block {i}: Missing @context")
            if "@type" not in parsed:
                REPORT["missing_type"] += 1
                page_issues.append(f"Block {i}: Missing @type")
            else:
                if parsed["@type"] == "FAQPage":
                    entities = parsed.get("mainEntity", [])
                    count = len(entities) if isinstance(entities, list) else 0
                    faq_blocks.append((full_match, parsed, count))
                if parsed["@type"] == "WebApplication":
                    if "name" not in parsed:
                        REPORT["missing_name_on_webapp"] += 1
                        page_issues.append(f"Block {i}: WebApplication missing 'name'")
        elif isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    if "@type" not in item:
                        REPORT["missing_type"] += 1
                    if item.get("@type") == "FAQPage":
                        entities = item.get("mainEntity", [])
                        count = len(entities) if isinstance(entities, list) else 0
                        faq_blocks.append((full_match, item, count))

    # Remove broken blocks
    for full_match in blocks_to_remove:
        if full_match in content:
            content = content.replace(full_match, '', 1)
            modified = True

    # Handle duplicate FAQPage schemas
    if len(faq_blocks) > 1:
        REPORT["duplicate_faq_pages"] += 1
        page_issues.append(f"Found {len(faq_blocks)} duplicate FAQPage schemas")

        # Find the best one (most questions)
        best_idx = max(range(len(faq_blocks)), key=lambda i: faq_blocks[i][2])
        best_count = faq_blocks[best_idx][2]

        # Collect unique full_match strings to remove (skip the best one)
        seen = set()
        for idx, (full_match, parsed_faq, count) in enumerate(faq_blocks):
            if idx == best_idx:
                continue
            if full_match in seen:
                continue
            seen.add(full_match)

        # Remove all duplicate FAQPage blocks (not the best)
        removed = 0
        for fm in seen:
            # Count how many times this exact block appears
            while fm in content:
                # But keep one instance if it's the same as the best
                if fm == faq_blocks[best_idx][0]:
                    break
                content = content.replace(fm, '', 1)
                removed += 1
                modified = True
                REPORT["fixes_applied"] += 1

        if removed > 0:
            page_issues.append(f"Removed {removed} duplicate FAQPage blocks, kept best with {best_count} questions")

    return page_issues, modified, content

def main():
    pages = find_tool_pages()
    print(f"Found {len(pages)} pages to scan")

    files_modified = 0
    all_issues = []

    for filepath in pages:
        REPORT["total_pages_scanned"] += 1
        rel_path = str(filepath.relative_to(BASE_DIR))

        issues, modified, new_content = validate_page(filepath)

        if issues:
            all_issues.append((rel_path, issues))

        if modified:
            try:
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

    # Save full report
    report_path = BASE_DIR / "audit_cycle1_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "stats": {
                "total_pages_scanned": REPORT["total_pages_scanned"],
                "pages_with_schema": REPORT["pages_with_schema"],
                "pages_without_schema": REPORT["pages_without_schema"],
                "valid_json_blocks": REPORT["valid_json_blocks"],
                "invalid_json_blocks": REPORT["invalid_json_blocks"],
                "duplicate_faq_pages": REPORT["duplicate_faq_pages"],
                "missing_context": REPORT["missing_context"],
                "missing_type": REPORT["missing_type"],
                "missing_name_on_webapp": REPORT["missing_name_on_webapp"],
                "fixes_applied": REPORT["fixes_applied"],
                "files_modified": files_modified,
            },
            "pages_without_schema": REPORT["pages_without_schema_list"],
            "issues": [(p, i) for p, i in all_issues],
        }, f, indent=2)
    print(f"\nFull report saved to: {report_path}")

if __name__ == "__main__":
    main()
