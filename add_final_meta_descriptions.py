#!/usr/bin/env python3
"""
Add Final Meta Descriptions - Agent 2
Adds meta descriptions to remaining tools missing them based on Loop 2 observations
"""

import os
import re
from pathlib import Path

def generate_final_meta_description(tool_name):
    """Generate meta descriptions for remaining tools"""

    # Specific descriptions for remaining tools
    descriptions = {
        'kmh-mph-converter': "Convert between KMH and MPH speed units bidirectionally. Free speed converter tool.",
        'loan-amortization-calculator': "Calculate loan amortization schedules with payment breakdowns and interest tracking.",
        'loan-calculator': "Calculate monthly loan payments with interest rates, terms, and total cost analysis.",
        'html-to-markdown': "Convert HTML to Markdown format preserving structure and formatting for documentation.",
        'ideal-body-weight-calculator': "Calculate ideal body weight using multiple formulas (Hamwi, Devine, Robinson).",
        'ideal-gas-law-calculator': "Calculate pressure, volume, temperature using the ideal gas law PV=nRT formula.",
        'ieee-citation-generator': "Generate IEEE format citations for academic papers, journals, and technical sources.",
        'image-compressor': "Compress images to reduce file size while maintaining quality. Free image compression tool.",
        'image-to-text-converter': "Extract text from images using OCR technology. Convert JPG, PNG to editable text.",
        'image-upscaler': "Upscale images to higher resolution using AI enhancement. Improve image quality online.",
        'inductance-calculator': "Calculate inductance values for coils, solenoids, and electrical circuits.",
        'instagram-font-generator': "Generate stylish fonts and text for Instagram bio, posts, and stories.",
        'interest-rate-calculator': "Calculate compound interest, simple interest, and investment growth over time.",
        'ip-lookup': "Lookup IP address information including location, ISP, and network details.",
        'jacobian-calculator': "Calculate Jacobian matrix and determinant for multivariable calculus functions.",
        'js-minifier': "Minify JavaScript code to reduce file size and improve website loading speed.",
        'json-to-xml-converter': "Convert JSON data to XML format with customizable structure and attributes.",
        'jwt-decoder': "Decode JWT tokens and view header, payload, and signature information securely.",
        'kelvin-to-celsius': "Convert Kelvin to Celsius temperature scale instantly. Free temperature converter."
    }

    if tool_name in descriptions:
        return descriptions[tool_name]
    else:
        # Generic fallback
        tool_display = tool_name.replace('-', ' ').title()
        return f"Free {tool_display} tool. Easy to use, accurate results, and completely online."

def add_final_meta_descriptions():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Tools that still need meta descriptions based on Loop 2 observations
    remaining_meta_tools = [
        'kmh-mph-converter', 'loan-amortization-calculator', 'loan-calculator',
        'html-to-markdown', 'ideal-body-weight-calculator', 'ideal-gas-law-calculator',
        'ieee-citation-generator', 'image-compressor', 'image-to-text-converter',
        'image-upscaler', 'inductance-calculator', 'instagram-font-generator',
        'interest-rate-calculator', 'ip-lookup', 'jacobian-calculator',
        'js-minifier', 'jwt-decoder', 'kelvin-to-celsius'
    ]

    fixes_made = 0

    for tool_name in remaining_meta_tools[:15]:  # Process 15 tools
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
            meta_desc = generate_final_meta_description(tool_name)

            # Insert meta description after title
            title_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if title_pattern.search(content):
                content = title_pattern.sub(
                    r'\\1\\n    <meta name="description" content="' + meta_desc + '">',
                    content
                )

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added final meta description")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added meta descriptions to {fixes_made} final tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_final_meta_descriptions()