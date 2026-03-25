#!/usr/bin/env python3
"""
Add More Meta Descriptions - Agent 2
Adds meta descriptions to additional G-N tools missing them
"""

import os
import re
from pathlib import Path

def generate_specific_meta_description(tool_name):
    """Generate specific meta descriptions for different tool types"""

    # H tools
    if tool_name == 'hash-generator':
        return "Generate MD5, SHA1, SHA256 hash values from text instantly. Free secure hash generator tool."
    elif tool_name == 'html-encoder':
        return "Encode and decode HTML entities, special characters, and HTML tags safely online."
    elif tool_name == 'html-formatter':
        return "Format and beautify HTML code with proper indentation. Free HTML formatter and validator."
    elif tool_name == 'htpasswd-generator':
        return "Generate Apache .htpasswd files for basic authentication. Create encrypted passwords for web security."
    elif tool_name == 'http-header-analyzer':
        return "Analyze HTTP response headers, security headers, and server information for any website."
    elif tool_name == 'http-status-checker':
        return "Check HTTP status codes and response headers for any URL. Test website connectivity."

    # I tools
    elif tool_name == 'ico-converter':
        return "Convert images to ICO format for favicons and Windows icons. Supports multiple sizes."
    elif tool_name == 'icon-generator':
        return "Generate custom icons and favicons from images. Create ICO, PNG icons in multiple sizes."
    elif tool_name == 'ics-calendar-generator':
        return "Create ICS calendar files for events. Generate calendar invitations and appointments."
    elif tool_name == 'image-converter':
        return "Convert images between JPG, PNG, WebP, and other formats online. Free image conversion tool."
    elif tool_name == 'image-cropper':
        return "Crop images online with precise control. Free image cropping tool with custom dimensions."
    elif tool_name == 'image-to-base64':
        return "Convert images to Base64 encoding for embedding in HTML, CSS, or data URIs."

    # J tools
    elif tool_name == 'json-formatter':
        return "Format, validate, and beautify JSON data with syntax highlighting. Free JSON formatter tool."
    elif tool_name == 'json-path-finder':
        return "Find JSON paths and extract values from complex JSON structures. JSONPath query tool."
    elif tool_name == 'json-to-csv-converter':
        return "Convert JSON data to CSV format for spreadsheets and data analysis. Free JSON to CSV tool."
    elif tool_name == 'json-to-xml-converter':
        return "Convert JSON data to XML format with customizable structure and formatting options."
    elif tool_name == 'json-viewer':
        return "View, format, and validate JSON data with tree structure and syntax highlighting."
    elif tool_name == 'json-yaml-converter':
        return "Convert between JSON and YAML formats bidirectionally. Free data format converter."
    elif tool_name == 'jwt-decoder':
        return "Decode and verify JWT tokens. View header, payload, and signature information securely."

    # K tools
    elif tool_name == 'kanban-board':
        return "Create Kanban boards for project management. Organize tasks with drag-and-drop interface."
    elif tool_name == 'kelvin-to-celsius':
        return "Convert Kelvin to Celsius temperature instantly. Free temperature conversion calculator."
    elif tool_name == 'keto-calculator':
        return "Calculate keto macros, daily carbs, and ketogenic diet requirements for weight loss."
    elif tool_name == 'keyword-density-checker':
        return "Check keyword density and frequency in text for SEO optimization and content analysis."
    elif tool_name == 'kinetic-energy-calculator':
        return "Calculate kinetic energy from mass and velocity using physics formulas. Free KE calculator."
    elif tool_name == 'km-per-hour-to-mph':
        return "Convert kilometers per hour to miles per hour instantly. Free speed conversion tool."
    elif tool_name == 'kmh-mph-converter':
        return "Convert between KMH and MPH speed units bidirectionally. Accurate speed converter."

    # L tools
    elif tool_name == 'land-loan-calculator':
        return "Calculate land loan payments, rates, and terms for vacant land purchases and financing."
    elif tool_name == 'lease-calculator':
        return "Calculate car lease payments, terms, and total costs. Compare lease vs buy options."
    elif tool_name == 'led-resistor-calculator':
        return "Calculate resistor values for LED circuits. Determine current limiting resistors for LEDs."
    elif tool_name == 'linear-equation-solver':
        return "Solve linear equations and systems of equations step by step. Free algebra calculator."
    elif tool_name == 'loan-payoff-calculator':
        return "Calculate loan payoff time with extra payments. See interest savings and payoff schedules."
    elif tool_name == 'loan-simulator':
        return "Simulate loan scenarios with different terms, rates, and payment amounts for comparison."
    elif tool_name == 'logo-maker':
        return "Create professional logos with AI assistance. Free logo generator for businesses and brands."
    elif tool_name == 'lorem-ipsum-generator':
        return "Generate Lorem Ipsum placeholder text for design and development. Custom length options."
    elif tool_name == 'lux-to-lumens-converter':
        return "Convert lux to lumens and lumens to lux for lighting calculations and measurements."

    # M tools
    elif tool_name == 'macro-calculator':
        return "Calculate daily macronutrient requirements for fitness goals. Protein, carbs, fats calculator."
    elif tool_name == 'macroeconomics-calculator':
        return "Calculate macroeconomic indicators like GDP, inflation, and economic growth rates."
    elif tool_name == 'madlib-generator':
        return "Create funny Mad Libs stories with custom word inputs. Family-friendly word game generator."
    elif tool_name == 'marathon-pace-chart':
        return "Calculate marathon pace times and splits for race planning and training schedules."
    elif tool_name == 'margin-calculator':
        return "Calculate profit margins, markup, and pricing for business financial analysis."
    elif tool_name == 'markdown-editor':
        return "Edit Markdown text with live preview. Free online Markdown editor with syntax highlighting."
    elif tool_name == 'markdown-table-generator':
        return "Generate Markdown tables with custom rows and columns. Format tables for documentation."
    elif tool_name == 'markdown-to-html':
        return "Convert Markdown to HTML with syntax highlighting and custom styling options."
    elif tool_name == 'markdown-to-pdf':
        return "Convert Markdown files to PDF documents with formatting and styling preservation."
    elif tool_name == 'markup-calculator':
        return "Calculate markup percentage and selling price from cost and desired profit margins."
    elif tool_name == 'math-equation-solver':
        return "Solve complex mathematical equations step by step. Free algebra and calculus solver."
    elif tool_name == 'math-solver':
        return "Solve math problems including algebra, geometry, and calculus with detailed solutions."
    elif tool_name == 'mathematics-solver':
        return "Advanced mathematics problem solver for algebra, calculus, and higher math concepts."
    elif tool_name == 'matrix-calculator':
        return "Calculate matrix operations including addition, multiplication, determinant, and inverse."
    elif tool_name == 'mean-bp-calculator':
        return "Calculate mean arterial pressure (MAP) from systolic and diastolic blood pressure values."
    elif tool_name == 'median-calculator':
        return "Calculate median, mode, and other statistical measures from number datasets."
    elif tool_name == 'meeting-cost-calculator':
        return "Calculate the cost of meetings based on attendee salaries and meeting duration."
    elif tool_name == 'meme-generator':
        return "Create custom memes with text overlay on popular meme templates. Free meme maker tool."

    # N tools
    elif tool_name == 'net-worth-calculator':
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

    # Generic fallback
    else:
        tool_display = tool_name.replace('-', ' ').title()
        return f"Free {tool_display} tool. Easy to use, accurate results, and completely online."

def add_more_meta_descriptions():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Priority tools for meta descriptions (H-N range)
    priority_tools = [
        'hash-generator', 'html-encoder', 'html-formatter', 'htpasswd-generator',
        'http-header-analyzer', 'http-status-checker', 'icon-generator',
        'image-converter', 'image-cropper', 'image-to-base64',
        'json-formatter', 'json-path-finder', 'json-to-csv-converter',
        'json-viewer', 'json-yaml-converter', 'jwt-decoder',
        'kanban-board', 'kelvin-to-celsius', 'keyword-density-checker',
        'kinetic-energy-calculator', 'km-per-hour-to-mph', 'kmh-mph-converter'
    ]

    fixes_made = 0

    for tool_name in priority_tools[:15]:  # Process 15 tools
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
            meta_desc = generate_specific_meta_description(tool_name)

            # Insert meta description after title
            title_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if title_pattern.search(content):
                content = title_pattern.sub(
                    r'\\1\\n    <meta name="description" content="' + meta_desc + '">',
                    content
                )

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added specific meta description")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added meta descriptions to {fixes_made} more tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_more_meta_descriptions()