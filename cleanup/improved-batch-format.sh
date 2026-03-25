#!/bin/bash
# ============================================================================
# IMPROVED BATCH TOOL FORMATTER - Agent 2 Mission
# ============================================================================

# Source the anti-AI formatter
source ~/zovo-workspaces/quality-pipeline/scripts/anti-ai-formatter.sh

TOOLS_PROCESSED=0
VIOLATIONS_FIXED=0
START_TIME=$(date +%s)

echo "=== IMPROVED BATCH TOOL FORMATTING AGENT 2 - START ==="
echo "Mission: Fix AI formatting violations in all tool pages"
echo "Started at: $(date)"
echo ""

# Custom HTML cleaner function that's more comprehensive
improved_clean_html() {
    local file="$1"
    local changes_made=0

    if [[ ! -f "$file" ]]; then
        echo "File not found: $file"
        return 1
    fi

    # Create backup
    cp "$file" "${file}.bak"

    # Apply our own comprehensive cleaning
    python3 << PYTHON
import re

with open("${file}", "r", encoding='utf-8') as f:
    content = f.read()

original_content = content
changes = []

# Fix em/en dashes (but not CSS variables)
em_dash_count = content.count('\u2014')
en_dash_count = content.count('\u2013')
double_dash_count = len(re.findall(r'(?<!-)--(?![-:])', content))

if em_dash_count > 0:
    content = content.replace('\u2014', ', ')
    changes.append(f"Fixed {em_dash_count} em dashes")

if en_dash_count > 0:
    content = content.replace('\u2013', ', ')
    changes.append(f"Fixed {en_dash_count} en dashes")

if double_dash_count > 0:
    # Only replace -- that are not CSS variables
    content = re.sub(r'(?<!-)--(?![-:])', ', ', content)
    changes.append(f"Fixed {double_dash_count} double dashes")

# Fix bold tags
strong_tags = len(re.findall(r'<strong[^>]*>.*?</strong>', content, re.DOTALL))
b_tags = len(re.findall(r'<b[^>]*>.*?</b>', content, re.DOTALL))
if strong_tags > 0 or b_tags > 0:
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'\\1', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'\\1', content, flags=re.DOTALL)
    changes.append(f"Fixed {strong_tags + b_tags} bold tags")

# Fix colon headings (but preserve URLs, CSS, and time formats)
heading_patterns = []
for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
    pattern = f'<{tag}[^>]*>([^<]*:[^<]*)</{tag}>'
    matches = re.findall(pattern, content)
    for match in matches:
        # Skip if it looks like a URL, time, or CSS
        if not any(x in match.lower() for x in ['http', 'https', ':', 'am', 'pm', 'step']):
            if ':' in match and not match.startswith('Step'):
                parts = match.split(':', 1)
                if len(parts) == 2:
                    new_heading = parts[1].strip()
                    content = content.replace(f'>{match}<', f'>{new_heading}<')
                    heading_patterns.append(match)

if heading_patterns:
    changes.append(f"Fixed {len(heading_patterns)} colon headings")

# Fix common AI phrases
ai_phrases = {
    'comprehensive': 'complete',
    'optimize': 'improve',
    'optimized': 'enhanced',
    'optimizing': 'improving',
    'leverage': 'use',
    'leveraging': 'using',
    'utilize': 'use',
    'utilizing': 'using',
    'robust': 'strong',
    'seamlessly': 'smoothly',
    'seamless': 'smooth',
    'delve': 'look at',
    'delving': 'looking at',
    'facilitate': 'help',
    'facilitating': 'helping'
}

ai_fixed = []
for phrase, replacement in ai_phrases.items():
    # Use word boundaries to avoid partial replacements
    pattern = r'\\b' + re.escape(phrase) + r'\\b'
    count = len(re.findall(pattern, content, re.IGNORECASE))
    if count > 0:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        ai_fixed.append(f"{phrase}x{count}")

if ai_fixed:
    changes.append(f"Fixed AI phrases: {', '.join(ai_fixed[:5])}")

# Clean up multiple commas/spaces
content = re.sub(r',\s*,+', ',', content)
content = re.sub(r'\s+', ' ', content)

# Write back if changes were made
if content != original_content:
    with open("${file}", "w", encoding='utf-8') as f:
        f.write(content)

    for change in changes:
        print(f"  FIXED: {change}")
    print(f"  Total changes: {len(changes)}")
    exit(len(changes))
else:
    print("  No changes needed")
    exit(0)
PYTHON

    return $?
}

# Get all tool directories
TOOL_DIRS=($(find . -name "index.html" -path "./*/index.html" | grep -v ".git" | grep -v "guides" | grep -v "articles" | sort))
TOTAL_TOOLS=${#TOOL_DIRS[@]}

echo "Found $TOTAL_TOOLS tool directories to process"
echo ""

# Process each tool
for tool_path in "${TOOL_DIRS[@]}"; do
    TOOLS_PROCESSED=$((TOOLS_PROCESSED + 1))
    tool_name=$(dirname "$tool_path" | sed 's|^./||')

    # Skip if already processed today
    if git log --oneline --since="1 day ago" --grep="Format: $tool_name" | grep -q "Format: $tool_name"; then
        echo "[$TOOLS_PROCESSED/$TOTAL_TOOLS] SKIP: $tool_name (already processed today)"
        continue
    fi

    echo "[$TOOLS_PROCESSED/$TOTAL_TOOLS] PROCESSING: $tool_name"

    # Apply our improved cleaner
    changes_made=$(improved_clean_html "$tool_path" 2>&1)
    changes_count=$?

    if [[ $changes_count -gt 0 ]]; then
        VIOLATIONS_FIXED=$((VIOLATIONS_FIXED + changes_count))

        # Get final audit score
        final_audit=$(audit_ai_patterns "$tool_path" 2>/dev/null | grep "SCORE:" | awk '{print $2}')

        # Commit the changes
        git add "$tool_path"
        git commit -q -m "Format: $tool_name - removed AI patterns

$changes_made
Final score: $final_audit"

        echo "  SUCCESS: Applied $changes_count changes, score: $final_audit"
    else
        echo "  CLEAN: No violations found"
    fi

    # Progress check every 25 tools
    if (( TOOLS_PROCESSED % 25 == 0 )); then
        elapsed=$(($(date +%s) - START_TIME))
        rate=$(echo "scale=2; $TOOLS_PROCESSED / ($elapsed / 60)" | bc -l 2>/dev/null || echo "~")
        echo ""
        echo "=== PROGRESS CHECK ==="
        echo "Tools processed: $TOOLS_PROCESSED/$TOTAL_TOOLS"
        echo "Violations fixed: $VIOLATIONS_FIXED"
        echo "Rate: $rate tools/minute"
        echo "Elapsed: ${elapsed}s"
        echo ""
    fi
done

# Final summary
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
echo ""
echo "=== IMPROVED BATCH TOOL FORMATTING COMPLETE ==="
echo "Total tools processed: $TOOLS_PROCESSED"
echo "Total violations fixed: $VIOLATIONS_FIXED"
echo "Total time: ${TOTAL_TIME}s"
echo "Average rate: $(echo "scale=2; $TOOLS_PROCESSED / ($TOTAL_TIME / 60)" | bc -l 2>/dev/null || echo "N/A") tools/minute"
echo "Completed at: $(date)"