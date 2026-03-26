#!/usr/bin/env python3
"""
Cycle 3b: Fix comment-based wiki-definition-box sections
These use <!-- wiki-definition-box --> comments instead of class attributes.
"""

import re
import os

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

# Definitions for tools with comment-based wiki-definition-box
DEFINITIONS = {
    'sek-to-usd-converter': (
        'the Swedish krona (SEK)',
        'the official currency of Sweden, subdivided into 100 ore, and one of the most traded currencies in the foreign exchange market',
        'Swedish_krona',
    ),
    'solar-panel-calculator': (
        'solar panels (photovoltaic modules)',
        'devices that convert sunlight into electricity using photovoltaic cells, with typical residential panels producing between 250 and 400 watts each',
        'Solar_panel',
    ),
    'sonotube-calculator': (
        'a concrete pier (sonotube)',
        'a cylindrical cardboard form used to create round concrete footings or columns, commonly used for deck posts and structural foundations',
        'Concrete',
    ),
    'sql-formatter': (
        'SQL (Structured Query Language)',
        'a domain-specific language used in programming for managing and manipulating data held in relational database management systems',
        'SQL',
    ),
    'statistical-significance-calculator': (
        'statistical significance',
        'a determination that a result from data analysis is unlikely to have occurred purely by chance, typically assessed using a p-value threshold',
        'Statistical_significance',
    ),
    'steps-to-calories-converter': (
        'the metabolic equivalent of task (MET)',
        'a physiological measure expressing the energy cost of physical activities, where walking typically burns 0.03 to 0.06 calories per step depending on body weight and pace',
        'Metabolic_equivalent_of_task',
    ),
    'stock-return-calculator': (
        'stock return',
        'the gain or loss of a stock investment over a period, including both capital appreciation and dividends, often expressed using CAGR (compound annual growth rate)',
        'Rate_of_return',
    ),
    'stud-spacing-calculator': (
        'wall stud spacing',
        'the center-to-center distance between vertical framing members in a wall, typically 16 or 24 inches in standard residential construction',
        'Wall_stud',
    ),
    'taco-bell-nutrition-calculator': (
        'Taco Bell',
        'an American chain of fast-food restaurants founded in 1962, serving a variety of Mexican-inspired foods with published nutritional information for menu items',
        'Taco_Bell',
    ),
    'tank-volume-calculator': (
        'tank volume',
        'the internal capacity of a storage vessel, calculated using geometric formulas specific to the tank shape such as cylindrical, rectangular, or spherical',
        'Storage_tank',
    ),
    'tax-on-overtime-calculator': (
        'overtime pay',
        'compensation paid to employees for hours worked beyond the standard workweek, typically at 1.5 times the regular hourly rate as mandated by the Fair Labor Standards Act',
        'Overtime',
    ),
    'td-exchange-rate-converter': (
        'foreign exchange rates',
        'the price of one currency expressed in terms of another, determined by supply and demand in the global foreign exchange market',
        'Exchange_rate',
    ),
    'texas-payroll-calculator': (
        'Texas payroll',
        'unique among most U.S. states because Texas levies no state income tax, so payroll deductions include only federal income tax, Social Security, and Medicare',
        'Income_tax_in_the_United_States',
    ),
    'three-phase-power-calculator': (
        'three-phase electric power',
        'a common type of alternating current used in power generation and distribution, where three circuit conductors carry three alternating currents of equal frequency and amplitude',
        'Three-phase_electric_power',
    ),
    'transformer-calculator': (
        'an electrical transformer',
        'a passive component that transfers electrical energy from one circuit to another through electromagnetic induction, used to increase or decrease voltage levels',
        'Transformer',
    ),
    'treadmill-calorie-calculator': (
        'calorie expenditure during exercise',
        'the energy burned during physical activity, calculated using factors including body weight, exercise intensity (measured in METs), and duration',
        'Exercise',
    ),
    'upc-label-generator': (
        'the Universal Product Code (UPC)',
        'a barcode symbology widely used for tracking trade items in stores, consisting of 12 numerical digits uniquely assigned to each trade item',
        'Universal_Product_Code',
    ),
    'ups-shipping-calculator': (
        'United Parcel Service (UPS)',
        'an American multinational shipping and supply chain management company, one of the largest package delivery companies in the world',
        'United_Parcel_Service',
    ),
    'usd-to-cedis-converter': (
        'the Ghanaian cedi (GHS)',
        'the official currency of Ghana, subdivided into 100 pesewas, named after the cedi seashell once used as currency in the region',
        'Ghanaian_cedi',
    ),
    'usd-to-gbp-converter': (
        'the British pound sterling (GBP)',
        'the official currency of the United Kingdom, the oldest currency still in use and the fourth most traded currency in the foreign exchange market',
        'Pound_sterling',
    ),
    'usd-to-idr-converter': (
        'the Indonesian rupiah (IDR)',
        'the official currency of Indonesia, issued and controlled by Bank Indonesia, with exchange rates influenced by trade balances and capital flows',
        'Indonesian_rupiah',
    ),
    'usd-to-zar-converter': (
        'the South African rand (ZAR)',
        'the official currency of South Africa, named after the Witwatersrand gold ridge, and also legal tender in Namibia, Lesotho, and Eswatini',
        'South_African_rand',
    ),
    'usps-postage-calculator': (
        'United States Postal Service (USPS)',
        'an independent agency of the executive branch of the U.S. federal government responsible for providing postal service, with rates based on weight, size, and destination',
        'United_States_Postal_Service',
    ),
    'va-salary-calculator': (
        'Virginia income tax',
        'a progressive state tax with rates from 2% to 5.75%, applied in addition to federal income tax on Virginia residents\' earnings',
        'Income_tax_in_the_United_States',
    ),
    'vinyl-plank-flooring-calculator': (
        'vinyl flooring',
        'a synthetic flooring material made from polyvinyl chloride (PVC), popular for its water resistance, durability, and ease of installation',
        'Vinyl_composition_tile',
    ),
    'wage-calculator-colorado': (
        'Colorado minimum wage',
        'set by the Colorado Department of Labor, adjusted annually for inflation, and applies to most employees in the state',
        'Minimum_wage_in_the_United_States',
    ),
    'wage-calculator-florida': (
        'Florida minimum wage',
        'mandated by the Florida Constitution, adjusted annually based on the Consumer Price Index, separate from the federal minimum wage',
        'Minimum_wage_in_the_United_States',
    ),
    'wage-calculator-north-carolina': (
        'the North Carolina minimum wage',
        'set at the federal minimum wage level, with the state\'s Wage and Hour Act governing wage payment practices',
        'Minimum_wage_in_the_United_States',
    ),
    'wcag-contrast-checker': (
        'the Web Content Accessibility Guidelines (WCAG)',
        'a set of technical standards for web accessibility published by the W3C, requiring a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text',
        'Web_Content_Accessibility_Guidelines',
    ),
    'wire-capacity-calculator': (
        'wire ampacity',
        'the maximum amount of electric current a conductor can carry continuously without exceeding its temperature rating, as defined by the National Electrical Code',
        'Ampacity',
    ),
    'wisconsin-salary-calculator': (
        'Wisconsin income tax',
        'a progressive state tax with rates ranging from 3.54% to 7.65%, applied to different income brackets in addition to federal tax',
        'Income_tax_in_the_United_States',
    ),
}


def fix_comment_wiki_defs():
    """Fix comment-based wiki-definition-box sections."""
    fixed = 0

    for tool_slug, (concept, definition, wiki_slug) in DEFINITIONS.items():
        path = os.path.join(BASE, tool_slug, 'index.html')
        if not os.path.isfile(path):
            print(f'  WARNING: {tool_slug}/index.html not found')
            continue

        with open(path, 'r') as f:
            content = f.read()

        if '<!-- wiki-definition-box -->' not in content:
            print(f'  SKIP: {tool_slug}: no comment-based wiki-definition-box')
            continue

        wiki_url = f'https://en.wikipedia.org/wiki/{wiki_slug}'

        # Match the entire comment-based wiki-definition-box block
        # Pattern: <!-- wiki-definition-box -->\n<div ...>...\n</div>
        pattern = (
            r'(<!-- wiki-definition-box -->)\s*'
            r'<div[^>]*>'
            r'.*?'
            r'</div>'
        )

        new_block = (
            f'<!-- wiki-definition-box -->\n'
            f'<div style="margin:2rem 0;padding:1.5rem;background:#12121a;border:1px solid #1e1e2a;border-radius:8px;border-left:4px solid #00ccff;">\n'
            f'<h3 style="color:#e0e0e8;margin-top:0;">Definition</h3>\n'
            f'<p style="color:#a0a0b0;font-size:0.92rem;line-height:1.6;">According to '
            f'<a href="{wiki_url}" rel="noopener" style="color:#00ccff;" target="_blank">Wikipedia</a>, '
            f'{concept} is {definition}.</p>\n'
            f'<p style="font-size:0.8rem;color:#666;margin:0;">Source: '
            f'<a href="{wiki_url}" rel="noopener" style="color:#00ccff;" target="_blank">Wikipedia</a></p>\n'
            f'</div>'
        )

        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_block + content[match.end():]
            with open(path, 'w') as f:
                f.write(content)
            fixed += 1
            print(f'  FIXED: {tool_slug}: {concept}')
        else:
            print(f'  FAIL: {tool_slug}: pattern not matched')

    return fixed


def main():
    print("=" * 70)
    print("CYCLE 3b: Fix Comment-Based Wiki Definition Boxes")
    print("=" * 70)
    print()

    fixed = fix_comment_wiki_defs()

    # Verify remaining generic definitions
    generic_remaining = 0
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            with open(path) as f:
                content = f.read()
            if 'wiki-definition-box' in content:
                if 'Learn more from Wikipedia' in content or 'is a free browser-based utility' in content:
                    generic_remaining += 1
                    print(f'  STILL GENERIC: {d}')

    print(f"\n{'=' * 70}")
    print(f"CYCLE 3b COMPLETE: Fixed {fixed} comment-based definitions")
    print(f"Remaining generic: {generic_remaining}")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
