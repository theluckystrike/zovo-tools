#!/usr/bin/env python3
"""
Cycle 2: StackOverflow Link Quality Audit and Fix
Scans all tool pages for stackoverflow.com/search links,
fixes queries to be concise and concept-focused.
"""

import re
import os
import urllib.parse

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

# Words to strip from SO queries (tool-type words, not concept words)
STRIP_WORDS = {
    'calculator', 'converter', 'generator', 'tool', 'checker', 'maker',
    'online', 'free', 'best', 'simple', 'easy', 'quick',
}

# Specific query replacements for tools where auto-cleanup isn't enough
QUERY_OVERRIDES = {
    '401k-calculator': '401k contribution limits',
    'air-density-calculator': 'air density formula',
    'alabama-paycheck-calculator': 'state income tax withholding',
    'arizona-salary-calculator': 'Arizona state tax brackets',
    'arkansas-paycheck-calculator': 'state payroll tax',
    'army-fitness-calculator': 'ACFT scoring standards',
    'asphalt-calculator': 'asphalt tonnage per square foot',
    'baht-to-usd-converter': 'Thai baht exchange rate API',
    'beam-deflection-calculator': 'beam deflection formula',
    'bench-press-calculator': 'one rep max estimation',
    'bernoulli-equation-calculator': 'Bernoulli equation fluid',
    'bond-yield-calculator': 'bond yield to maturity formula',
    'bra-size-calculator': 'bra size measurement guide',
    'brick-calculator': 'bricks per square foot',
    'business-card-maker': 'CSS print media exact dimensions',
    'california-payroll-calculator': 'California payroll tax rates',
    'carpet-calculator': 'carpet square footage estimation',
    'cd-account-calculator': 'certificate of deposit interest',
    'cd-interest-calculator': 'compound interest CD formula',
    'cd-ladder-calculator': 'CD ladder strategy',
    'chf-to-usd-converter': 'Swiss franc exchange rate API',
    'chipotle-calorie-calculator': 'Chipotle menu nutrition data',
    'chmod-calculator': 'Unix file permissions chmod',
    'circuit-breaker-size-calculator': 'circuit breaker sizing NEC',
    'colorado-payroll-calculator': 'Colorado payroll tax rates',
    'concrete-calculator-yards': 'concrete cubic yards formula',
    'concrete-column-calculator': 'concrete column volume',
    'concrete-slab-calculator': 'concrete slab thickness',
    'concrete-yard-calculator': 'concrete volume cubic yards',
    'creatinine-clearance-calculator': 'Cockcroft-Gault equation',
    'cron-expression-generator': 'cron expression syntax',
    'cross-stitch-calculator': 'cross stitch fabric count',
    'crypto-profit-calculator': 'crypto portfolio profit loss',
    'css-gradient-generator': 'CSS linear gradient syntax',
    'currency-converter': 'exchange rate API',
    'date-difference-calculator': 'date difference days JavaScript',
    'deck-board-calculator': 'deck board spacing layout',
    'dilution-calculator': 'dilution equation C1V1',
    'docker-compose-generator': 'docker compose YAML syntax',
    'dog-food-calculator': 'dog daily calorie requirements',
    'dosage-calculator': 'medication dosage weight based',
    'drywall-calculator': 'drywall sheets per room',
    'drywall-mud-calculator': 'drywall joint compound coverage',
    'electricity-bill-calculator': 'kWh electricity cost',
    'electricity-cost-calculator': 'electricity rate per kWh',
    'enthalpy-calculator': 'enthalpy change formula',
    'euro-to-dollar-converter': 'EUR USD exchange rate API',
    'exterior-painting-cost-calculator': 'exterior paint coverage rate',
    'fedex-dimensional-weight-calculator': 'dimensional weight formula',
    'file-size-converter': 'bytes KB MB GB conversion',
    'flow-rate-calculator': 'flow rate pipe diameter',
    'food-cost-calculator': 'food cost percentage formula',
    'freight-density-calculator': 'freight class density PCF',
    'ga-salary-calculator': 'Georgia state income tax',
    'gas-pipe-sizing-calculator': 'gas pipe sizing BTU',
    'gear-tooth-calculator': 'gear module pitch formula',
    'georgia-salary-calculator': 'Georgia income tax brackets',
    'git-command-generator': 'git common commands reference',
    'glomerular-filtration-rate-calculator': 'GFR CKD-EPI equation',
    'h1b-wage-level-calculator': 'H1B prevailing wage levels',
    'heat-loss-calculator': 'heat loss U-value formula',
    'heat-pump-sizing-calculator': 'heat pump BTU sizing',
    'heloc-payment-calculator': 'HELOC interest only payment',
    'heloc-repayment-calculator': 'HELOC repayment amortization',
    'hemoglobin-a1c-calculator': 'HbA1c blood glucose correlation',
    'hkd-to-usd-converter': 'HKD USD exchange rate API',
    'house-payoff-calculator': 'mortgage payoff amortization',
    'hvac-duct-calculator': 'HVAC duct sizing CFM',
    'indiana-payroll-calculator': 'Indiana state tax withholding',
    'infant-tylenol-dosage-calculator': 'infant acetaminophen dosage weight',
    'interest-rate-calculator': 'compound interest formula',
    'invoice-generator': 'HTML invoice template print',
    'ip-port-checker': 'TCP port connectivity check',
    'iv-drip-rate-calculator': 'IV drip rate drops per minute',
    'iv-infusion-rate-calculator': 'IV infusion rate mL per hour',
    'kansas-paycheck-calculator': 'Kansas state income tax',
    'kentucky-paycheck-calculator': 'Kentucky income tax withholding',
    'kr-to-usd-converter': 'Korean won exchange rate API',
    'lean-body-mass-calculator': 'lean body mass formula',
    'lending-calculator': 'loan amortization formula',
    'louisiana-paycheck-calculator': 'Louisiana state income tax',
    'lux-to-lumens-converter': 'lux lumens conversion formula',
    'macroeconomics-calculator': 'GDP multiplier formula',
    'maryland-payroll-calculator': 'Maryland payroll tax rates',
    'mean-bp-calculator': 'mean arterial pressure formula',
    'menstruation-period-calculator': 'menstrual cycle length prediction',
    'michigan-salary-calculator': 'Michigan income tax rate',
    'mile-to-kilometer-converter': 'miles to kilometers conversion',
    'minnesota-payroll-calculator': 'Minnesota income tax brackets',
    'molality-calculator': 'molality formula chemistry',
    'molecular-concentration-calculator': 'molarity concentration formula',
    'naira-to-usd-converter': 'Nigerian naira exchange rate',
    'nasm-calorie-calculator': 'NASM calorie estimation TDEE',
    'net-worth-calculator': 'net worth assets liabilities',
    'nevada-paycheck-calculator': 'Nevada payroll deductions',
    'new-jersey-payroll-calculator': 'NJ payroll tax rates',
    'new-jersey-salary-calculator': 'New Jersey income tax brackets',
    'new-york-paycheck-calculator': 'New York state tax withholding',
    'north-carolina-salary-calculator': 'NC income tax flat rate',
    'oklahoma-paycheck-calculator': 'Oklahoma income tax brackets',
    'oregon-salary-calculator': 'Oregon income tax brackets',
    'paint-coverage-calculator': 'paint coverage square feet gallon',
    'parlay-bet-calculator': 'parlay odds payout formula',
    'pay-increase-calculator': 'percentage pay raise formula',
    'pay-raise-calculator': 'salary increase percentage',
    'paycheck-calculator-california': 'California income tax withholding',
    'payroll-calculator': 'federal income tax brackets',
    'pennsylvania-salary-calculator': 'Pennsylvania flat income tax',
    'pool-pump-size-calculator': 'pool pump GPM sizing',
    'pool-pump-sizing-calculator': 'pool pump flow rate',
    'pool-volume-calculator': 'pool volume gallons formula',
    'pregnancy-calculator-ivf': 'IVF due date estimation',
    'price-per-square-foot-calculator': 'price per square foot real estate',
    'profit-margin-calculator': 'profit margin formula',
    'pulley-calculator': 'pulley ratio speed torque',
    'rafter-length-calculator': 'rafter length pitch calculation',
    'rafter-span-calculator': 'rafter span load tables',
    'rebar-calculator': 'rebar spacing concrete slab',
    'receipt-generator': 'JavaScript dynamic table rows',
    'recipe-converter': 'recipe scaling ratios',
    'rent-to-own-calculator': 'rent to own agreement terms',
    'rental-property-calculator': 'rental property ROI cap rate',
    'reynolds-number-calculator': 'Reynolds number formula',
    'rm-to-usd-converter': 'Malaysian ringgit exchange rate',
    'roi-calculator': 'return on investment formula',
    'rouble-to-usd-converter': 'Russian ruble exchange rate',
    'salary-calculator-florida': 'Florida no income tax payroll',
    'sample-size-calculator': 'sample size confidence interval',
    'sek-to-usd-converter': 'Swedish krona exchange rate',
    'solar-panel-calculator': 'solar panel wattage estimation',
    'sonotube-calculator': 'concrete pier volume formula',
    'south-carolina-paycheck-calculator': 'SC income tax withholding',
    'spring-rate-calculator': 'spring constant Hooke law',
    'statistical-significance-calculator': 'p-value statistical significance',
    'steps-to-calories-converter': 'steps calories MET formula',
    'stock-return-calculator': 'stock return CAGR formula',
    'stud-spacing-calculator': 'wall stud spacing layout',
    'student-loan-calculator': 'student loan amortization',
    'taco-bell-nutrition-calculator': 'Taco Bell menu nutrition data',
    'tank-volume-calculator': 'tank volume geometry formula',
    'tax-on-overtime-calculator': 'overtime pay tax withholding',
    'td-exchange-rate-converter': 'foreign exchange rate API',
    'texas-payroll-calculator': 'Texas no income tax payroll',
    'three-phase-power-calculator': 'three phase power formula',
    'transformer-calculator': 'transformer turns ratio formula',
    'treadmill-calorie-calculator': 'treadmill MET calorie burn',
    'upc-label-generator': 'UPC barcode encoding',
    'ups-shipping-calculator': 'UPS shipping rate estimation',
    'usd-to-aud-converter': 'USD AUD exchange rate API',
    'usd-to-cedis-converter': 'Ghanaian cedi exchange rate',
    'usd-to-egp-converter': 'Egyptian pound exchange rate',
    'usd-to-gbp-converter': 'USD GBP exchange rate API',
    'usd-to-idr-converter': 'Indonesian rupiah exchange rate',
    'usd-to-npr-converter': 'Nepalese rupee exchange rate',
    'usd-to-won-converter': 'Korean won exchange rate',
    'usd-to-zar-converter': 'South African rand exchange rate',
    'usps-postage-calculator': 'USPS postage rates API',
    'utah-paycheck-calculator': 'Utah income tax flat rate',
    'va-salary-calculator': 'Virginia income tax brackets',
    'vinyl-plank-flooring-calculator': 'vinyl plank flooring coverage',
    'wage-calculator-colorado': 'Colorado minimum wage rate',
    'wage-calculator-florida': 'Florida minimum wage rate',
    'wage-calculator-north-carolina': 'NC minimum wage rate',
    'wcag-contrast-checker': 'WCAG contrast ratio requirements',
    'western-union-fee-calculator': 'Western Union transfer fees',
    'wire-capacity-calculator': 'wire ampacity NEC table',
    'wire-gauge-calculator': 'AWG wire gauge ampacity',
    'wisconsin-salary-calculator': 'Wisconsin income tax brackets',
    # Non tool-term but can be improved
    'articles': 'web development articles',
    'ascii-table': 'ASCII character codes table',
}


def scan_so_links():
    """Scan all tool pages for StackOverflow search links."""
    results = []
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
            so_links = re.findall(
                r'href="(https?://stackoverflow\.com/search\?q=([^"]+))"',
                content
            )
            for full_url, query in so_links:
                decoded = urllib.parse.unquote_plus(query)
                results.append({
                    'tool': d,
                    'full_url': full_url,
                    'query': query,
                    'decoded': decoded,
                })
    return results


def fix_so_links():
    """Apply fixes to StackOverflow search queries."""
    fixed_count = 0

    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if not os.path.isfile(path):
            continue

        with open(path, 'r') as f:
            content = f.read()

        if 'stackoverflow.com/search' not in content:
            continue

        new_content = content

        if d in QUERY_OVERRIDES:
            new_query = QUERY_OVERRIDES[d]
            encoded_query = urllib.parse.quote_plus(new_query)

            # Find and replace all SO search URLs for this tool
            so_pattern = r'(https?://stackoverflow\.com/search\?q=)[^"]*'

            def replace_query(match):
                return match.group(1) + encoded_query

            new_content = re.sub(so_pattern, replace_query, new_content)
        else:
            # Auto-cleanup: strip tool terms from queries
            so_matches = re.findall(
                r'(https?://stackoverflow\.com/search\?q=)([^"]+)',
                content
            )
            for prefix, query in so_matches:
                decoded = urllib.parse.unquote_plus(query)
                words = decoded.split()
                cleaned = [w for w in words if w.lower() not in STRIP_WORDS]
                if cleaned != words and cleaned:
                    new_query = ' '.join(cleaned)
                    encoded = urllib.parse.quote_plus(new_query)
                    old_url = prefix + query
                    new_url = prefix + encoded
                    new_content = new_content.replace(old_url, new_url)

        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            fixed_count += 1

            # Show what changed
            old_queries = re.findall(r'stackoverflow\.com/search\?q=([^"]+)', content)
            new_queries = re.findall(r'stackoverflow\.com/search\?q=([^"]+)', new_content)
            old_decoded = [urllib.parse.unquote_plus(q) for q in old_queries]
            new_decoded = [urllib.parse.unquote_plus(q) for q in new_queries]
            if old_decoded != new_decoded:
                print(f'  FIXED: {d}')
                for old, new in zip(old_decoded, new_decoded):
                    if old != new:
                        print(f'    "{old}" -> "{new}"')

    return fixed_count


def main():
    print("=" * 70)
    print("CYCLE 2: StackOverflow Link Quality Audit")
    print("=" * 70)
    print()

    # Phase 1: Scan
    so_data = scan_so_links()
    print(f"Total SO links found: {len(so_data)}")
    print(f"Unique queries: {len(set(item['decoded'] for item in so_data))}")

    # Phase 2: Analyze issues
    print("\n--- Issue Analysis ---")
    tool_term_count = 0
    long_count = 0
    for item in so_data:
        decoded = item['decoded']
        words = decoded.split()
        if any(t in decoded.lower() for t in STRIP_WORDS):
            tool_term_count += 1
        if len(words) > 5:
            long_count += 1
    print(f"  Queries with tool terms: {tool_term_count}")
    print(f"  Overly long queries: {long_count}")

    # Phase 3: Fix
    print("\n--- Applying Fixes ---")
    fixed = fix_so_links()

    # Phase 4: Verify
    print(f"\n--- Post-Fix Verification ---")
    so_data_post = scan_so_links()
    tool_term_post = sum(1 for item in so_data_post
                         if any(t in item['decoded'].lower() for t in STRIP_WORDS))
    long_post = sum(1 for item in so_data_post if len(item['decoded'].split()) > 5)
    print(f"  Tool term queries: {tool_term_count} -> {tool_term_post}")
    print(f"  Overly long queries: {long_count} -> {long_post}")

    print(f"\n{'=' * 70}")
    print(f"CYCLE 2 COMPLETE: Fixed {fixed} StackOverflow search queries")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
