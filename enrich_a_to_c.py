#!/usr/bin/env python3
"""
Enrichment script for Zovo Tools (a-c alphabetical range).
Adds missing enrichment layers to each tool's index.html:
1. About This Tool section
2. Quick Facts section
3. Visible FAQ from JSON-LD
4. Twitter meta tags
5. Fix og:site_name from "Zovo Tools" to "Zovo"
"""

import os
import re
import json
import html

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Tool-specific fourth fact for Quick Facts
TOOL_FACTS = {
    "calculator": ("Instant", "Results"),
    "generator": ("One Click", "Generate"),
    "converter": ("Instant", "Conversion"),
    "solver": ("Smart", "Algorithm"),
    "checker": ("Real-Time", "Analysis"),
    "tester": ("Live", "Testing"),
    "builder": ("Visual", "Builder"),
    "finder": ("Smart", "Search"),
    "maker": ("Easy", "Creation"),
    "editor": ("Live", "Preview"),
    "simulator": ("Visual", "Simulation"),
    "analyzer": ("Deep", "Analysis"),
    "visualizer": ("Interactive", "Display"),
    "translator": ("Instant", "Translation"),
    "encoder": ("Fast", "Encoding"),
    "decoder": ("Fast", "Decoding"),
    "validator": ("Instant", "Validation"),
    "minifier": ("Fast", "Minification"),
    "beautifier": ("Code", "Formatting"),
    "picker": ("Visual", "Selection"),
    "remover": ("One Click", "Removal"),
    "trimmer": ("Precise", "Trimming"),
    "viewer": ("Instant", "Preview"),
    "detector": ("Smart", "Detection"),
}


def get_fourth_fact(slug):
    """Derive a tool-specific fourth fact from the slug."""
    for key, (val, label) in TOOL_FACTS.items():
        if key in slug:
            return val, label
    # Default
    return "Easy to", "Use"


def get_tool_name(slug):
    """Derive readable tool name from slug."""
    return slug.replace("-", " ").title()


def get_tool_dirs():
    """Get all tool directories starting with a-c that have index.html."""
    dirs = []
    for name in sorted(os.listdir(BASE_DIR)):
        if not name[0:1].isalpha():
            continue
        if name[0].lower() not in "abc":
            continue
        index_path = os.path.join(BASE_DIR, name, "index.html")
        if os.path.isfile(index_path):
            dirs.append(name)
    return dirs


def extract_faq_from_jsonld(content):
    """Extract FAQ Q&A pairs from FAQPage JSON-LD in the HTML."""
    faqs = []
    # Find all JSON-LD blocks
    pattern = r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>'
    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
    for match in matches:
        try:
            data = json.loads(match)
        except json.JSONDecodeError:
            continue

        # Handle single object
        if isinstance(data, dict):
            items = [data]
        elif isinstance(data, list):
            items = data
        else:
            continue

        for item in items:
            if item.get("@type") == "FAQPage":
                for entity in item.get("mainEntity", []):
                    if entity.get("@type") == "Question":
                        q = entity.get("name", "")
                        ans = entity.get("acceptedAnswer", {})
                        a = ans.get("text", "") if isinstance(ans, dict) else ""
                        if q and a:
                            faqs.append((q, a))
            # Handle @graph
            if "@graph" in item:
                for node in item["@graph"]:
                    if node.get("@type") == "FAQPage":
                        for entity in node.get("mainEntity", []):
                            if entity.get("@type") == "Question":
                                q = entity.get("name", "")
                                ans = entity.get("acceptedAnswer", {})
                                a = ans.get("text", "") if isinstance(ans, dict) else ""
                                if q and a:
                                    faqs.append((q, a))
    return faqs


def extract_title(content):
    """Extract the page title."""
    m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Remove "| Zovo" or "| Zovo Tools" suffix
        title = re.sub(r'\s*\|\s*Zovo\s*(Tools)?\s*$', '', title)
        return title
    return ""


def extract_description(content):
    """Extract meta description."""
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


def has_pattern(content, *patterns):
    """Check if content contains any of the patterns (case-insensitive)."""
    lower = content.lower()
    for p in patterns:
        if p.lower() in lower:
            return True
    return False


def add_about_section(content, slug):
    """Add About This Tool section before </body> if missing."""
    if has_pattern(content, "About This Tool", "about-this-tool"):
        return content, False

    tool_name = get_tool_name(slug)

    about_html = f'''
<!-- About This Tool -->
<div style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:'Inter',sans-serif;">
  <h2 style="color:#fff;font-size:1.3rem;margin:0 0 1rem;">About This Tool</h2>
  <p style="color:#ccc;line-height:1.7;margin-bottom:1rem;">The {tool_name} is a free browser-based utility designed to save you time and simplify everyday tasks. Whether you are a professional, student, or hobbyist, this tool provides accurate results instantly without the need for downloads, installations, or account sign-ups.</p>
  <p style="color:#ccc;line-height:1.7;margin:0;">Built by Michael Lip, this tool runs 100% client-side in your browser. No data is ever sent to any server, and nothing is stored or tracked. Your privacy is fully preserved every time you use it.</p>
</div>
'''
    content = content.replace("</body>", about_html + "\n</body>")
    return content, True


def add_quick_facts(content, slug):
    """Add Quick Facts section before </body> if missing."""
    if has_pattern(content, "Quick Facts", "quick-facts"):
        return content, False

    fourth_val, fourth_label = get_fourth_fact(slug)

    qf_html = f'''
<!-- Quick Facts -->
<div style="max-width:800px;margin:2rem auto;padding:0 1rem;">
  <p style="color:#00ff88;font-size:0.85rem;font-weight:600;margin:0 0 12px;">Quick Facts</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.5rem;font-weight:700;color:#00ff88;">100%</div>
      <div style="font-size:0.8rem;color:#aaa;">Client-Side</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.5rem;font-weight:700;color:#00ff88;">Zero</div>
      <div style="font-size:0.8rem;color:#aaa;">Data Uploaded</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.5rem;font-weight:700;color:#00ff88;">Free</div>
      <div style="font-size:0.8rem;color:#aaa;">Forever</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.5rem;font-weight:700;color:#00ff88;">{html.escape(fourth_val)}</div>
      <div style="font-size:0.8rem;color:#aaa;">{html.escape(fourth_label)}</div>
    </div>
  </div>
</div>
'''
    content = content.replace("</body>", qf_html + "\n</body>")
    return content, True


def add_visible_faq(content, slug):
    """If FAQPage JSON-LD exists but no visible FAQ section, add one."""
    # Check if visible FAQ already exists
    if has_pattern(content, "Common Questions", "Frequently Asked"):
        return content, False

    # Check if FAQPage JSON-LD exists
    if not has_pattern(content, "FAQPage"):
        return content, False

    faqs = extract_faq_from_jsonld(content)
    if not faqs:
        return content, False

    faq_items = ""
    for i, (q, a) in enumerate(faqs):
        q_escaped = html.escape(q)
        a_escaped = html.escape(a)
        faq_items += f'''
    <div style="border-bottom:1px solid #2a2a3a;">
      <button onclick="this.classList.toggle('active');var p=this.nextElementSibling;p.style.display=p.style.display==='block'?'none':'block';" style="width:100%;text-align:left;background:none;border:none;color:#e0e0e8;padding:1rem 0;font-size:0.95rem;font-weight:500;cursor:pointer;font-family:'Inter',sans-serif;display:flex;justify-content:space-between;align-items:center;">{q_escaped}<span style="color:#00ff88;font-size:1.2rem;transition:transform 0.2s;">+</span></button>
      <div style="display:none;padding:0 0 1rem;color:#aaa;line-height:1.7;font-size:0.9rem;">{a_escaped}</div>
    </div>'''

    faq_html = f'''
<!-- Frequently Asked Questions -->
<div style="max-width:800px;margin:2rem auto;padding:0 1rem;">
  <h2 style="color:#fff;font-size:1.3rem;font-weight:500;margin-bottom:1rem;" id="frequently-asked-questions">Frequently Asked Questions</h2>
  <div style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;overflow:hidden;padding:0 1.5rem;">
    {faq_items}
  </div>
</div>
'''
    content = content.replace("</body>", faq_html + "\n</body>")
    return content, True


def add_twitter_meta(content, slug):
    """Add twitter:card, twitter:title, twitter:description if missing."""
    if has_pattern(content, "twitter:card"):
        return content, False

    tool_name = get_tool_name(slug)
    title = extract_title(content) or f"Free {tool_name}"
    desc = extract_description(content) or f"Free online {tool_name.lower()}. Runs in your browser, no data uploaded."

    # Truncate desc if too long
    if len(desc) > 200:
        desc = desc[:197] + "..."

    twitter_html = f'''<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title, quote=True)}">
<meta name="twitter:description" content="{html.escape(desc, quote=True)}">
'''

    # Insert after </title> or after existing og tags or before </head>
    if "</title>" in content:
        content = content.replace("</title>", "</title>\n" + twitter_html, 1)
    elif "</head>" in content:
        content = content.replace("</head>", twitter_html + "</head>", 1)

    return content, True


def fix_og_site_name(content):
    """Fix og:site_name from 'Zovo Tools' to 'Zovo'."""
    pattern = r'(<meta\s+property="og:site_name"\s+content=")Zovo Tools(")'
    new_content, count = re.subn(pattern, r'\1Zovo\2', content, flags=re.IGNORECASE)
    return new_content, count > 0


def process_tool(slug):
    """Process a single tool's index.html, adding missing enrichment layers."""
    index_path = os.path.join(BASE_DIR, slug, "index.html")

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # 1. About This Tool
    content, changed = add_about_section(content, slug)
    if changed:
        changes.append("About This Tool")

    # 2. Quick Facts
    content, changed = add_quick_facts(content, slug)
    if changed:
        changes.append("Quick Facts")

    # 3. Visible FAQ
    content, changed = add_visible_faq(content, slug)
    if changed:
        changes.append("Visible FAQ")

    # 4. Twitter meta
    content, changed = add_twitter_meta(content, slug)
    if changed:
        changes.append("Twitter meta")

    # 5. Fix og:site_name
    content, changed = fix_og_site_name(content)
    if changed:
        changes.append("og:site_name fix")

    if content != original:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

    return changes


def main():
    tools = get_tool_dirs()
    print(f"Found {len(tools)} tools starting with a-c\n")

    total_changes = 0
    tools_modified = 0
    layer_counts = {
        "About This Tool": 0,
        "Quick Facts": 0,
        "Visible FAQ": 0,
        "Twitter meta": 0,
        "og:site_name fix": 0,
    }

    for slug in tools:
        changes = process_tool(slug)
        if changes:
            tools_modified += 1
            total_changes += len(changes)
            for c in changes:
                layer_counts[c] = layer_counts.get(c, 0) + 1
            print(f"  [UPDATED] {slug}: {', '.join(changes)}")
        else:
            print(f"  [OK]      {slug}: no changes needed")

    print(f"\n{'='*60}")
    print(f"ENRICHMENT SUMMARY")
    print(f"{'='*60}")
    print(f"Tools scanned:       {len(tools)}")
    print(f"Tools modified:      {tools_modified}")
    print(f"Total layers added:  {total_changes}")
    print(f"")
    for layer, count in layer_counts.items():
        status = f"{count} added" if count > 0 else "none needed"
        print(f"  {layer:20s} {status}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
