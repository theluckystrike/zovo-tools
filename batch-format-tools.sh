#!/bin/bash
# ============================================================================
# BATCH TOOL FORMATTER - Agent 2 Mission
# ============================================================================
# Systematically scan and fix AI formatting violations in all tool pages
# Mission: Clean all 600 tool directories in ~/zovo-workspaces/zovo-tools/

# Source the anti-AI formatter
source ~/zovo-workspaces/quality-pipeline/scripts/anti-ai-formatter.sh

TOOLS_PROCESSED=0
VIOLATIONS_FIXED=0
START_TIME=$(date +%s)

echo "=== BATCH TOOL FORMATTING AGENT 2 - START ==="
echo "Mission: Fix AI formatting violations in all tool pages"
echo "Started at: $(date)"
echo ""

# Get all tool directories (excluding .git, guides, articles)
TOOL_DIRS=($(find . -name "index.html" -path "./*/index.html" | grep -v ".git" | grep -v "guides" | grep -v "articles" | sort))
TOTAL_TOOLS=${#TOOL_DIRS[@]}

echo "Found $TOTAL_TOOLS tool directories to process"
echo ""

# Process each tool
for tool_path in "${TOOL_DIRS[@]}"; do
    TOOLS_PROCESSED=$((TOOLS_PROCESSED + 1))
    tool_name=$(dirname "$tool_path" | sed 's|^./||')

    # Skip if already processed (check git log)
    if git log --oneline --since="1 day ago" --grep="Format: $tool_name" | grep -q "Format: $tool_name"; then
        echo "[$TOOLS_PROCESSED/$TOTAL_TOOLS] SKIP: $tool_name (already processed today)"
        continue
    fi

    echo "[$TOOLS_PROCESSED/$TOTAL_TOOLS] PROCESSING: $tool_name"

    # Audit for violations
    violations=$(audit_ai_patterns "$tool_path" 2>/dev/null | grep "Total issues:" | awk '{print $3}')

    if [[ "$violations" == "0" ]]; then
        echo "  CLEAN: No violations found"
        continue
    fi

    echo "  FOUND: $violations violation types detected"

    # Apply deep clean
    deep_clean_result=$(deep_clean_html "$tool_path" 2>&1)

    # Extract changes from the result
    changes_count=$(echo "$deep_clean_result" | grep "Total:" | tail -1 | awk '{print $2}')

    if [[ -n "$changes_count" && "$changes_count" != "0" ]]; then
        VIOLATIONS_FIXED=$((VIOLATIONS_FIXED + changes_count))

        # Handle remaining AI phrases manually
        remaining_phrases=$(audit_ai_patterns "$tool_path" 2>/dev/null | grep "AI PHRASES" || echo "")
        if [[ -n "$remaining_phrases" ]]; then
            echo "  MANUAL: Fixing remaining AI phrases..."
            # Simple replacements for common AI phrases
            sed -i '' 's/comprehensive/complete/gi' "$tool_path"
            sed -i '' 's/\boptimize\b/improve/gi' "$tool_path"
            sed -i '' 's/\boptimized\b/enhanced/gi' "$tool_path"
            sed -i '' 's/\bleverage\b/use/gi' "$tool_path"
            sed -i '' 's/\butilize\b/use/gi' "$tool_path"
            sed -i '' 's/\brobust\b/strong/gi' "$tool_path"
            sed -i '' 's/\bseamlessly\b/smoothly/gi' "$tool_path"
            sed -i '' 's/\bdelve\b/look at/gi' "$tool_path"
        fi

        # Final audit to get clean score
        final_score=$(audit_ai_patterns "$tool_path" 2>/dev/null | grep "SCORE:" | awk '{print $2}')

        # Commit the changes
        git add "$tool_path"
        git commit -m "Format: $tool_name - removed AI patterns

$deep_clean_result
Final score: $final_score" >/dev/null 2>&1

        echo "  FIXED: Applied $changes_count changes, score: $final_score"
    else
        echo "  ERROR: No changes applied by deep_clean_html"
    fi

    # Progress check every 10 tools
    if (( TOOLS_PROCESSED % 10 == 0 )); then
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
echo "=== BATCH TOOL FORMATTING COMPLETE ==="
echo "Total tools processed: $TOOLS_PROCESSED"
echo "Total violations fixed: $VIOLATIONS_FIXED"
echo "Total time: ${TOTAL_TIME}s"
echo "Average rate: $(echo "scale=2; $TOOLS_PROCESSED / ($TOTAL_TIME / 60)" | bc -l 2>/dev/null || echo "N/A") tools/minute"
echo "Completed at: $(date)"