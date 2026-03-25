#!/usr/bin/env python3
"""
Add Schema to L-M Tools - Agent 2
Adds JSON-LD schema markup to L and M tools missing it
"""

import os
import re
import json
from pathlib import Path

def generate_l_m_schema(tool_name):
    """Generate schema markup for L and M tools"""

    clean_name = tool_name.replace('-', ' ').title()

    schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": f"{clean_name} - Free Online Tool",
        "url": f"https://tools.zovo.one/free-tools/{tool_name}/",
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

    # Add specific descriptions and categories
    if 'calculator' in tool_name:
        schema["applicationSubCategory"] = "Calculator"
        if 'loan' in tool_name:
            schema["description"] = f"Calculate {tool_name.replace('-', ' ')} payments, rates, and terms online."
        elif 'mortgage' in tool_name:
            schema["description"] = f"Calculate {tool_name.replace('-', ' ')} payments and scenarios."
        else:
            schema["description"] = f"Free {clean_name.lower()} for accurate calculations."
    elif 'converter' in tool_name or '-to-' in tool_name:
        schema["applicationSubCategory"] = "Converter"
        schema["description"] = f"Convert {tool_name.replace('-', ' ').replace('to', 'to')} instantly online."
    elif 'generator' in tool_name:
        schema["applicationSubCategory"] = "Generator"
        schema["description"] = f"Generate {tool_name.replace('-generator', '').replace('-', ' ')} online."
    elif 'maker' in tool_name:
        schema["applicationSubCategory"] = "Creator"
        schema["description"] = f"Create {tool_name.replace('-maker', '').replace('-', ' ')} with ease."
    elif 'solver' in tool_name:
        schema["applicationSubCategory"] = "Calculator"
        schema["description"] = f"Solve {tool_name.replace('-solver', '').replace('-', ' ')} problems step by step."
    elif 'editor' in tool_name:
        schema["applicationSubCategory"] = "Editor"
        schema["description"] = f"Edit {tool_name.replace('-editor', '').replace('-', ' ')} with live preview."
    else:
        schema["description"] = f"Free online {clean_name.lower()} tool. Easy to use and accurate results."

    return json.dumps(schema, indent=2)

def add_l_m_schema():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # L and M tools that likely need schema
    priority_tools = [
        'loan-payoff-calculator', 'loan-simulator', 'markdown-table-generator',
        'math-equation-solver', 'matrix-calculator', 'mean-bp-calculator',
        'mind-map-maker', 'mobile-home-loan-calculator', 'molar-mass-calculator',
        'morse-code-translator', 'mortgage-calculator', 'mortgage-recast-calculator',
        'mov-to-mp3-converter', 'mp3-cutter'
    ]

    fixes_made = 0

    for tool_name in priority_tools[:10]:  # Process 10 tools
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
            schema_json = generate_l_m_schema(tool_name)

            # Insert schema before closing head tag
            head_close_pattern = re.compile(r'(</head>)', re.IGNORECASE)
            if head_close_pattern.search(content):
                schema_script = f'''
    <script type="application/ld+json">
{schema_json}
    </script>
'''
                content = head_close_pattern.sub(schema_script + r'\\1', content)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added L/M schema markup")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added schema markup to {fixes_made} L/M tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_l_m_schema()