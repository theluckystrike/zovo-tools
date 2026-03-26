#!/usr/bin/env python3
"""
Cycle 3: Wikipedia Definition Box Quality Fix
Replaces generic "Learn more from Wikipedia" and tool-description definitions
with actual concept definitions following the pattern:
"According to Wikipedia, {concept} is {brief definition}."
"""

import re
import os

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

# Actual concept definitions for each tool
# Format: tool_slug -> (concept_name, definition, wikipedia_slug)
DEFINITIONS = {
    'paint-coverage-calculator': (
        'paint coverage',
        'the area that a given volume of paint can coat, typically measured in square feet per gallon, varying by paint type and surface texture',
        'Paint'
    ),
    'parlay-bet-calculator': (
        'a parlay',
        'a single bet that links together two or more individual wagers for a higher payout, requiring all selections to win for the bettor to collect',
        'Parlay_(gambling)'
    ),
    'pay-increase-calculator': (
        'a pay raise',
        'an increase in the amount of compensation an employee receives, often expressed as a percentage of current salary',
        'Salary'
    ),
    'pay-raise-calculator': (
        'a salary increase',
        'a periodic adjustment to an employee\'s compensation, typically based on performance reviews, cost of living, or market conditions',
        'Salary'
    ),
    'paycheck-calculator-california': (
        'California income tax',
        'a progressive state income tax with rates ranging from 1% to 13.3%, in addition to federal income tax, Social Security, and Medicare withholdings',
        'Income_tax_in_the_United_States'
    ),
    'paycheck-estimator-texas': (
        'Texas',
        'one of nine U.S. states that does not levy a personal income tax, meaning residents only pay federal income tax, Social Security, and Medicare from their paychecks',
        'Income_tax_in_the_United_States'
    ),
    'pennsylvania-salary-calculator': (
        'Pennsylvania income tax',
        'a flat-rate state income tax of 3.07%, one of the lowest in the United States, applied uniformly to all taxable income',
        'Income_tax_in_the_United_States'
    ),
    'pool-volume-calculator': (
        'pool volume calculation',
        'the process of determining the water capacity of a swimming pool using geometric formulas based on pool shape, length, width, and depth',
        'Swimming_pool'
    ),
    'pregnancy-calculator-ivf': (
        'in vitro fertilisation (IVF)',
        'a medical procedure in which an egg is fertilised by sperm outside the body, with the resulting embryo transferred to the uterus to establish a pregnancy',
        'In_vitro_fertilisation'
    ),
    'price-per-square-foot-calculator': (
        'price per square foot',
        'a standard real estate metric calculated by dividing a property\'s price by its total livable area, used to compare values across different properties',
        'Real_estate_appraisal'
    ),
    'profit-margin-calculator': (
        'profit margin',
        'a financial metric that measures the percentage of revenue remaining after costs are deducted, expressed as net income divided by revenue',
        'Profit_margin'
    ),
    'pulley-calculator': (
        'a pulley',
        'a wheel on an axle or shaft designed to support movement and change of direction of a taut cable or belt, providing mechanical advantage',
        'Pulley'
    ),
    'puppy-years-to-human-years': (
        'aging in dogs',
        'a biological process where dogs mature faster than humans early in life, with recent research suggesting a logarithmic rather than linear age conversion',
        'Aging_in_dogs'
    ),
    'rebar-calculator': (
        'rebar (reinforcing bar)',
        'a steel bar used as a tension device in reinforced concrete to strengthen and hold the concrete in compression, typically placed in a grid pattern',
        'Rebar'
    ),
    'recipe-converter': (
        'recipe scaling',
        'the process of adjusting ingredient quantities proportionally to change the number of servings a recipe produces while maintaining the correct ratios',
        'Recipe'
    ),
    'refinance-car-loan-estimator': (
        'refinancing',
        'the process of replacing an existing loan with a new one, typically to obtain a lower interest rate, reduce monthly payments, or change the loan term',
        'Refinancing'
    ),
    'rent-to-own-calculator': (
        'a rent-to-own agreement',
        'a contract that gives a tenant the option to purchase the rented property at or before the end of the lease period, with a portion of rent sometimes applied to the purchase price',
        'Rent-to-own'
    ),
    'rental-property-calculator': (
        'rental property investment',
        'the purchase of real estate to generate income through rent, evaluated using metrics like cap rate, cash-on-cash return, and net operating income',
        'Real_estate_investing'
    ),
    'rm-to-usd-converter': (
        'the Malaysian ringgit (MYR)',
        'the official currency of Malaysia, subdivided into 100 sen, with exchange rates managed under a managed float system by Bank Negara Malaysia',
        'Malaysian_ringgit'
    ),
    'roi-calculator': (
        'return on investment (ROI)',
        'a financial ratio that measures the gain or loss generated relative to the amount invested, calculated as net profit divided by cost of investment',
        'Return_on_investment'
    ),
    'salary-calculator-florida': (
        'Florida',
        'one of nine U.S. states with no personal income tax, meaning residents keep more of their gross pay compared to states with income tax',
        'Income_tax_in_the_United_States'
    ),
    'sample-size-calculator': (
        'sample size determination',
        'the process of calculating the number of observations needed in a statistical study to ensure results have a desired level of confidence and precision',
        'Sample_size_determination'
    ),
    'screen-resolution-tester': (
        'display resolution',
        'the number of distinct pixels in each dimension that can be displayed, typically quoted as width by height in pixels',
        'Display_resolution'
    ),
    'sek-to-usd-converter': (
        'the Swedish krona (SEK)',
        'the official currency of Sweden, subdivided into 100 ore, and one of the most traded currencies in the foreign exchange market',
        'Swedish_krona'
    ),
    'solar-panel-calculator': (
        'solar panels (photovoltaic modules)',
        'devices that convert sunlight into electricity using photovoltaic cells, with typical residential panels producing between 250 and 400 watts each',
        'Solar_panel'
    ),
    'sonotube-calculator': (
        'a concrete pier (sonotube)',
        'a cylindrical cardboard form used to create round concrete footings or columns, commonly used for deck posts and structural foundations',
        'Concrete'
    ),
    'sql-formatter': (
        'SQL (Structured Query Language)',
        'a domain-specific language used in programming for managing and manipulating data held in relational database management systems',
        'SQL'
    ),
    'statistical-significance-calculator': (
        'statistical significance',
        'a determination that a result from data analysis is unlikely to have occurred purely by chance, typically assessed using a p-value threshold',
        'Statistical_significance'
    ),
    'steps-to-calories-converter': (
        'the metabolic equivalent of task (MET)',
        'a physiological measure expressing the energy cost of physical activities, where walking typically burns 0.03 to 0.06 calories per step depending on body weight and pace',
        'Metabolic_equivalent_of_task'
    ),
    'stock-return-calculator': (
        'stock return',
        'the gain or loss of a stock investment over a period, including both capital appreciation and dividends, often expressed using CAGR (compound annual growth rate)',
        'Rate_of_return'
    ),
    'stud-spacing-calculator': (
        'wall stud spacing',
        'the center-to-center distance between vertical framing members in a wall, typically 16 or 24 inches in standard residential construction',
        'Wall_stud'
    ),
    'taco-bell-nutrition-calculator': (
        'Taco Bell',
        'an American chain of fast-food restaurants founded in 1962, serving a variety of Mexican-inspired foods with published nutritional information for menu items',
        'Taco_Bell'
    ),
    'tank-volume-calculator': (
        'tank volume',
        'the internal capacity of a storage vessel, calculated using geometric formulas specific to the tank shape such as cylindrical, rectangular, or spherical',
        'Storage_tank'
    ),
    'tax-on-overtime-calculator': (
        'overtime pay',
        'compensation paid to employees for hours worked beyond the standard workweek, typically at 1.5 times the regular hourly rate as mandated by the Fair Labor Standards Act',
        'Overtime'
    ),
    'td-exchange-rate-converter': (
        'foreign exchange rates',
        'the price of one currency expressed in terms of another, determined by supply and demand in the global foreign exchange market',
        'Exchange_rate'
    ),
    'texas-payroll-calculator': (
        'Texas payroll',
        'unique among most U.S. states because Texas levies no state income tax, so payroll deductions include only federal income tax, Social Security, and Medicare',
        'Income_tax_in_the_United_States'
    ),
    'three-phase-power-calculator': (
        'three-phase electric power',
        'a common type of alternating current used in power generation and distribution, where three circuit conductors carry three alternating currents of equal frequency and amplitude',
        'Three-phase_electric_power'
    ),
    'transformer-calculator': (
        'an electrical transformer',
        'a passive component that transfers electrical energy from one circuit to another through electromagnetic induction, used to increase or decrease voltage levels',
        'Transformer'
    ),
    'treadmill-calorie-calculator': (
        'calorie expenditure during exercise',
        'the energy burned during physical activity, calculated using factors including body weight, exercise intensity (measured in METs), and duration',
        'Exercise'
    ),
    'upc-label-generator': (
        'the Universal Product Code (UPC)',
        'a barcode symbology widely used for tracking trade items in stores, consisting of 12 numerical digits uniquely assigned to each trade item',
        'Universal_Product_Code'
    ),
    'ups-shipping-calculator': (
        'United Parcel Service (UPS)',
        'an American multinational shipping and supply chain management company, one of the largest package delivery companies in the world',
        'United_Parcel_Service'
    ),
    'usd-to-cedis-converter': (
        'the Ghanaian cedi (GHS)',
        'the official currency of Ghana, subdivided into 100 pesewas, named after the cedi seashell once used as currency in the region',
        'Ghanaian_cedi'
    ),
    'usd-to-gbp-converter': (
        'the British pound sterling (GBP)',
        'the official currency of the United Kingdom, the oldest currency still in use and the fourth most traded currency in the foreign exchange market',
        'Pound_sterling'
    ),
    'usd-to-idr-converter': (
        'the Indonesian rupiah (IDR)',
        'the official currency of Indonesia, issued and controlled by Bank Indonesia, with exchange rates influenced by trade balances and capital flows',
        'Indonesian_rupiah'
    ),
    'usd-to-zar-converter': (
        'the South African rand (ZAR)',
        'the official currency of South Africa, named after the Witwatersrand gold ridge, and also legal tender in Namibia, Lesotho, and Eswatini',
        'South_African_rand'
    ),
    'usps-postage-calculator': (
        'United States Postal Service (USPS)',
        'an independent agency of the executive branch of the U.S. federal government responsible for providing postal service, with rates based on weight, size, and destination',
        'United_States_Postal_Service'
    ),
    'va-salary-calculator': (
        'Virginia income tax',
        'a progressive state tax with rates from 2% to 5.75%, applied in addition to federal income tax on Virginia residents\' earnings',
        'Income_tax_in_the_United_States'
    ),
    'vinyl-plank-flooring-calculator': (
        'vinyl flooring',
        'a synthetic flooring material made from polyvinyl chloride (PVC), popular for its water resistance, durability, and ease of installation',
        'Vinyl_composition_tile'
    ),
    'wage-calculator-colorado': (
        'Colorado minimum wage',
        'set by the Colorado Department of Labor, adjusted annually for inflation, and applies to most employees in the state',
        'Minimum_wage_in_the_United_States'
    ),
    'wage-calculator-florida': (
        'Florida minimum wage',
        'mandated by the Florida Constitution, adjusted annually based on the Consumer Price Index, separate from the federal minimum wage',
        'Minimum_wage_in_the_United_States'
    ),
    'wage-calculator-north-carolina': (
        'the North Carolina minimum wage',
        'set at the federal minimum wage level, with the state\'s Wage and Hour Act governing wage payment practices',
        'Minimum_wage_in_the_United_States'
    ),
    'wcag-contrast-checker': (
        'the Web Content Accessibility Guidelines (WCAG)',
        'a set of technical standards for web accessibility published by the W3C, requiring a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text',
        'Web_Content_Accessibility_Guidelines'
    ),
    'wire-capacity-calculator': (
        'wire ampacity',
        'the maximum amount of electric current a conductor can carry continuously without exceeding its temperature rating, as defined by the National Electrical Code',
        'Ampacity'
    ),
    'wisconsin-salary-calculator': (
        'Wisconsin income tax',
        'a progressive state tax with rates ranging from 3.54% to 7.65%, applied to different income brackets in addition to federal tax',
        'Income_tax_in_the_United_States'
    ),
}


def fix_wiki_definitions():
    """Replace generic wiki-definition-box content with actual definitions."""
    fixed_count = 0

    for tool_slug, (concept, definition, wiki_slug) in DEFINITIONS.items():
        path = os.path.join(BASE, tool_slug, 'index.html')
        if not os.path.isfile(path):
            print(f'  WARNING: {tool_slug}/index.html not found')
            continue

        with open(path, 'r') as f:
            content = f.read()

        if 'wiki-definition-box' not in content:
            print(f'  SKIP: {tool_slug}: no wiki-definition-box found')
            continue

        # Build the new definition HTML
        wiki_url = f'https://en.wikipedia.org/wiki/{wiki_slug}'
        new_definition = (
            f'<p style="color:#a0a0b0;font-size:0.92rem;line-height:1.6;">'
            f'According to <a href="{wiki_url}" rel="noopener" '
            f'style="color:#00ccff;" target="_blank">Wikipedia</a>, '
            f'{concept} is {definition}.</p>'
        )

        # Find the wiki-definition-box and replace its content
        # Pattern 1: div with class
        pattern1 = r'(<div[^>]*class="wiki-definition-box"[^>]*>)(.*?)(</div>)'
        # Pattern 2: section with class
        pattern2 = r'(<section[^>]*class="wiki-definition-box"[^>]*>)(.*?)(</section>)'
        # Pattern 3: div with inline style that includes wiki-definition-box
        pattern3 = r'(<div[^>]*wiki-definition-box[^>]*>)(.*?)(</div>)'

        replaced = False
        for pattern in [pattern1, pattern2, pattern3]:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                old_content = match.group(0)
                new_box = match.group(1) + '\n' + new_definition + '\n' + match.group(3)
                content = content.replace(old_content, new_box, 1)
                replaced = True
                break

        if replaced:
            with open(path, 'w') as f:
                f.write(content)
            fixed_count += 1
            print(f'  FIXED: {tool_slug}: "{concept} is {definition[:60]}..."')
        else:
            print(f'  SKIP: {tool_slug}: could not match wiki-definition-box pattern')

    return fixed_count


def main():
    print("=" * 70)
    print("CYCLE 3: Wikipedia Definition Box Content Quality")
    print("=" * 70)
    print()

    # Count initial state
    generic_count = 0
    good_count = 0
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
            if 'wiki-definition-box' in content:
                if 'Learn more from Wikipedia' in content or 'is a free browser-based utility' in content:
                    generic_count += 1
                else:
                    good_count += 1

    print(f"Wiki-definition-boxes found: {generic_count + good_count}")
    print(f"  Good definitions: {good_count}")
    print(f"  Generic definitions: {generic_count}")
    print()

    # Apply fixes
    print("--- Applying Definition Fixes ---")
    fixed = fix_wiki_definitions()

    # Verify
    print(f"\n--- Post-Fix Verification ---")
    generic_post = 0
    good_post = 0
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
            if 'wiki-definition-box' in content:
                if 'Learn more from Wikipedia' in content or 'is a free browser-based utility' in content:
                    generic_post += 1
                else:
                    good_post += 1

    print(f"  Good definitions: {good_count} -> {good_post}")
    print(f"  Generic definitions: {generic_count} -> {generic_post}")

    print(f"\n{'=' * 70}")
    print(f"CYCLE 3 COMPLETE: Fixed {fixed} wiki-definition-box entries")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
