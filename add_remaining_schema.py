#!/usr/bin/env python3
"""
Add Remaining Schema - Agent 2
Adds JSON-LD schema markup to remaining G-N tools that need it
"""

import os
import re
import json
from pathlib import Path

def generate_comprehensive_schema(tool_name):
    """Generate comprehensive schema for any tool type"""

    clean_name = tool_name.replace('-', ' ').title()

    # Base schema structure
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

    # Add tool-specific descriptions and categories
    if 'calculator' in tool_name:
        schema["applicationSubCategory"] = "Calculator"
        if 'gpa' in tool_name:
            schema["description"] = "Calculate GPA from grades and credit hours with accurate weighted averages."
        elif 'loan' in tool_name or 'mortgage' in tool_name:
            schema["description"] = f"Calculate {tool_name.replace('-', ' ')} payments, rates, and amortization schedules."
        elif 'grade' in tool_name:
            schema["description"] = "Calculate final grades, weighted scores, and academic performance metrics."
        elif 'lease' in tool_name:
            schema["description"] = "Calculate lease payments, terms, and compare lease vs buy scenarios."
        else:
            schema["description"] = f"Calculate {tool_name.replace('-calculator', '').replace('-', ' ')} with precision."

    elif 'converter' in tool_name or '-to-' in tool_name:
        schema["applicationSubCategory"] = "Converter"
        schema["description"] = f"Convert {tool_name.replace('-converter', '').replace('-to-', ' to ').replace('-', ' ')} instantly."

    elif 'generator' in tool_name:
        schema["applicationSubCategory"] = "Generator"
        if 'gradient' in tool_name:
            schema["description"] = "Generate CSS gradients and color transitions for web design."
        elif 'neumorphism' in tool_name:
            schema["description"] = "Generate neumorphism CSS code for modern soft UI elements."
        elif 'nginx' in tool_name:
            schema["description"] = "Generate Nginx configuration files with SSL and security settings."
        else:
            schema["description"] = f"Generate {tool_name.replace('-generator', '').replace('-', ' ')} content."

    elif 'solver' in tool_name:
        schema["applicationSubCategory"] = "Educational Tool"
        schema["description"] = f"Solve {tool_name.replace('-solver', '').replace('-', ' ')} problems with step-by-step solutions."

    elif 'editor' in tool_name:
        schema["applicationSubCategory"] = "Editor"
        schema["description"] = f"Edit {tool_name.replace('-editor', '').replace('-', ' ')} with live preview and formatting."

    else:
        # Generic description based on tool name
        schema["description"] = f"Free online {clean_name.lower()} tool with accurate results and easy interface."

    return json.dumps(schema, indent=2)

def add_remaining_schema():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Tools that still need schema based on Loop 2 observations
    remaining_schema_tools = [
        'ico-converter', 'ics-calendar-generator', 'ideal-body-weight-calculator',
        'ideal-gas-law-calculator', 'image-metadata-viewer', 'image-to-text-ocr',
        'inches-to-square-feet-calculator', 'inr-to-usd-converter',
        'interest-only-loan-calculator', 'land-loan-calculator', 'lease-calculator',
        'life-expectancy-calculator', 'linear-equation-solver', 'neumorphism-generator'
    ]

    fixes_made = 0

    for tool_name in remaining_schema_tools[:12]:  # Process 12 tools
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
            schema_json = generate_comprehensive_schema(tool_name)

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
                print(f"✅ {tool_name}: Added comprehensive schema markup")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added comprehensive schema markup to {fixes_made} remaining tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_remaining_schema()