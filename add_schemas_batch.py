#!/usr/bin/env python3
"""Add missing JSON-LD schemas (WebApplication, FAQPage, BreadcrumbList) to tools."""

import re
import os
import json

BASE = '/Users/mike/zovo-workspaces/zovo-tools'

# Tool configs: slug -> { name, desc, category, faqs: [(q,a),...] }
TOOL_CONFIGS = {
    'acre-square-footage': {
        'name': 'Acre Square Footage Calculator',
        'category': 'Utility',
        'faqs': [
            ('How many square feet are in one acre?', 'One acre equals exactly 43,560 square feet. This is derived from the historical surveying chain measurement of 66 feet by 660 feet.'),
            ('How do I convert acres to hectares?', 'Multiply the number of acres by 0.4047 to get hectares. For example, 5 acres equals approximately 2.02 hectares.'),
            ('What does one acre look like in real life?', 'One acre is roughly 75% the size of an American football field, or about 16 tennis courts arranged together.'),
            ('Can I calculate the area of an irregular plot in acres?', 'Yes, this tool supports triangular and circular plot calculations. Enter the dimensions and it converts the result to acres automatically.'),
            ('How do I calculate cost per acre from a total land price?', 'Divide the total purchase price by the number of acres. This tool also shows cost per square foot and cost per hectare for comparison.'),
        ]
    },
    'ascii-banner-generator': {
        'name': 'ASCII Banner Generator',
        'category': 'Utility',
        'faqs': [
            ('What is an ASCII banner?', 'An ASCII banner is large text art created using standard keyboard characters. Each letter is rendered in an oversized block style using symbols like hash marks, slashes, and pipes.'),
            ('How many font styles does this ASCII banner generator support?', 'This generator includes 8 or more font styles, each rendering your text in a different ASCII art pattern. You can preview all styles instantly.'),
            ('Can I copy the ASCII banner to my clipboard?', 'Yes, click the copy button to instantly copy the generated ASCII banner text to your clipboard for pasting into code comments, READMEs, or terminal screens.'),
            ('Is this ASCII banner generator free to use?', 'Yes, this tool is completely free with no registration, no ads, and no usage limits. It runs entirely in your browser.'),
            ('What are common uses for ASCII banners?', 'ASCII banners are popular in source code headers, terminal welcome messages, README files, email signatures, and retro-style website designs.'),
        ]
    },
    'commercial-mortgage-calculator': {
        'name': 'Commercial Mortgage Calculator',
        'category': 'Finance',
        'faqs': [
            ('How is a commercial mortgage payment calculated?', 'Commercial mortgage payments are calculated using the loan amount, interest rate, and amortization period. This calculator factors in both the monthly payment and total interest over the loan term.'),
            ('What is a typical commercial mortgage interest rate?', 'Commercial mortgage rates typically range from 5% to 10% depending on the property type, borrower credit, and loan-to-value ratio. Rates vary by lender and market conditions.'),
            ('What is the difference between amortization and loan term in commercial mortgages?', 'The amortization period is the schedule over which payments are calculated, often 20-30 years. The loan term is the actual length before renewal, typically 5-10 years, often resulting in a balloon payment.'),
            ('What loan-to-value ratio do commercial lenders require?', 'Most commercial lenders require a loan-to-value ratio of 65% to 80%, meaning you need 20% to 35% as a down payment on the property.'),
            ('Can I calculate debt service coverage ratio with this tool?', 'Yes, enter your net operating income and the calculator will compute your DSCR, which lenders typically want at 1.20 or higher for loan approval.'),
        ]
    },
    'completing-the-square-calculator': {
        'name': 'Completing the Square Calculator',
        'category': 'Education',
        'faqs': [
            ('What does completing the square mean in algebra?', 'Completing the square is a technique for rewriting a quadratic expression in the form (x + p) squared + q. It helps solve quadratic equations and find the vertex of a parabola.'),
            ('When should I use completing the square instead of the quadratic formula?', 'Completing the square is preferred when you need the vertex form of a quadratic, when deriving the quadratic formula itself, or when integrating certain expressions in calculus.'),
            ('How do I complete the square for ax squared + bx + c?', 'Divide all terms by a, move the constant to the other side, add (b/2a) squared to both sides, then factor the left side as a perfect square trinomial.'),
            ('Can this calculator show step-by-step work?', 'Yes, this calculator displays each step of the completing the square process so you can follow the algebra and verify your own work.'),
            ('Does completing the square work for all quadratic equations?', 'Yes, completing the square works for every quadratic equation. It always produces the vertex form, even when the discriminant is negative, in which case the solutions involve complex numbers.'),
        ]
    },
    'cover-letter-generator': {
        'name': 'Cover Letter Generator',
        'category': 'Utility',
        'faqs': [
            ('How do I write a professional cover letter?', 'Start with a clear header, address the hiring manager by name, open with a strong hook about why you fit the role, highlight 2-3 relevant achievements, and close with a confident call to action.'),
            ('How long should a cover letter be?', 'A cover letter should be 250-400 words, fitting on a single page. Hiring managers spend an average of 30 seconds reviewing each cover letter, so conciseness matters.'),
            ('Should I customize my cover letter for each job?', 'Yes, tailoring your cover letter to each position significantly increases your chances. Reference the company name, specific role, and how your skills match the listed requirements.'),
            ('What tone should a cover letter use?', 'Use a professional but personable tone. Avoid overly formal language and instead write naturally while demonstrating enthusiasm for the role and company.'),
            ('Is this cover letter generator free?', 'Yes, this tool is completely free with no registration required. It generates professional cover letters based on your input and runs entirely in your browser.'),
        ]
    },
    'gear-ratio-calculator': {
        'name': 'Gear Ratio Calculator',
        'category': 'Utility',
        'faqs': [
            ('How do I calculate a gear ratio?', 'Divide the number of teeth on the driven gear by the number of teeth on the driving gear. For example, a 40-tooth driven gear with a 20-tooth driver gives a 2:1 ratio.'),
            ('What does a higher gear ratio mean?', 'A higher gear ratio means more torque multiplication but lower output speed. A 4:1 ratio quadruples the torque while reducing the output speed to one quarter of the input.'),
            ('How do I calculate gear ratio for a multi-stage gear train?', 'Multiply the individual gear ratios of each stage together. A two-stage train with ratios of 3:1 and 4:1 produces an overall ratio of 12:1.'),
            ('What is the difference between gear ratio and speed ratio?', 'Gear ratio is driven teeth divided by driver teeth. Speed ratio is the inverse - it tells you how the output speed relates to input speed. A 3:1 gear ratio means a 1:3 speed ratio.'),
            ('Can I calculate bicycle gear ratios with this tool?', 'Yes, enter your chainring teeth as the driving gear and your cassette sprocket teeth as the driven gear. The calculator shows your gear ratio and effective gear inches.'),
        ]
    },
    'interest-rate-calculator': {
        'name': 'Interest Rate Calculator',
        'category': 'Finance',
        'faqs': [
            ('How do I calculate the interest rate on a loan?', 'Enter the principal amount, total amount paid, and loan term. The calculator determines the annual interest rate using standard financial formulas.'),
            ('What is the difference between APR and interest rate?', 'The interest rate is the cost of borrowing the principal, while APR includes the interest rate plus fees and other charges, giving you the true annual cost of a loan.'),
            ('How does compound interest differ from simple interest?', 'Simple interest is calculated only on the principal. Compound interest is calculated on the principal plus previously earned interest, causing your balance to grow faster over time.'),
            ('What is a good interest rate for a personal loan?', 'Personal loan rates typically range from 6% to 36%. A good rate depends on your credit score, income, and the lender. Rates below 10% are generally considered favorable.'),
            ('Can this calculator handle different compounding frequencies?', 'Yes, you can select monthly, quarterly, semi-annual, or annual compounding to see how frequency affects the effective interest rate and total cost.'),
        ]
    },
    'led-resistor-calculator': {
        'name': 'LED Resistor Calculator',
        'category': 'Utility',
        'faqs': [
            ('How do I calculate the resistor value for an LED?', 'Use the formula R = (Vs - Vf) / If, where Vs is supply voltage, Vf is LED forward voltage, and If is the desired forward current, typically 20mA for standard LEDs.'),
            ('What happens if I use the wrong resistor with an LED?', 'Too low a resistance allows excessive current that burns out the LED. Too high a resistance limits current so the LED appears dim or does not light up at all.'),
            ('What is the typical forward voltage for different LED colors?', 'Red LEDs typically have a 1.8-2.2V forward voltage, green and yellow are 2.0-2.4V, blue and white are 3.0-3.6V. Check your LED datasheet for exact values.'),
            ('Can I connect multiple LEDs to one resistor?', 'Yes, for LEDs in series, add their forward voltages and use one resistor. For parallel LEDs, each should have its own resistor to ensure equal current distribution.'),
            ('What wattage resistor do I need for my LED circuit?', 'Calculate power as P = I squared times R. For a typical 20mA LED circuit, a standard 1/4 watt resistor is usually sufficient. Use a higher wattage for extra safety margin.'),
        ]
    },
    'matrix-calculator': {
        'name': 'Matrix Calculator',
        'category': 'Education',
        'faqs': [
            ('What matrix operations does this calculator support?', 'This calculator supports addition, subtraction, multiplication, determinant, inverse, transpose, eigenvalues, and row echelon form for matrices up to 10x10.'),
            ('How do I multiply two matrices?', 'Matrix multiplication requires the number of columns in the first matrix to equal the number of rows in the second. Each element is the dot product of a row from the first matrix and a column from the second.'),
            ('What is a matrix determinant used for?', 'The determinant indicates whether a matrix is invertible (non-zero determinant), calculates area/volume scaling in transformations, and appears in solutions to systems of linear equations.'),
            ('When is a matrix not invertible?', 'A matrix is not invertible (singular) when its determinant equals zero. This happens when rows or columns are linearly dependent, meaning one can be expressed as a combination of others.'),
            ('Can this calculator solve systems of linear equations?', 'Yes, enter the coefficient matrix and use row reduction to solve the system. The calculator shows each step of the Gaussian elimination process.'),
        ]
    },
    'mulch-calculator': {
        'name': 'Mulch Calculator',
        'category': 'Utility',
        'faqs': [
            ('How much mulch do I need for my garden?', 'Measure your garden area in square feet, decide on mulch depth (typically 2-4 inches), and use this calculator. It converts the result to cubic yards, which is how mulch is sold.'),
            ('How deep should I apply mulch?', 'Apply 2-3 inches for flower beds and around trees, 3-4 inches for pathways and weed suppression. Avoid piling mulch deeper than 4 inches as it can suffocate plant roots.'),
            ('How many cubic yards of mulch do I need per square foot?', 'At 3 inches deep, you need about 1 cubic yard for every 108 square feet of coverage. At 2 inches, one cubic yard covers about 162 square feet.'),
            ('What type of mulch is best for landscaping?', 'Hardwood mulch works well for most flower beds, pine bark is ideal for acid-loving plants, and rubber mulch lasts longest for playgrounds. Each type has different coverage rates per bag.'),
            ('How often should I replace mulch?', 'Organic mulch typically needs refreshing once a year as it decomposes. Add 1-2 inches annually to maintain proper depth. Inorganic mulch like rubber or stone rarely needs replacement.'),
        ]
    },
    'ovulation-calculator': {
        'name': 'Ovulation Calculator',
        'category': 'Health',
        'faqs': [
            ('How do I calculate my ovulation date?', 'Ovulation typically occurs 14 days before your next expected period. Enter your last period start date and average cycle length, and this calculator estimates your fertile window.'),
            ('What is a fertile window?', 'Your fertile window is the approximately 6-day period when pregnancy is possible - the 5 days before ovulation plus the day of ovulation itself. Sperm can survive up to 5 days in the reproductive tract.'),
            ('How accurate are ovulation calculators?', 'Ovulation calculators provide estimates based on average cycle patterns. They are most accurate for women with regular cycles. For irregular cycles, ovulation test kits or basal body temperature tracking provide better accuracy.'),
            ('What is a normal menstrual cycle length?', 'A normal menstrual cycle ranges from 21 to 35 days, with 28 days being the average. Cycle length can vary month to month, which affects ovulation timing.'),
            ('Can I use this calculator to avoid pregnancy?', 'This calculator is designed as an educational estimation tool only. It should not be used as a sole method of contraception. Consult a healthcare provider for birth control guidance.'),
        ]
    },
    'salary-to-hourly-calculator': {
        'name': 'Salary to Hourly Calculator',
        'category': 'Finance',
        'faqs': [
            ('How do I convert my annual salary to an hourly rate?', 'Divide your annual salary by the number of work hours per year. For a standard 40-hour week with 52 weeks, divide by 2,080. A $50,000 salary equals about $24.04 per hour.'),
            ('How many work hours are in a year?', 'A standard work year has 2,080 hours (40 hours per week times 52 weeks). After accounting for typical paid time off, the actual working hours are closer to 1,920-2,000.'),
            ('Does this calculator account for taxes?', 'This calculator shows gross hourly rate conversions. Your net (take-home) hourly rate will be lower after federal, state, and local taxes, plus deductions for benefits.'),
            ('How do I compare a salary offer to an hourly job?', 'Convert the salary to hourly using this tool, then factor in benefits value. Salaried positions often include health insurance, retirement matching, and paid leave worth 20-30% of base pay.'),
            ('What is considered a good hourly rate?', 'A good hourly rate depends on your location, industry, and experience. The national median hourly wage is around $22-$23. Rates above $30/hour are generally considered above average.'),
        ]
    },
    'tile-calculator': {
        'name': 'Tile Calculator',
        'category': 'Utility',
        'faqs': [
            ('How do I calculate how many tiles I need?', 'Measure your floor or wall area in square feet, select your tile size, and this calculator determines the number of tiles needed, including a waste factor for cuts and breakage.'),
            ('How much tile waste should I plan for?', 'Plan for 10% extra for standard layouts and 15% for diagonal or complex patterns. Irregular room shapes may require up to 20% waste. Always round up to the nearest full box.'),
            ('What is the standard tile size for floors?', 'Common floor tile sizes are 12x12 inches, 12x24 inches, and 18x18 inches. Larger tiles like 24x24 are trending for modern spaces but require a flatter subfloor.'),
            ('How do I account for grout lines in tile calculations?', 'Standard grout lines are 1/8 to 1/4 inch wide. This calculator includes grout spacing in its area calculations so the tile count is accurate for your chosen joint width.'),
            ('How much does tile installation cost per square foot?', 'Professional tile installation typically costs $5-$15 per square foot for labor, depending on tile type and pattern complexity. Material costs are additional, ranging from $1-$20 per square foot.'),
        ]
    },
    'time-to-decimal-calculator': {
        'name': 'Time to Decimal Calculator',
        'category': 'Utility',
        'faqs': [
            ('How do I convert hours and minutes to decimal time?', 'Divide the minutes by 60 and add to the hours. For example, 2 hours 30 minutes equals 2.50 decimal hours (30/60 = 0.50).'),
            ('Why do I need to convert time to decimal format?', 'Decimal time is used for payroll processing, billing clients, project time tracking, and spreadsheet calculations. It makes adding and multiplying time values much simpler.'),
            ('What is 45 minutes in decimal?', '45 minutes equals 0.75 in decimal format (45 divided by 60 = 0.75). So 3 hours and 45 minutes would be 3.75 decimal hours.'),
            ('How do I convert decimal hours back to hours and minutes?', 'Take the decimal portion and multiply by 60 to get minutes. For example, 4.25 hours equals 4 hours and 15 minutes (0.25 x 60 = 15).'),
            ('Is this calculator useful for timesheet rounding?', 'Yes, many employers round time to the nearest quarter hour (0.25) for payroll. This calculator helps verify that your timesheet entries are correctly rounded.'),
        ]
    },
    'time-zone-meeting-planner': {
        'name': 'Time Zone Meeting Planner',
        'category': 'Utility',
        'faqs': [
            ('How do I schedule a meeting across multiple time zones?', 'Select the time zones of all participants and this planner highlights overlapping business hours. It shows the best meeting times that fall within working hours for everyone.'),
            ('What are standard business hours for international scheduling?', 'Standard business hours are typically 9 AM to 5 PM local time. When scheduling across continents, you may need to find overlap windows as narrow as 1-2 hours.'),
            ('Does this planner account for daylight saving time?', 'Yes, this tool adjusts for daylight saving time changes automatically. Time zone offsets update based on the selected date so your meeting time is always accurate.'),
            ('What is the best time to schedule a meeting between the US and Europe?', 'For US Eastern and Central European time, the best overlap is typically 9-11 AM Eastern (3-5 PM Central European). Adjust earlier for US Pacific time participants.'),
            ('Can I plan meetings for more than two time zones?', 'Yes, add as many time zones as needed. The planner identifies windows where all participants have reasonable working hours and highlights the optimal meeting slots.'),
        ]
    },
    'tip-split-calculator': {
        'name': 'Tip Split Calculator',
        'category': 'Finance',
        'faqs': [
            ('How do I split a restaurant bill with tip?', 'Enter the bill total, select your tip percentage, and choose the number of people splitting. The calculator shows each person share including their portion of the tip.'),
            ('What is the standard tip percentage at restaurants?', '15% is considered the minimum for adequate service in the US, 18-20% is standard for good service, and 25% or more is generous. Tip customs vary by country.'),
            ('Should I tip before or after tax?', 'Traditionally, tips are calculated on the pre-tax subtotal. However, many people tip on the post-tax total for simplicity. This calculator lets you choose either method.'),
            ('How do I calculate a 20% tip quickly?', 'Move the decimal point one place left to find 10%, then double it. For a $45.00 bill, 10% is $4.50, so 20% is $9.00, making the total $54.00.'),
            ('Can I split the bill unevenly with this calculator?', 'Yes, this tool supports custom split amounts so each person can pay a different share while the tip is distributed proportionally based on what each person ordered.'),
        ]
    },
    'trademark-search': {
        'name': 'Trademark Search Tool',
        'category': 'Business',
        'faqs': [
            ('How do I search for an existing trademark?', 'Enter your proposed business name, brand, or slogan and this tool searches registered trademarks. It checks for exact matches and similar names that could cause conflicts.'),
            ('Why should I search trademarks before starting a business?', 'Using a name that is already trademarked can result in cease-and-desist letters, forced rebranding, and legal liability. A search helps you avoid these costly problems before you invest in branding.'),
            ('What is the difference between a trademark and a trade name?', 'A trademark protects a brand name or logo used on goods or services. A trade name (or DBA) is the legal name under which a company conducts business. Both can be searched and registered.'),
            ('How long does a trademark registration last?', 'A US federal trademark registration lasts 10 years and can be renewed indefinitely in 10-year increments, as long as you continue using the mark in commerce and file required maintenance documents.'),
            ('Can I trademark a common word?', 'Common words can be trademarked if they are used in a distinctive way for specific goods or services. For example, Apple is trademarked for electronics but not for fruit.'),
        ]
    },
    'wallpaper-calculator': {
        'name': 'Wallpaper Calculator',
        'category': 'Utility',
        'faqs': [
            ('How do I calculate how many rolls of wallpaper I need?', 'Measure your wall height and total wall width, subtract window and door areas, then divide by the coverage per roll. This calculator handles all the math including pattern repeat waste.'),
            ('How much wall does one roll of wallpaper cover?', 'A standard American single roll covers about 36 square feet. A European roll covers about 57 square feet. Double rolls, which are more common in stores, cover roughly 72 square feet.'),
            ('What is pattern repeat and why does it matter?', 'Pattern repeat is the distance between identical points in a wallpaper design. Larger pattern repeats create more waste because you need to align each strip, sometimes discarding significant amounts.'),
            ('How do I account for windows and doors in wallpaper calculations?', 'Measure the width and height of each window and door, then subtract those areas from the total wall area. This calculator has fields for entering door and window dimensions.'),
            ('Should I buy extra wallpaper?', 'Yes, buy 10-15% more than calculated to account for cutting waste, pattern matching, and future repairs. Wallpaper from different production batches can have slight color variations.'),
        ]
    },
}

def get_tool_info(slug):
    """Extract title and description from the HTML file."""
    filepath = os.path.join(BASE, slug, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    if title_match:
        raw_title = title_match.group(1).strip()
        # Clean title - remove " - Free ..." suffix for the name
        name = re.sub(r'\s*[-|]\s*(Free|Online|Tool|Calculator).*$', '', raw_title, flags=re.IGNORECASE).strip()
        if not name:
            name = raw_title
    else:
        # Try h1
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        if h1_match:
            name = h1_match.group(1).strip()
        else:
            name = slug.replace('-', ' ').title()

    # Extract description
    desc_match = re.search(r'name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content)
    if not desc_match:
        desc_match = re.search(r'content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', content)
    desc = desc_match.group(1).strip() if desc_match else f'Free online {name.lower()} tool.'

    return name, desc, content


def build_webapp_schema(slug, name, desc, category):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": name,
        "description": desc,
        "url": f"https://zovo.one/free-tools/{slug}/",
        "applicationCategory": f"{category}Application",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Michael Lip"}
    }, indent=2)


def build_faq_schema(faqs):
    entities = []
    for q, a in faqs:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, indent=2)


def build_breadcrumb_schema(slug, name):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://zovo.one/"},
            {"@type": "ListItem", "position": 2, "name": "Free Tools", "item": "https://zovo.one/free-tools/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"https://zovo.one/free-tools/{slug}/"}
        ]
    }, indent=2)


def process_tool(slug):
    filepath = os.path.join(BASE, slug, 'index.html')
    name, desc, content = get_tool_info(slug)

    config = TOOL_CONFIGS.get(slug)
    if not config:
        print(f"  SKIP {slug}: no config defined")
        return False

    # Use config name if available
    display_name = config.get('name', name)
    category = config.get('category', 'Utility')
    faqs = config.get('faqs', [])

    has_webapp = '"WebApplication"' in content
    has_faq = '"FAQPage"' in content
    has_breadcrumb = '"BreadcrumbList"' in content

    if has_webapp and has_faq and has_breadcrumb:
        print(f"  SKIP {slug}: already has all schemas")
        return False

    # Build the schemas to add
    schemas_to_add = []
    if not has_webapp:
        schemas_to_add.append(f'<script type="application/ld+json">\n{build_webapp_schema(slug, display_name, desc, category)}\n</script>')
    if not has_faq and faqs:
        schemas_to_add.append(f'<script type="application/ld+json">\n{build_faq_schema(faqs)}\n</script>')
    if not has_breadcrumb:
        schemas_to_add.append(f'<script type="application/ld+json">\n{build_breadcrumb_schema(slug, display_name)}\n</script>')

    if not schemas_to_add:
        print(f"  SKIP {slug}: nothing to add")
        return False

    schema_block = '\n'.join(schemas_to_add)

    # Find insertion point
    modified = False

    # Strategy 1: Insert before </head>
    head_close_idx = content.find('</head>')
    if head_close_idx > 0:
        # Check if there are existing ld+json blocks - insert after the last one before </head>
        last_ld_end = -1
        for m in re.finditer(r'</script>\s*(?=<script type="application/ld\+json">|</head>)', content[:head_close_idx]):
            last_ld_end = m.end()

        if last_ld_end > 0:
            content = content[:last_ld_end] + '\n' + schema_block + '\n' + content[last_ld_end:]
        else:
            content = content[:head_close_idx] + '\n' + schema_block + '\n' + content[head_close_idx:]
        modified = True
    elif '</head' in content:
        # Some files have </head> without proper >
        head_close_idx = content.find('</head')
        content = content[:head_close_idx] + '\n' + schema_block + '\n' + content[head_close_idx:]
        modified = True
    else:
        # No </head> found - look for <body> or first <header> or <nav>
        for marker in ['<body', '<header', '<nav ']:
            idx = content.find(marker)
            if idx > 0:
                content = content[:idx] + '\n' + schema_block + '\n' + content[idx:]
                modified = True
                break

    if not modified:
        print(f"  ERROR {slug}: could not find insertion point")
        return False

    # Remove bold tags if needed (for acre-square-footage, gear-ratio-calculator, date-difference-calculator)
    if slug in ('acre-square-footage', 'gear-ratio-calculator', 'date-difference-calculator'):
        content = re.sub(r'</?strong>', '', content)
        content = re.sub(r'</?b>', '', content)
        print(f"  Removed bold tags from {slug}")

    # For gear-ratio-calculator: add canonical + OG meta tags if missing
    if slug == 'gear-ratio-calculator':
        if 'rel="canonical"' not in content and "rel='canonical'" not in content:
            # Find a place to insert canonical - before </head> or before first schema
            insert_before = content.find('<script type="application/ld+json">')
            if insert_before < 0:
                insert_before = content.find('</head')
            if insert_before > 0:
                canonical_og = (
                    f'<link rel="canonical" href="https://zovo.one/free-tools/gear-ratio-calculator/">\n'
                    f'<meta property="og:title" content="Gear Ratio Calculator - Free Online Tool">\n'
                    f'<meta property="og:description" content="Calculate gear ratios, speed reduction, torque multiplication, and output RPM for spur gears and multi-stage gear trains.">\n'
                    f'<meta property="og:type" content="website">\n'
                    f'<meta property="og:url" content="https://zovo.one/free-tools/gear-ratio-calculator/">\n'
                    f'<meta property="og:site_name" content="Zovo">\n'
                )
                content = content[:insert_before] + canonical_og + content[insert_before:]
                print(f"  Added canonical + OG tags to gear-ratio-calculator")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    added = []
    if not has_webapp: added.append('WebApp')
    if not has_faq: added.append('FAQ')
    if not has_breadcrumb: added.append('Breadcrumb')
    print(f"  OK {slug}: added {', '.join(added)}")
    return True


def main():
    tools_to_process = [
        'acre-square-footage', 'ascii-banner-generator', 'commercial-mortgage-calculator',
        'completing-the-square-calculator', 'cover-letter-generator',
        'gear-ratio-calculator', 'interest-rate-calculator',
        'led-resistor-calculator', 'matrix-calculator', 'mulch-calculator',
        'ovulation-calculator', 'salary-to-hourly-calculator', 'tile-calculator',
        'time-to-decimal-calculator', 'time-zone-meeting-planner', 'tip-split-calculator',
        'trademark-search', 'wallpaper-calculator'
    ]

    processed = 0
    for slug in tools_to_process:
        filepath = os.path.join(BASE, slug, 'index.html')
        if not os.path.exists(filepath):
            print(f"  MISSING {slug}: file not found")
            continue
        if process_tool(slug):
            processed += 1

    print(f"\nTotal processed: {processed}/{len(tools_to_process)}")


if __name__ == '__main__':
    main()
