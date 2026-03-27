#!/bin/bash

# PERFECTION AGENT GAMMA - FINAL CLEANUP
# Fix malformed sequences and ensure absolute quality

echo "=== PERFECTION AGENT GAMMA - FINAL CLEANUP ==="

# Fix nginx-config-generator malformed sequence
echo "Fixing nginx-config-generator..."
sed -i '' 's|name="viewport"/>\\\1\\n <meta name="description"|name="viewport"/>\
<title>Nginx Config Generator - SSL, Reverse Proxy, Caching, Rate Limiting | Free Tool</title>\
<meta name="description"|g' nginx-config-generator/index.html

# Fix neumorphism-generator malformed sequence
echo "Fixing neumorphism-generator..."
sed -i '' 's|name="viewport"/>\\\1\\n <meta content=|name="viewport"/>\
<title>Neumorphism Generator - CSS Soft UI Builder | Free Tool</title>\
<meta content=|g' neumorphism-generator/index.html

echo "Final cleanup complete!"
echo ""

echo "=== FINAL VERIFICATION ==="
missing_titles=$(find . -name "index.html" -path "./[n-s]*" -exec grep -L "<title>" {} \; | wc -l | tr -d ' ')
echo "Missing title tags: $missing_titles"

if [ "$missing_titles" -eq "0" ]; then
    echo "✅ PERFECTION ACHIEVED - All title tags present"
else
    echo "⚠️  Still missing $missing_titles title tags"
fi