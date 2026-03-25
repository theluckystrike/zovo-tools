#!/usr/bin/env python3
"""
Update sitemap.xml with all tool URLs
"""

import os
import glob
from datetime import datetime

TOOLS_DIR = "."
BASE_URL = "https://zovo.one/free-tools"

def generate_sitemap():
    """Generate updated sitemap.xml"""
    # Get all tool directories with index.html
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    # Filter out articles directory as it's handled separately
    tool_files = [f for f in files if '/articles/' not in f]

    # Get current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Generate sitemap XML
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://zovo.one/</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://zovo.one/free-tools/</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
'''.format(date=current_date)

    # Add tool URLs
    for filepath in tool_files:
        tool_name = os.path.basename(os.path.dirname(filepath))
        if tool_name and tool_name != 'articles':
            sitemap_content += f'''  <url>
    <loc>{BASE_URL}/{tool_name}/</loc>
    <lastmod>{current_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    sitemap_content += '</urlset>\n'

    return sitemap_content, len(tool_files)

def main():
    print("Updating sitemap.xml...")
    print("=" * 50)

    sitemap_content, tool_count = generate_sitemap()

    # Write sitemap
    sitemap_path = os.path.join(TOOLS_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    print(f"✓ Sitemap updated with {tool_count + 2} URLs")
    print(f"✓ Base URLs: 2")
    print(f"✓ Tool URLs: {tool_count}")
    print("=" * 50)

if __name__ == '__main__':
    main()