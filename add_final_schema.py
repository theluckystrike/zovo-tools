#!/usr/bin/env python3
"""
Add Final Schema - Agent 2
Adds JSON-LD schema to the last remaining tools that need it
"""

import os
import re
import json
from pathlib import Path

def generate_final_tool_schema(tool_name):
    """Generate schema for final remaining tools"""

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

    # Add specific categories and descriptions
    if tool_name == 'linear-equation-solver':
        schema["applicationSubCategory"] = "Educational Tool"
        schema["description"] = "Solve linear equations and systems of equations with step-by-step solutions."
    elif tool_name == 'neumorphism-generator':
        schema["applicationSubCategory"] = "Design Tool"
        schema["description"] = "Generate neumorphism CSS code for modern soft UI design elements."
    elif tool_name == 'mixed-fraction-calculator':
        schema["applicationSubCategory"] = "Calculator"
        schema["description"] = "Calculate with mixed fractions, convert between improper and mixed numbers."
    elif tool_name == 'molarity-calculator':
        schema["applicationSubCategory"] = "Calculator"
        schema["description"] = "Calculate molarity concentration from moles of solute and solution volume."
    elif tool_name == 'kmh-mph-converter':
        schema["applicationSubCategory"] = "Converter"
        schema["description"] = "Convert between kilometers per hour and miles per hour instantly."
    elif tool_name == 'inflation-calculator':
        schema["applicationSubCategory"] = "Calculator"
        schema["description"] = "Calculate inflation impact on purchasing power over time periods."
    else:
        # Generic schema
        if 'calculator' in tool_name:
            schema["applicationSubCategory"] = "Calculator"
        elif 'converter' in tool_name:
            schema["applicationSubCategory"] = "Converter"
        elif 'generator' in tool_name:
            schema["applicationSubCategory"] = "Generator"

        schema["description"] = f"Free online {clean_name.lower()} tool with accurate results."

    return json.dumps(schema, indent=2)

def add_final_schema():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Final remaining tools that need schema based on Loop 2 observations
    final_schema_tools = [
        'linear-equation-solver', 'neumorphism-generator', 'mixed-fraction-calculator',
        'molarity-calculator', 'kmh-mph-converter', 'inflation-calculator'
    ]

    fixes_made = 0

    for tool_name in final_schema_tools:
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
            schema_json = generate_final_tool_schema(tool_name)

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
                print(f"✅ {tool_name}: Added final schema markup")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added final schema markup to {fixes_made} tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_final_schema()