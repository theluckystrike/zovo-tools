#!/usr/bin/env python3
"""
Add L-M Meta Descriptions - Agent 2
Adds meta descriptions to L and M tools missing them
"""

import os
import re
from pathlib import Path

def generate_l_m_meta_description(tool_name):
    """Generate meta descriptions for L and M tools"""

    # L tools
    if tool_name == 'land-loan-calculator':
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
    elif tool_name == 'math-solver':
        return "Solve math problems including algebra, geometry, and calculus with detailed solutions."
    elif tool_name == 'mathematics-solver':
        return "Advanced mathematics problem solver for algebra, calculus, and higher math concepts."
    elif tool_name == 'median-calculator':
        return "Calculate median, mode, and other statistical measures from number datasets."
    elif tool_name == 'meeting-cost-calculator':
        return "Calculate the cost of meetings based on attendee salaries and meeting duration."
    elif tool_name == 'meme-generator':
        return "Create custom memes with text overlay on popular meme templates. Free meme maker tool."
    elif tool_name == 'menstruation-period-calculator':
        return "Track menstrual cycles and predict next period dates. Women's health cycle calculator."
    elif tool_name == 'meta-tag-generator':
        return "Generate HTML meta tags for SEO optimization. Create title, description, and social tags."
    elif tool_name == 'metronome':
        return "Online metronome for musicians. Adjustable tempo, time signatures, and beat patterns."
    elif tool_name == 'mile-to-kilometer-converter':
        return "Convert miles to kilometers and km to miles instantly. Free distance conversion tool."
    elif tool_name == 'mind-map-maker':
        return "Create mind maps and visual diagrams for brainstorming and project planning online."
    elif tool_name == 'mind-map-tool':
        return "Build interactive mind maps with nodes, connections, and visual organization features."
    elif tool_name == 'mla-citation-generator':
        return "Generate MLA format citations for books, websites, and academic sources automatically."
    elif tool_name == 'mobile-home-loan-calculator':
        return "Calculate mobile home loan payments, rates, and financing options for manufactured homes."
    elif tool_name == 'molality-calculator':
        return "Calculate molality concentration from moles of solute and kilograms of solvent."
    elif tool_name == 'molar-mass-calculator':
        return "Calculate molar mass from chemical formulas. Chemistry molecular weight calculator."

    # Generic fallback
    else:
        tool_display = tool_name.replace('-', ' ').title()
        return f"Free {tool_display} tool. Easy to use, accurate results, and completely online."

def add_l_m_meta_descriptions():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # L and M tools for meta descriptions
    priority_tools = [
        'land-loan-calculator', 'lease-calculator', 'led-resistor-calculator',
        'linear-equation-solver', 'loan-payoff-calculator', 'loan-simulator',
        'lorem-ipsum-generator', 'lux-to-lumens-converter',
        'madlib-generator', 'marathon-pace-chart', 'margin-calculator',
        'markdown-editor', 'markdown-table-generator', 'math-solver',
        'mathematics-solver', 'median-calculator', 'meeting-cost-calculator',
        'meme-generator', 'menstruation-period-calculator', 'meta-tag-generator',
        'metronome', 'mile-to-kilometer-converter', 'mind-map-maker',
        'mind-map-tool', 'mla-citation-generator', 'mobile-home-loan-calculator',
        'molality-calculator'
    ]

    fixes_made = 0

    for tool_name in priority_tools[:20]:  # Process 20 tools
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
            meta_desc = generate_l_m_meta_description(tool_name)

            # Insert meta description after title
            title_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if title_pattern.search(content):
                content = title_pattern.sub(
                    r'\\1\\n    <meta name="description" content="' + meta_desc + '">',
                    content
                )

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added L/M meta description")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added meta descriptions to {fixes_made} L/M tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_l_m_meta_descriptions()