#!/usr/bin/env python3
"""
Add N Tools Meta Descriptions - Agent 2
Adds meta descriptions to N tools missing them
"""

import os
import re
from pathlib import Path

def generate_n_meta_description(tool_name):
    """Generate meta descriptions for N tools"""

    if tool_name == 'net-worth-calculator':
        return "Calculate personal net worth by subtracting liabilities from assets. Financial planning tool."
    elif tool_name == 'neumorphism-generator':
        return "Generate neumorphism (soft UI) CSS code for modern, elegant user interface elements."
    elif tool_name == 'nginx-config-generator':
        return "Generate Nginx server configuration files with SSL, redirects, and security settings."
    elif tool_name == 'noise-generator':
        return "Generate white, pink, and brown noise audio for relaxation, focus, and sound masking."
    elif tool_name == 'number-base-converter':
        return "Convert numbers between binary, decimal, hexadecimal, and octal number systems."
    elif tool_name == 'number-system-converter':
        return "Convert between different number systems including binary, octal, decimal, and hex."
    else:
        tool_display = tool_name.replace('-', ' ').title()
        return f"Free {tool_display} tool. Easy to use, accurate results, and completely online."

def add_n_tools_meta_descriptions():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # N tools for meta descriptions
    n_tools = [
        'net-worth-calculator', 'neumorphism-generator', 'nginx-config-generator',
        'noise-generator', 'number-base-converter', 'number-system-converter'
    ]

    fixes_made = 0

    for tool_name in n_tools:
        tool_dir = base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            continue

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if meta description already exists
            if '<meta name="description"' in content:
                continue

            # Generate specific meta description
            meta_desc = generate_n_meta_description(tool_name)

            # Insert meta description after title
            title_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if title_pattern.search(content):
                content = title_pattern.sub(
                    r'\\1\\n    <meta name="description" content="' + meta_desc + '">',
                    content
                )

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added N tool meta description")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added meta descriptions to {fixes_made} N tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_n_tools_meta_descriptions()