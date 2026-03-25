#!/usr/bin/env python3
"""
Add Meta Descriptions - Agent 2
Adds meta descriptions to tools missing them
"""

import os
import re
from pathlib import Path

def generate_meta_description(tool_name):
    """Generate appropriate meta description for tool"""

    # Tool type mapping
    if 'calculator' in tool_name:
        if 'gpa' in tool_name:
            return "Calculate your GPA instantly with our free online calculator. Enter grades and credits to get accurate results."
        elif 'loan' in tool_name:
            return "Calculate loan payments, interest rates, and amortization schedules with our free online loan calculator."
        elif 'mortgage' in tool_name:
            return "Calculate mortgage payments, rates, and affordability with our comprehensive mortgage calculator tool."
        elif 'grade' in tool_name or 'grading' in tool_name:
            return "Calculate final grades, weighted averages, and grade point calculations with our free grading calculator."
        elif 'gear' in tool_name:
            return "Calculate gear ratios for bikes, cars, and machinery with our accurate gear ratio calculator tool."
        else:
            return f"Free {tool_name.replace('-', ' ')} tool. Calculate instantly with accurate results and easy-to-use interface."

    elif 'converter' in tool_name or 'to-' in tool_name:
        return f"Convert {tool_name.replace('-', ' ').replace('to', 'to')} instantly with our free online conversion tool."

    elif 'generator' in tool_name:
        if 'logo' in tool_name:
            return "Create professional logos instantly with our free AI logo generator. No design skills required."
        elif 'gradient' in tool_name:
            return "Generate beautiful CSS gradients and color transitions with our free gradient generator tool."
        elif 'hash' in tool_name:
            return "Generate MD5, SHA1, SHA256 and other hash values from text with our secure hash generator."
        else:
            return f"Generate {tool_name.replace('-generator', '').replace('-', ' ')} instantly with our free online tool."

    elif 'maker' in tool_name:
        return f"Create {tool_name.replace('-maker', '').replace('-', ' ')} easily with our free online maker tool."

    elif 'builder' in tool_name:
        return f"Build {tool_name.replace('-builder', '').replace('-', ' ')} quickly with our intuitive builder tool."

    else:
        # Generic description
        tool_display = tool_name.replace('-', ' ').title()
        return f"Free {tool_display} tool. Easy to use, accurate results, and completely online."

def add_meta_descriptions():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Get G-N tools
    all_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    gn_tools = [d for d in all_dirs if d[0].lower() in 'ghijklmn']

    fixes_made = 0

    for tool_name in gn_tools[:20]:  # Process first 20 to not overwhelm
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

            # Generate appropriate meta description
            meta_desc = generate_meta_description(tool_name)

            # Insert meta description after title or viewport
            head_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if head_pattern.search(content):
                content = head_pattern.sub(
                    r'\1\n    <meta name="description" content="' + meta_desc + '">',
                    content
                )

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added meta description")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\n🔧 Added meta descriptions to {fixes_made} tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_meta_descriptions()