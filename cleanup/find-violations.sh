#!/bin/bash

# Source the anti-AI formatter
source ~/zovo-workspaces/quality-pipeline/scripts/anti-ai-formatter.sh 2>/dev/null

echo "Finding tools with AI formatting violations..."
echo ""

violations_found=0

find . -name "index.html" -path "./*/index.html" | head -100 | while read file; do
  tool_name=$(dirname "$file" | sed 's|^./||')

  # Run audit and capture output
  result=$(audit_ai_patterns "$file" 2>/dev/null)
  violations=$(echo "$result" | grep "Total issues:" | awk '{print $3}')
  score=$(echo "$result" | grep "SCORE:" | awk '{print $2}')

  if [[ "$violations" != "0" ]] && [[ -n "$violations" ]]; then
    echo "$tool_name: $violations violations (score: $score)"
    violations_found=$((violations_found + 1))
  fi
done

echo ""
echo "Found $violations_found tools with violations out of first 100 checked"