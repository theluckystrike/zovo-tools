#!/usr/bin/env python3
"""
Add Schema Markup to H-K Tools - Agent 2
Adds JSON-LD schema markup to remaining H-K tools
"""

import os
import re
import json
from pathlib import Path

def generate_tool_schema(tool_name):
    """Generate schema markup for specific tool types"""

    # Clean tool name for display
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

    # Add specific descriptions and categories
    if tool_name == 'hash-generator':
        schema["description"] = "Generate MD5, SHA1, SHA256 hash values from text instantly. Free secure hash generator tool."
        schema["applicationSubCategory"] = "Security"
    elif tool_name == 'html-encoder':
        schema["description"] = "Encode and decode HTML entities, special characters, and HTML tags safely online."
        schema["applicationSubCategory"] = "Developer Tools"
    elif tool_name == 'http-header-analyzer':
        schema["description"] = "Analyze HTTP response headers, security headers, and server information for any website."
        schema["applicationSubCategory"] = "Network Tools"
    elif tool_name == 'image-converter':
        schema["description"] = "Convert images between JPG, PNG, WebP, and other formats online. Free image conversion tool."
        schema["applicationSubCategory"] = "Image Processing"
    elif tool_name == 'json-formatter':
        schema["description"] = "Format, validate, and beautify JSON data with syntax highlighting. Free JSON formatter tool."
        schema["applicationSubCategory"] = "Developer Tools"
    elif tool_name == 'jwt-decoder':
        schema["description"] = "Decode and verify JWT tokens. View header, payload, and signature information securely."
        schema["applicationSubCategory"] = "Security"
    elif tool_name == 'kanban-board':
        schema["description"] = "Create Kanban boards for project management. Organize tasks with drag-and-drop interface."
        schema["applicationSubCategory"] = "Productivity"
    else:
        schema["description"] = f"Free online {clean_name.lower()} tool. Easy to use and accurate results."

        # Set category based on tool type
        if 'calculator' in tool_name:
            schema["applicationSubCategory"] = "Calculator"
        elif 'converter' in tool_name or 'to-' in tool_name:
            schema["applicationSubCategory"] = "Converter"
        elif 'generator' in tool_name:
            schema["applicationSubCategory"] = "Generator"
        elif 'builder' in tool_name or 'maker' in tool_name:
            schema["applicationSubCategory"] = "Creator"

    return json.dumps(schema, indent=2)

def add_schema_h_k_tools():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # H-K tools that likely need schema markup
    priority_tools = [
        'hash-generator', 'html-encoder', 'http-header-analyzer', 'http-status-checker',
        'image-converter', 'image-cropper', 'image-to-base64', 'json-formatter',
        'json-path-finder', 'json-to-csv-converter', 'json-viewer',
        'json-yaml-converter', 'jwt-decoder', 'kanban-board', 'keto-calculator'
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
            schema_json = generate_tool_schema(tool_name)

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
                print(f"✅ {tool_name}: Added enhanced schema markup")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added enhanced schema markup to {fixes_made} H-K tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_schema_h_k_tools()