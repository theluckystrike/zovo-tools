#!/usr/bin/env python3
"""
Create Missing Index Files - Agent 2
Creates basic index.html for tools missing them
"""

import os
from pathlib import Path

def create_basic_index(tool_name):
    """Create a basic index.html template for missing tools"""

    tool_title = tool_name.replace('-', ' ').title()

    # Basic HTML template
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tool_title} - Free Online Tool</title>
    <meta name="description" content="Free online {tool_title.lower()} tool. Easy to use and accurate results.">
    <link rel="canonical" href="https://tools.zovo.one/free-tools/{tool_name}/">

    <!-- Open Graph -->
    <meta property="og:title" content="{tool_title} - Free Online Tool">
    <meta property="og:description" content="Free online {tool_title.lower()} tool. Easy to use and accurate results.">
    <meta property="og:url" content="https://tools.zovo.one/free-tools/{tool_name}/">
    <meta property="og:type" content="website">

    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "{tool_title} - Free Online Tool",
        "url": "https://tools.zovo.one/free-tools/{tool_name}/",
        "description": "Free online {tool_title.lower()} tool. Easy to use and accurate results.",
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Any",
        "offers": {{
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }},
        "creator": {{
            "@type": "Person",
            "name": "Michael Lip"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Zovo Tools",
            "url": "https://tools.zovo.one/"
        }}
    }}
    </script>

    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            color: #e0e0e8;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
        h1 {{ color: #00ff88; margin-bottom: 1rem; }}
        .tool-area {{
            background: #12121a;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{tool_title}</h1>
            <p>Free online {tool_title.lower()} tool. Coming soon!</p>
        </header>

        <main>
            <div class="tool-area">
                <p>This tool is under development. Check back soon for the full functionality.</p>
            </div>
        </main>

        <footer>
            <p>Built by Michael Lip | Part of Zovo Tools</p>
        </footer>
    </div>
</body>
</html>'''

    return html_template

def create_missing_index_files():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Tools missing index.html
    missing_tools = [
        'harvard-citation-generator',
        'hkd-to-usd-converter',
        'kr-to-usd-converter',
        'naira-to-usd-converter'
    ]

    created = 0

    for tool_name in missing_tools:
        tool_dir = base_dir / tool_name

        if tool_dir.exists():
            index_path = tool_dir / 'index.html'

            if not index_path.exists():
                html_content = create_basic_index(tool_name)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                print(f"✅ Created index.html for {tool_name}")
                created += 1
            else:
                print(f"⚠️ {tool_name}: index.html already exists")
        else:
            print(f"❌ {tool_name}: directory not found")

    print(f"\n🔧 Created {created} index.html files")
    return created > 0

if __name__ == "__main__":
    create_missing_index_files()