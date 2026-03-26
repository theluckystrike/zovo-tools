#!/usr/bin/env python3
"""
Cycle 1: Wikipedia Link Quality Audit and Fix
Scans all 873 tool pages, identifies bad Wikipedia slugs, and fixes the worst offenders.
"""

import re
import os
import urllib.parse

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

# Mapping of bad Wikipedia slugs to correct ones
# Format: old_slug -> new_slug (real Wikipedia article titles)
WIKIPEDIA_FIXES = {
    # Auto-generated from tool slug (non-existent articles)
    'Paycheck_Calculator_California': 'Income_tax_in_the_United_States',
    'Paycheck_Estimator_Texas': 'Income_tax_in_the_United_States',
    'Pregnancy_Calculator_Ivf': 'In_vitro_fertilisation',
    'Puppy_Years_To_Human_Years': 'Aging_in_dogs',
    'Refinance_Car_Loan_Estimator': 'Refinancing',
    'Salary_Calculator_Florida': 'Income_tax_in_the_United_States',
    'Wage_Calculator_Colorado': 'Minimum_wage_in_the_United_States',
    'Wage_Calculator_Florida': 'Minimum_wage_in_the_United_States',
    'Wage_Calculator_North_Carolina': 'Minimum_wage_in_the_United_States',
    'Price_Per_Square_Foot': 'Real_estate_appraisal',
    'Rent_To_Own': 'Rent-to-own',
    'Rm_To_Usd': 'Malaysian_ringgit',
    'Sek_To_Usd': 'Swedish_krona',
    'Steps_To_Calories': 'Metabolic_equivalent_of_task',
    'Taco_Bell_Nutrition': 'Taco_Bell',
    'Tax_On_Overtime': 'Overtime',
    'Td_Exchange_Rate': 'Exchange_rate',
    'Three_Phase_Power': 'Three-phase_electric_power',
    'Usd_To_Cedis': 'Ghanaian_cedi',
    'Usd_To_Gbp': 'Pound_sterling',
    'Usd_To_Idr': 'Indonesian_rupiah',
    'Usd_To_Zar': 'South_African_rand',
    'Vinyl_Plank_Flooring': 'Vinyl_composition_tile',
    'Ip_And_Location': 'IP_address',

    # Tool terms in slugs that should be concept-only
    'Amortization_calculator': 'Amortization_(business)',
    'Mortgage_calculator': 'Mortgage_loan',
    'Graphing_calculator': 'Graphing_calculator',  # This one is actually valid!
    'Scientific_calculator': 'Scientific_calculator',  # This one is actually valid!

    # Suspicious multi-word that may not exist
    'California_State_Income_Tax': 'Taxation_in_California',

    # URL encoding fixes -- these need %20 -> _
    # (will be caught by the general encoding fix below)
}

# Additional fixes: tools where the Wikipedia link concept is wrong
TOOL_SPECIFIC_FIXES = {
    # tool_slug -> (old_wiki_url_part, new_wiki_url_part)
    'ip-and-location-finder': ('Ip_And_Location', 'IP_address'),
    'paycheck-calculator-california': ('Paycheck_Calculator_California', 'Income_tax_in_the_United_States'),
    'paycheck-estimator-texas': ('Paycheck_Estimator_Texas', 'Income_tax_in_the_United_States'),
    'pregnancy-calculator-ivf': ('Pregnancy_Calculator_Ivf', 'In_vitro_fertilisation'),
    'puppy-years-to-human-years': ('Puppy_Years_To_Human_Years', 'Aging_in_dogs'),
    'refinance-car-loan-estimator': ('Refinance_Car_Loan_Estimator', 'Refinancing'),
    'salary-calculator-florida': ('Salary_Calculator_Florida', 'Income_tax_in_the_United_States'),
    'wage-calculator-colorado': ('Wage_Calculator_Colorado', 'Minimum_wage_in_the_United_States'),
    'wage-calculator-florida': ('Wage_Calculator_Florida', 'Minimum_wage_in_the_United_States'),
    'wage-calculator-north-carolina': ('Wage_Calculator_North_Carolina', 'Minimum_wage_in_the_United_States'),
    'price-per-square-foot-calculator': ('Price_Per_Square_Foot', 'Real_estate_appraisal'),
    'rent-to-own-calculator': ('Rent_To_Own', 'Rent-to-own'),
    'rm-to-usd-converter': ('Rm_To_Usd', 'Malaysian_ringgit'),
    'sek-to-usd-converter': ('Sek_To_Usd', 'Swedish_krona'),
    'steps-to-calories-converter': ('Steps_To_Calories', 'Metabolic_equivalent_of_task'),
    'taco-bell-nutrition-calculator': ('Taco_Bell_Nutrition', 'Taco_Bell'),
    'tax-on-overtime-calculator': ('Tax_On_Overtime', 'Overtime'),
    'td-exchange-rate-converter': ('Td_Exchange_Rate', 'Exchange_rate'),
    'three-phase-power-calculator': ('Three_Phase_Power', 'Three-phase_electric_power'),
    'usd-to-cedis-converter': ('Usd_To_Cedis', 'Ghanaian_cedi'),
    'usd-to-gbp-converter': ('Usd_To_Gbp', 'Pound_sterling'),
    'usd-to-idr-converter': ('Usd_To_Idr', 'Indonesian_rupiah'),
    'usd-to-zar-converter': ('Usd_To_Zar', 'South_African_rand'),
    'vinyl-plank-flooring-calculator': ('Vinyl_Plank_Flooring', 'Vinyl_composition_tile'),
    'california-payroll-calculator': ('California_State_Income_Tax', 'Taxation_in_California'),

    # Amortization_calculator -> Amortization_(business) for loan tools
    'auto-refinance-calculator': ('Amortization_calculator', 'Amortization_(business)'),
    'heloc-calculator': ('Amortization_calculator', 'Home_equity_line_of_credit'),
    'home-equity-loan-calculator': ('Amortization_calculator', 'Home_equity_loan'),
    'land-loan-calculator': ('Amortization_calculator', 'Amortization_(business)'),
    'mortgage-payoff-calculator': ('Amortization_calculator', 'Amortization_(business)'),
    'mortgage-recast-calculator': ('Amortization_calculator', 'Mortgage_loan'),
    'motorcycle-loan-calculator': ('Amortization_calculator', 'Amortization_(business)'),

    # Mortgage_calculator -> Mortgage_loan (concept, not tool)
    'mortgage-calculator': ('Mortgage_calculator', 'Mortgage_loan'),
    'mortgage-extra-payment-calculator': ('Mortgage_calculator', 'Mortgage_loan'),
}


def scan_all_tools():
    """Scan all tool pages and collect Wikipedia link data."""
    results = []
    tool_dirs = []
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            tool_dirs.append(d)

    print(f"Scanning {len(tool_dirs)} tool pages...")

    for d in tool_dirs:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()

        wiki_links = re.findall(
            r'href="(https?://en\.wikipedia\.org/wiki/([^"]+))"',
            content
        )
        for full_url, slug in wiki_links:
            decoded = urllib.parse.unquote(slug)
            results.append({
                'tool': d,
                'full_url': full_url,
                'slug': slug,
                'decoded': decoded,
            })

    return results, tool_dirs


def analyze_issues(wiki_data):
    """Analyze Wikipedia links for quality issues."""
    issues = {
        'duplicate_words': [],
        'overly_long': [],
        'tool_terms': [],
        'encoding_issues': [],
        'auto_generated': [],
    }

    for item in wiki_data:
        decoded = item['decoded']
        slug = item['slug']
        tool = item['tool']

        words = decoded.replace('_', ' ').split()
        lower_words = [w.lower() for w in words]

        # Duplicate words
        if len(lower_words) != len(set(lower_words)):
            issues['duplicate_words'].append(item)

        # Overly long
        if len(decoded) > 40:
            issues['overly_long'].append(item)

        # Tool terms in slug
        if any(t in decoded.lower() for t in ['calculator', 'converter', 'generator', 'tool', 'checker', 'maker']):
            issues['tool_terms'].append(item)

        # Encoding issues
        if '%20' in slug:
            issues['encoding_issues'].append(item)

        # Auto-generated (tool slug title-cased)
        tool_title = tool.replace('-', ' ').title().replace(' ', '_')
        if decoded == tool_title or decoded.lower() == tool_title.lower():
            issues['auto_generated'].append(item)

    return issues


def fix_wikipedia_links(tool_dirs):
    """Apply fixes to Wikipedia links in tool pages."""
    fixed_count = 0
    fixed_tools = set()

    for tool_slug, (old_part, new_part) in TOOL_SPECIFIC_FIXES.items():
        path = os.path.join(BASE, tool_slug, 'index.html')
        if not os.path.isfile(path):
            print(f"  WARNING: {tool_slug}/index.html not found")
            continue

        with open(path, 'r') as f:
            content = f.read()

        old_url = f'https://en.wikipedia.org/wiki/{old_part}'
        new_url = f'https://en.wikipedia.org/wiki/{new_part}'

        if old_url in content:
            content = content.replace(old_url, new_url)
            with open(path, 'w') as f:
                f.write(content)
            fixed_count += 1
            fixed_tools.add(tool_slug)
            print(f"  FIXED: {tool_slug}: {old_part} -> {new_part}")
        else:
            # Try URL-encoded version
            old_encoded = f'https://en.wikipedia.org/wiki/{urllib.parse.quote(old_part, safe="()#")}'
            if old_encoded in content:
                content = content.replace(old_encoded, new_url)
                with open(path, 'w') as f:
                    f.write(content)
                fixed_count += 1
                fixed_tools.add(tool_slug)
                print(f"  FIXED (encoded): {tool_slug}: {old_part} -> {new_part}")
            else:
                print(f"  SKIP: {tool_slug}: old URL not found ({old_part})")

    return fixed_count, fixed_tools


def fix_encoding_issues(tool_dirs):
    """Fix %20 encoding in Wikipedia URLs (should be _)."""
    fixed_count = 0

    for d in tool_dirs:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()

        # Find Wikipedia URLs with %20
        pattern = r'(https?://en\.wikipedia\.org/wiki/)([^"]*%20[^"]*)'
        matches = re.findall(pattern, content)
        if matches:
            new_content = content
            for base_url, slug in matches:
                old_full = base_url + slug
                fixed_slug = slug.replace('%20', '_')
                new_full = base_url + fixed_slug
                new_content = new_content.replace(old_full, new_full)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"  FIXED encoding: {d}")

    return fixed_count


def main():
    print("=" * 70)
    print("CYCLE 1: Wikipedia Link Quality Audit")
    print("=" * 70)
    print()

    # Phase 1: Scan
    wiki_data, tool_dirs = scan_all_tools()
    print(f"\nTotal Wikipedia links found: {len(wiki_data)}")
    print(f"Unique slugs: {len(set(item['decoded'] for item in wiki_data))}")
    print(f"Tools scanned: {len(tool_dirs)}")

    # Phase 2: Analyze
    print("\n--- Issue Analysis ---")
    issues = analyze_issues(wiki_data)
    for category, items in issues.items():
        print(f"  {category}: {len(items)} links")

    # Phase 3: Fix specific bad slugs
    print("\n--- Fixing Specific Bad Wikipedia Slugs ---")
    fix_count, fixed_tools = fix_wikipedia_links(tool_dirs)
    print(f"\nFixed {fix_count} Wikipedia links across {len(fixed_tools)} tools")

    # Phase 4: Fix encoding issues
    print("\n--- Fixing URL Encoding Issues ---")
    enc_count = fix_encoding_issues(tool_dirs)
    print(f"\nFixed encoding in {enc_count} tools")

    # Phase 5: Verify
    print("\n--- Post-Fix Verification ---")
    wiki_data_post, _ = scan_all_tools()
    issues_post = analyze_issues(wiki_data_post)
    for category, items in issues_post.items():
        remaining = len(items)
        original = len(issues[category])
        print(f"  {category}: {original} -> {remaining} ({original - remaining} fixed)")

    total_fixed = fix_count + enc_count
    print(f"\n{'=' * 70}")
    print(f"CYCLE 1 COMPLETE: Fixed {total_fixed} Wikipedia link issues")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
