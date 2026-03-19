#!/bin/bash
# Autonomous tool deployment script for zovo-tools
# Usage: ./deploy-tool.sh <tool-slug>
#
# This script:
# 1. Commits the tool
# 2. Pushes to GitHub
# 3. GitHub Pages auto-deploys
# 4. Submits to IndexNow
# 5. Updates sitemap

TOOL_SLUG="$1"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DOMAIN="zovo.one/free-tools"

if [ -z "$TOOL_SLUG" ]; then
  echo "Usage: $0 <tool-slug>"
  exit 1
fi

if [ ! -f "${REPO_DIR}/${TOOL_SLUG}/index.html" ]; then
  echo "ERROR: ${TOOL_SLUG}/index.html not found"
  exit 1
fi

cd "$REPO_DIR"

# Add to sitemap if not already there
if ! grep -q "$TOOL_SLUG" sitemap.xml; then
  sed -i '' "/<\/urlset>/i\\
  <url>\\
    <loc>https://${DOMAIN}/${TOOL_SLUG}/</loc>\\
    <lastmod>$(date +%Y-%m-%d)</lastmod>\\
    <changefreq>weekly</changefreq>\\
    <priority>0.9</priority>\\
  </url>" sitemap.xml
  echo "Added $TOOL_SLUG to sitemap"
fi

# Update index.html tool count
TOOL_COUNT=$(find . -maxdepth 2 -name "index.html" ! -path "./index.html" | wc -l | tr -d ' ')
echo "Total tools: $TOOL_COUNT"

# Commit and push
git add "${TOOL_SLUG}/" sitemap.xml index.html
git commit -m "Deploy ${TOOL_SLUG}"
git push

echo "Deployed: https://${DOMAIN}/${TOOL_SLUG}/"
echo "GitHub Pages will build automatically in ~30 seconds"
