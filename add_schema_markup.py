#!/usr/bin/env python3
"""
Add Schema Markup - Agent 2
Adds basic JSON-LD schema markup to tools missing it
"""

import os
import re
import json
from pathlib import Path

def generate_schema(tool_name):
    """Generate appropriate schema markup for tool"""

    # Clean tool name for display
    clean_name = tool_name.replace('-', ' ').title()

    # Basic WebApplication schema
    schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": f"{clean_name} - Free Online Tool",
        "url": f"https://tools.zovo.one/free-tools/{tool_name}/",
        "description": f"Free online {clean_name.lower()} tool. Easy to use and accurate results.",
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Any",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "creator": {
            "@type": "Person",
            "name": "Michael Lip"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Zovo Tools",
            "url": "https://tools.zovo.one/"
        }
    }

    # Add specific categories based on tool type
    if 'calculator' in tool_name:
        schema["applicationSubCategory"] = "Calculator"
    elif 'converter' in tool_name or 'to-' in tool_name:
        schema["applicationSubCategory"] = "Converter"
    elif 'generator' in tool_name:
        schema["applicationSubCategory"] = "Generator"
    elif 'builder' in tool_name or 'maker' in tool_name:
        schema["applicationSubCategory"] = "Creator"

    return json.dumps(schema, indent=2)

def add_schema_markup():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Get G-N tools that are likely missing schema
    priority_tools = [
        'gif-builder', 'gif-maker', 'gif-to-video', 'gitignore-generator',
        'glassmorphism-generator', 'google-keyword-planner-tool', 'gpa-calculator-pro',
        'gradient-generator', 'gradient-text-generator', 'graphing-calculator-online',
        'hash-generator', 'html-encoder', 'html-to-pdf-converter', 'htpasswd-generator',
        'http-header-analyzer', 'http-status-checker', 'ico-converter', 'icon-generator',
        'ics-calendar-generator', 'ideal-body-weight-calculator', 'ideal-gas-law-calculator'
    ]

    fixes_made = 0

    for tool_name in priority_tools[:10]:  # Process first 10
        tool_dir = base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            continue

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if schema already exists
            if '"application/ld+json"' in content:
                continue

            # Generate schema markup
            schema_json = generate_schema(tool_name)

            # Insert schema before closing head tag
            head_close_pattern = re.compile(r'(</head>)', re.IGNORECASE)
            if head_close_pattern.search(content):
                schema_script = f'''
    <script type="application/ld+json">
{schema_json}
    </script>
'''
                content = head_close_pattern.sub(schema_script + r'\1', content)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added schema markup")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\n🔧 Added schema markup to {fixes_made} tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_schema_markup()