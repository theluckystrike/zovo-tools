#!/usr/bin/env python3
"""Add FAQ schema (L12) to tools missing it."""

import re
import json
import subprocess
import os

os.chdir('/Users/mike/zovo-workspaces/zovo-tools')

# Tool-specific FAQs
TOOL_FAQS = {
    "keto-calculator": [
        ("What is a keto macro calculator?", "A keto macro calculator determines your ideal daily intake of fat, protein, and carbohydrates for a ketogenic diet. It uses your body metrics, activity level, and goals to calculate the right ratio, typically around 70% fat, 25% protein, and 5% carbs."),
        ("How many carbs should I eat on keto?", "Most standard ketogenic diets recommend limiting net carbs to 20 to 50 grams per day. Net carbs are calculated by subtracting fiber from total carbohydrates. This restriction helps your body enter and maintain ketosis."),
        ("How long does it take to enter ketosis?", "It generally takes 2 to 7 days of restricting carbohydrates to enter ketosis. The exact timeline depends on factors like your prior diet, activity level, and individual metabolism. Testing with urine strips or a blood ketone meter can confirm when you have reached ketosis."),
        ("Should I track net carbs or total carbs on keto?", "Most keto practitioners track net carbs, which exclude fiber and certain sugar alcohols that do not raise blood sugar. This approach allows more vegetable and fiber consumption while still maintaining ketosis."),
        ("Can I use this calculator if I am doing a targeted keto diet?", "Yes, you can adjust the settings for a targeted ketogenic diet (TKD) by increasing your carb allowance around workouts. A TKD typically adds 25 to 50 grams of easily digestible carbs before exercise to fuel high-intensity training."),
    ],
    "logo-maker": [
        ("Is this logo maker completely free to use?", "Yes, this logo maker is 100% free with no hidden fees or watermarks. You can create and download your custom logo at full resolution without creating an account or providing payment information."),
        ("What file formats can I download my logo in?", "You can download your finished logo in PNG format with a transparent background. PNG is widely supported across websites, social media platforms, print materials, and business documents."),
        ("Can I use logos created here for commercial purposes?", "Yes, logos you design with this tool are yours to use for any purpose, including commercial use. You retain full ownership of the designs you create using the available shapes, fonts, and color options."),
        ("Do I need design experience to create a logo?", "No design experience is required. The tool provides intuitive controls for choosing icons, adjusting colors, selecting fonts, and arranging elements. You can create a professional-looking logo in just a few minutes."),
        ("Can I edit my logo after downloading it?", "You can return to the tool and recreate your logo with different settings at any time. For further editing, you can open the downloaded PNG file in any image editor to make additional adjustments."),
    ],
    "macro-calculator": [
        ("What does a macro calculator do?", "A macro calculator determines your total daily energy expenditure (TDEE) and breaks it down into recommended grams of protein, carbohydrates, and fat. It factors in your age, weight, height, activity level, and fitness goals to provide personalized targets."),
        ("How accurate are macro calculators?", "Macro calculators provide a solid starting point based on established formulas like Mifflin-St Jeor. However, individual metabolism varies, so it is best to use the results as initial targets and adjust based on your progress over 2 to 4 weeks."),
        ("What is the difference between macros and calories?", "Calories measure total energy intake, while macros (macronutrients) break that energy into three categories: protein (4 calories per gram), carbohydrates (4 calories per gram), and fat (9 calories per gram). Tracking macros gives you more control over body composition than tracking calories alone."),
        ("How much protein do I need per day?", "Protein needs vary based on your goals and activity level. A common recommendation is 0.7 to 1.0 grams per pound of body weight for active individuals, with higher amounts (up to 1.2 grams per pound) for those focused on muscle building."),
        ("Should I adjust my macros on rest days?", "Many people reduce carbohydrate intake slightly on rest days since energy demands are lower. You can keep protein the same to support recovery and reduce carbs by 15 to 25 percent, shifting some of those calories to healthy fats."),
    ],
    "mortgage-extra-payment-calculator": [
        ("How much can extra mortgage payments save me?", "Extra mortgage payments can save tens of thousands of dollars in interest over the life of a loan. For example, adding just $200 per month to a $300,000 mortgage at 6.5% can save over $60,000 in interest and shorten the loan by several years."),
        ("Is it better to make extra payments monthly or as a lump sum?", "Both approaches reduce your principal and save interest, but making extra payments monthly is generally more effective because it reduces the principal sooner, meaning less interest accrues each month. A lump sum payment also helps but provides savings from only the point it is applied."),
        ("Are there penalties for making extra mortgage payments?", "Most conventional mortgages do not have prepayment penalties, but some loans, particularly certain adjustable-rate or subprime mortgages, may include them. Check your loan agreement or contact your lender to confirm before making extra payments."),
        ("Should I pay extra on my mortgage or invest the money?", "This depends on your mortgage interest rate compared to expected investment returns. If your mortgage rate is below 5 to 6 percent, investing may yield higher long-term returns. If your rate is higher, paying down the mortgage provides a guaranteed return equal to your interest rate."),
        ("How do I specify that extra payments go to principal?", "When making extra payments, instruct your lender to apply the additional amount to principal only. Many lenders have an option on their payment portal, or you can include a note with your payment specifying principal reduction."),
    ],
    "mortgage-recast-calculator": [
        ("What is a mortgage recast?", "A mortgage recast is when you make a large lump-sum payment toward your principal and your lender recalculates your monthly payment based on the reduced balance. Unlike refinancing, a recast keeps your existing interest rate and loan term while lowering your monthly obligation."),
        ("How is recasting different from refinancing?", "Recasting reduces your monthly payment by applying a lump sum to your principal without changing your interest rate or loan term. Refinancing replaces your entire loan with a new one, potentially at a different rate and term, and involves closing costs and a credit check."),
        ("What is the minimum lump sum required to recast a mortgage?", "Most lenders require a minimum lump-sum payment of $5,000 to $10,000 to recast a mortgage. The exact minimum varies by lender, and some may also charge a processing fee of $150 to $500 for the recast."),
        ("Can all types of mortgages be recast?", "Most conventional and conforming loans are eligible for recasting. However, FHA loans and VA loans generally cannot be recast. Jumbo loans may also have different recast policies depending on the lender."),
        ("When does a mortgage recast make sense?", "A recast makes sense when you receive a large sum of money, such as an inheritance or home sale proceeds, and want to lower your monthly payment without the costs of refinancing. It is particularly beneficial if your current interest rate is already favorable."),
    ],
    "mulch-calculator": [
        ("How do I calculate how much mulch I need?", "Measure the length and width of your garden bed in feet, then decide on the mulch depth (typically 2 to 4 inches). Multiply length by width by depth (converted to feet), then divide by 27 to get cubic yards. This calculator handles all these conversions automatically."),
        ("How deep should I apply mulch?", "For most garden beds, apply mulch 2 to 3 inches deep. Around trees, keep mulch 3 to 4 inches deep but leave a gap of several inches around the trunk to prevent rot. Deeper than 4 inches can suffocate plant roots and prevent water from reaching the soil."),
        ("How many bags of mulch are in a cubic yard?", "A standard 2-cubic-foot bag of mulch contains about 0.074 cubic yards. You need approximately 13.5 bags to equal one cubic yard. Buying in bulk by the cubic yard is usually more cost-effective for areas larger than 200 square feet."),
        ("What type of mulch is best for landscaping?", "Hardwood mulch and cedar mulch are popular choices for landscape beds because they decompose slowly and resist insects. Cypress mulch is durable in wet climates, while pine bark nuggets work well on slopes. The best choice depends on your climate, budget, and aesthetic preference."),
        ("How often should I replace mulch?", "Organic mulch typically needs replenishing once a year, usually in spring. Over the year it decomposes, which is actually beneficial because it adds nutrients to the soil. Top off thin areas to maintain a consistent 2 to 3 inch depth."),
    ],
    "number-system-converter": [
        ("What number systems does this converter support?", "This converter supports binary (base 2), octal (base 8), decimal (base 10), and hexadecimal (base 16) number systems. You can convert between any pair of these systems instantly by entering a value in one field."),
        ("How do I convert binary to decimal?", "To convert binary to decimal, multiply each bit by 2 raised to its position power (starting from 0 on the right) and sum the results. For example, binary 1010 equals 1x8 + 0x4 + 1x2 + 0x1, which is 10 in decimal. This tool performs the conversion automatically."),
        ("What is hexadecimal used for?", "Hexadecimal is widely used in computing to represent binary data in a more compact, human-readable format. Each hex digit represents exactly 4 binary bits, making it common in color codes (like #FF0000 for red), memory addresses, and MAC addresses."),
        ("Why do computers use binary?", "Computers use binary because their circuits have two states: on and off, represented as 1 and 0. All data and instructions in a computer, from text to images to programs, are ultimately stored and processed as sequences of these binary digits."),
        ("What is the difference between octal and hexadecimal?", "Octal uses digits 0 through 7 (base 8) while hexadecimal uses digits 0 through 9 plus letters A through F (base 16). Hexadecimal is more common in modern computing because each hex digit maps to exactly 4 binary bits, aligning with byte boundaries."),
    ],
    "payroll-tax-calculator": [
        ("What taxes are included in payroll tax calculations?", "Payroll taxes typically include Social Security tax (6.2% for both employer and employee), Medicare tax (1.45% each), and federal income tax withholding. Some states also require state income tax, unemployment insurance, and disability insurance deductions."),
        ("What is the Social Security wage base limit?", "The Social Security wage base limit is the maximum amount of earnings subject to Social Security tax. For 2026, earnings above this threshold are not subject to the 6.2% Social Security tax, though all earnings remain subject to the 1.45% Medicare tax."),
        ("How is the additional Medicare tax calculated?", "An additional 0.9% Medicare tax applies to individual earnings above $200,000 (or $250,000 for married couples filing jointly). This surtax is paid only by the employee and is not matched by the employer."),
        ("What is the difference between gross pay and net pay?", "Gross pay is your total earnings before any deductions, while net pay (take-home pay) is what you receive after federal taxes, state taxes, Social Security, Medicare, and any voluntary deductions like retirement contributions or health insurance premiums are subtracted."),
        ("Do employers pay the same payroll taxes as employees?", "Employers match the employee's Social Security (6.2%) and Medicare (1.45%) contributions, paying an additional 7.65% on top of wages. Employers also pay federal and state unemployment taxes (FUTA and SUTA), which employees do not pay."),
    ],
    "percentage-change-calculator": [
        ("How do I calculate percentage change?", "Percentage change is calculated by subtracting the original value from the new value, dividing the result by the original value, and multiplying by 100. The formula is: ((New - Original) / Original) x 100. A positive result indicates an increase, while a negative result indicates a decrease."),
        ("What is the difference between percentage change and percentage difference?", "Percentage change compares a new value to an original value and has a direction (increase or decrease). Percentage difference compares two values without implying which came first, using the average of both values as the denominator."),
        ("Can percentage change exceed 100%?", "Yes, percentage change can exceed 100%. For example, if a stock price goes from $10 to $25, that is a 150% increase. Percentage change can be any positive or negative number, depending on the magnitude of the change."),
        ("How do I calculate a percentage decrease?", "Use the same formula as percentage change: ((New - Original) / Original) x 100. When the new value is smaller than the original, the result will automatically be negative, indicating a decrease. For example, going from 80 to 60 is a -25% change."),
        ("What is the percentage change from 0?", "Percentage change from zero is mathematically undefined because you would be dividing by zero. In practical applications, if a starting value is zero and the new value is non-zero, the change is considered infinite or is simply reported as the absolute change instead."),
    ],
    "protein-calculator": [
        ("How much protein do I need per day?", "Daily protein needs depend on your body weight, activity level, and goals. The general recommendation is 0.36 grams per pound (0.8 grams per kilogram) for sedentary adults. Active individuals and those building muscle should aim for 0.7 to 1.0 grams per pound of body weight."),
        ("When is the best time to eat protein?", "Distributing protein intake evenly across 3 to 5 meals throughout the day is more effective than consuming it all at once. Each meal should contain 20 to 40 grams of protein to maximize muscle protein synthesis. Post-workout protein within 2 hours of exercise also supports recovery."),
        ("Can I eat too much protein?", "For most healthy adults, high protein intake up to about 1.5 grams per pound of body weight is safe. However, individuals with kidney disease should consult their doctor before increasing protein. Excess protein beyond what your body needs will be converted to energy or stored."),
        ("What are the best sources of protein?", "High-quality protein sources include chicken breast, eggs, Greek yogurt, fish, lean beef, tofu, lentils, and whey protein. Animal sources are complete proteins containing all essential amino acids, while plant sources can be combined to achieve a complete amino acid profile."),
        ("Do I need more protein to build muscle?", "Yes, muscle building requires higher protein intake, typically 0.7 to 1.2 grams per pound of body weight daily. This higher intake, combined with resistance training, provides the amino acids needed for muscle repair and growth. Spreading intake across meals improves absorption."),
    ],
    "qr-code-designer": [
        ("How is a QR code designer different from a basic QR code generator?", "A QR code designer lets you customize the appearance of your QR code with colors, shapes, logos, and patterns while maintaining scannability. A basic generator creates standard black-and-white codes without visual customization options."),
        ("Can I add a logo to my QR code?", "Yes, you can embed a logo or image in the center of your QR code. QR codes have built-in error correction that allows up to 30% of the code to be obscured while remaining scannable. Keep your logo within this safe zone for reliable scanning."),
        ("Will a colored QR code still scan properly?", "Yes, colored QR codes scan reliably as long as there is sufficient contrast between the foreground and background. The foreground (dots) should be darker than the background. Avoid low-contrast combinations like yellow on white or light colors on light backgrounds."),
        ("What resolution should I use for printed QR codes?", "For print materials, export your QR code at a minimum of 300 DPI. The physical size should be at least 2 cm x 2 cm (about 0.8 inches) for close-range scanning. For posters or billboards meant to be scanned from a distance, increase the size proportionally."),
        ("What types of data can I encode in a custom QR code?", "You can encode URLs, plain text, email addresses, phone numbers, WiFi credentials, vCards, and geographic coordinates. URLs are the most common use case, allowing you to direct scanners to websites, landing pages, or digital content."),
    ],
    "qr-code-maker": [
        ("What is a QR code?", "A QR (Quick Response) code is a two-dimensional barcode that stores data in a grid of black and white squares. Originally developed for the automotive industry in Japan, QR codes are now used worldwide for linking to websites, sharing contact info, making payments, and more."),
        ("What can I create a QR code for?", "You can create QR codes for URLs, plain text, email addresses, phone numbers, SMS messages, WiFi network credentials, and vCards. The most common use is encoding a website URL so people can visit it simply by scanning the code with their phone camera."),
        ("Is there a size limit for QR code data?", "QR codes can store up to 4,296 alphanumeric characters or 7,089 numeric characters. However, more data means a denser, harder-to-scan code. For best results, keep URLs short and text concise. Most practical QR codes contain fewer than 300 characters."),
        ("Do QR codes expire?", "Static QR codes, like those generated by this tool, never expire. The data is encoded directly in the pattern and remains scannable indefinitely. Dynamic QR codes from some services can expire if the redirect service is discontinued."),
        ("How do I scan a QR code?", "Most modern smartphones can scan QR codes directly through their built-in camera app. Open your camera, point it at the QR code, and a notification or link will appear. If your camera does not support this, you can download a free QR scanner app from your app store."),
    ],
    "qr-reader": [
        ("How does a QR code reader work?", "A QR code reader uses your device's camera or an uploaded image to detect the distinctive square pattern of a QR code. It then decodes the black and white modules within the pattern to extract the stored data, which can be a URL, text, contact information, or other content."),
        ("Can I scan a QR code from a screenshot or saved image?", "Yes, this QR reader supports scanning from uploaded images as well as live camera feeds. Simply upload a screenshot, photo, or any image file containing a QR code, and the tool will decode it and display the stored content."),
        ("What types of QR codes can this reader decode?", "This reader can decode all standard QR code formats including URLs, plain text, email addresses, phone numbers, WiFi credentials, vCards, and geographic coordinates. It supports QR codes of any size, color, or error correction level."),
        ("Is it safe to scan unknown QR codes?", "Exercise caution when scanning QR codes from unknown sources. This tool shows you the decoded content before you act on it, so you can verify URLs before visiting them. Avoid scanning codes that redirect to suspicious websites or prompt you to download files."),
        ("Why is my QR code not scanning?", "Common reasons include poor image quality, insufficient lighting, damaged or partially obscured codes, or very small code sizes. Try improving lighting, holding the camera steady, getting closer to the code, or uploading a higher-resolution image."),
    ],
    "quadratic-equation-grapher": [
        ("What is a quadratic equation?", "A quadratic equation is a second-degree polynomial in the form ax-squared + bx + c = 0, where a is not zero. Its graph is a parabola that opens upward when a is positive and downward when a is negative. Quadratic equations appear in physics, engineering, economics, and many other fields."),
        ("What is the vertex of a parabola?", "The vertex is the highest or lowest point on a parabola. For an upward-opening parabola, the vertex is the minimum point; for a downward-opening one, it is the maximum. The vertex coordinates are found using the formula x = -b/(2a) and then plugging that x value back into the equation."),
        ("How do I find the roots of a quadratic equation?", "The roots (also called zeros or x-intercepts) are where the parabola crosses the x-axis. You can find them using the quadratic formula: x = (-b plus or minus the square root of b-squared minus 4ac) divided by 2a. This grapher displays the roots visually and numerically."),
        ("What does the discriminant tell you about a quadratic?", "The discriminant (b-squared minus 4ac) reveals how many real roots a quadratic equation has. A positive discriminant means two distinct real roots, zero means one repeated root (the parabola touches the x-axis at one point), and a negative discriminant means no real roots."),
        ("Can I use this grapher for homework and exams?", "This grapher is an excellent study tool for understanding how changing coefficients affects the shape and position of a parabola. It helps visualize the relationship between the equation and its graph, making it useful for algebra, pre-calculus, and physics coursework."),
    ],
    "random-picker": [
        ("How does the random picker work?", "The random picker uses a cryptographically secure random number generator built into your browser to make fair, unbiased selections. Whether picking a number, spinning a wheel, or choosing a name, each outcome has an equal probability of being selected."),
        ("Is the random selection truly random?", "Yes, this tool uses the Web Crypto API (crypto.getRandomValues) which provides cryptographically strong random values. This is far more random than basic Math.random() and is suitable for fair drawings, unbiased selections, and games where true randomness matters."),
        ("Can I use this for giveaways and contests?", "Yes, the random picker is suitable for selecting giveaway winners, raffle drawings, and contest selections. Each entry has an equal chance of being chosen. For transparency, you can screen-record the selection process to show participants that the drawing was fair."),
        ("How many items can I add to the random picker?", "You can add hundreds of items to the picker without performance issues. Simply enter each name or item on a separate line or separated by commas. The tool handles large lists efficiently and selects from them with equal probability."),
        ("Can I exclude items that have already been picked?", "Yes, you can remove previously selected items from the list before picking again to ensure no repeats. This is useful for drawings where each person can only win once, or for assigning tasks where each person should get a unique assignment."),
    ],
    "readability-checker": [
        ("What readability formulas does this checker use?", "This checker analyzes text using multiple established formulas including Flesch-Kincaid Grade Level, Flesch Reading Ease, Gunning Fog Index, Coleman-Liau Index, and SMOG Index. Using multiple formulas provides a more comprehensive assessment than relying on a single score."),
        ("What is a good readability score?", "For general web content, aim for a Flesch Reading Ease score of 60 to 70 (8th to 9th grade level). Most popular newspapers write at a 6th to 8th grade level. Technical or academic content may have lower scores, which is acceptable for specialized audiences."),
        ("How is readability different from grammar checking?", "Readability measures how easy text is to understand based on sentence length, word length, and syllable count. Grammar checking looks for errors in syntax, punctuation, and usage. Text can be grammatically perfect but still difficult to read if it uses complex sentence structures."),
        ("Can readability scores improve my SEO?", "Yes, search engines favor content that is easy to read and understand. Google considers user experience signals, and content with appropriate readability tends to have lower bounce rates and higher engagement. Aim for readability that matches your target audience."),
        ("How do I improve my readability score?", "Use shorter sentences (under 20 words on average), choose simpler words over complex ones, break up long paragraphs, use active voice instead of passive, and avoid jargon unless writing for a specialist audience. Replace multi-syllable words with shorter alternatives where possible."),
    ],
    "rental-yield-calculator": [
        ("What is rental yield?", "Rental yield is the annual rental income expressed as a percentage of the property's value. Gross rental yield is calculated by dividing annual rent by the property price and multiplying by 100. It is a key metric for comparing the income potential of different investment properties."),
        ("What is the difference between gross and net rental yield?", "Gross rental yield uses total rental income divided by property price. Net rental yield subtracts operating expenses (maintenance, insurance, property management fees, vacancies) from rental income before dividing by the total investment. Net yield gives a more accurate picture of actual returns."),
        ("What is a good rental yield?", "A good gross rental yield is typically 5% to 8%, while a net yield of 3% to 5% is considered solid in most markets. Higher yields often come with higher risk or less desirable locations. Markets like city centers may have lower yields but stronger capital appreciation."),
        ("What is cash-on-cash return?", "Cash-on-cash return measures the annual pre-tax cash flow relative to the total cash invested (down payment, closing costs, and renovation costs). It is particularly useful for leveraged purchases where you use a mortgage, as it shows the return on your actual cash outlay."),
        ("How does vacancy rate affect rental yield?", "Vacancy rate directly reduces your effective rental income. If your property sits empty for one month per year, that is roughly an 8% vacancy rate, reducing your annual income accordingly. This calculator factors in vacancy to give you a realistic net yield estimate."),
    ],
    "resistor-color-code-calculator": [
        ("How do resistor color codes work?", "Resistor color codes use colored bands painted on the resistor body to indicate its resistance value and tolerance. Each color represents a digit or multiplier. For a 4-band resistor, the first two bands are digits, the third is a multiplier, and the fourth indicates tolerance."),
        ("What is the difference between 4-band and 5-band resistors?", "A 4-band resistor has two significant digit bands, one multiplier band, and one tolerance band. A 5-band resistor adds a third significant digit band for greater precision. 5-band resistors are typically used in precision circuits where tighter tolerance is required."),
        ("What does the tolerance band mean?", "The tolerance band (usually the last band) indicates how much the actual resistance may vary from the stated value. A gold band means plus or minus 5%, silver means plus or minus 10%, and brown means plus or minus 1%. Tighter tolerance costs more but is needed for sensitive circuits."),
        ("How do I read a resistor if the colors are faded?", "If color bands are difficult to read, use a digital multimeter to measure the actual resistance value. Place the probes on each end of the resistor and read the ohm value directly. This gives you the precise resistance regardless of band readability."),
        ("What do resistor values like 4.7K or 2.2M mean?", "K stands for kilohms (thousands of ohms) and M stands for megohms (millions of ohms). So 4.7K equals 4,700 ohms, and 2.2M equals 2,200,000 ohms. These abbreviations are standard shorthand used in electronics schematics and component listings."),
    ],
    "resume-generator": [
        ("What is the difference between a resume generator and a resume builder?", "A resume generator creates a formatted resume from your input data, producing a ready-to-download document. A resume builder may offer more interactive editing, drag-and-drop sections, and real-time previews. Both help you create professional resumes without starting from scratch."),
        ("What format should I save my resume in?", "PDF is the preferred format for submitting resumes because it preserves formatting across all devices and operating systems. Some applicant tracking systems (ATS) also accept Word (.docx) files. Avoid submitting resumes as images, plain text, or Pages files."),
        ("How long should my resume be?", "For most professionals with less than 10 years of experience, keep your resume to one page. Those with extensive experience or academic backgrounds may use two pages. Recruiters spend an average of 6 to 7 seconds on an initial resume scan, so conciseness matters."),
        ("Should I include a summary or objective on my resume?", "A professional summary of 2 to 3 sentences highlighting your key qualifications and career focus is more effective than a generic objective statement. Tailor the summary to each job application, mentioning specific skills and achievements relevant to the position."),
        ("How do I make my resume ATS-friendly?", "Use standard section headings (Experience, Education, Skills), avoid tables and columns, use a clean sans-serif font, and include keywords from the job description. Avoid headers and footers, images, and graphics, as many ATS systems cannot parse these elements."),
    ],
    "sales-tax-calculator": [
        ("How do I calculate sales tax?", "Multiply the item price by the tax rate expressed as a decimal. For example, an item costing $50 with a 7% sales tax: $50 x 0.07 = $3.50 in tax, making the total $53.50. This calculator handles the conversion and addition automatically."),
        ("Do all US states have sales tax?", "No, five US states have no statewide sales tax: Alaska, Delaware, Montana, New Hampshire, and Oregon. However, some localities within Alaska do impose local sales taxes. States with sales tax have rates ranging from 2.9% (Colorado) to 7.25% (California)."),
        ("What is the difference between sales tax and use tax?", "Sales tax is collected by the seller at the point of purchase, while use tax is owed by the buyer on purchases where sales tax was not collected, such as online purchases from out-of-state retailers. The rates are typically the same."),
        ("Are groceries subject to sales tax?", "Sales tax on groceries varies by state. Most states exempt unprepared food and groceries from sales tax, but some states like Alabama, Mississippi, and South Dakota tax groceries at the full rate. Others apply a reduced rate to grocery items."),
        ("How do I calculate the pre-tax price from a total?", "To find the pre-tax price, divide the total amount by (1 + the tax rate as a decimal). For example, if the total is $107 and the tax rate is 7%: $107 / 1.07 = $100 pre-tax price. This reverse calculation is useful for expense tracking."),
    ],
    "sitemap-generator": [
        ("What is an XML sitemap?", "An XML sitemap is a file that lists all the important URLs on your website, helping search engines like Google discover and crawl your pages. It includes metadata such as when each page was last modified, how often it changes, and its relative priority on your site."),
        ("Do I need a sitemap for my website?", "A sitemap is recommended for any website, especially those with more than a few pages. It is particularly important for new sites (which have few external links), large sites (with hundreds of pages), and sites with pages that are not well linked internally."),
        ("How do I submit my sitemap to Google?", "Submit your sitemap through Google Search Console by navigating to the Sitemaps section and entering your sitemap URL. You can also reference your sitemap in your robots.txt file by adding a Sitemap directive. Google will then periodically re-crawl the listed URLs."),
        ("How many URLs can a sitemap contain?", "A single XML sitemap can contain up to 50,000 URLs and must not exceed 50 MB in size. If your site has more URLs, you can create multiple sitemaps and reference them from a sitemap index file. Most small to medium websites fit within a single sitemap."),
        ("Should I include every page in my sitemap?", "Include only pages you want search engines to index. Exclude pages with noindex tags, duplicate content, thin pages, admin pages, and thank-you or confirmation pages. A focused sitemap helps search engines prioritize your most important content."),
    ],
    "slug-generator": [
        ("What is a URL slug?", "A URL slug is the portion of a web address that comes after the domain name, identifying a specific page in a human-readable format. For example, in 'example.com/best-coffee-shops', the slug is 'best-coffee-shops'. Good slugs are short, descriptive, and use hyphens between words."),
        ("Why are URL slugs important for SEO?", "URL slugs help search engines understand what a page is about. Descriptive slugs containing relevant keywords can improve search rankings and click-through rates. Users are also more likely to click on a URL that clearly describes the page content."),
        ("What characters are allowed in a URL slug?", "URL slugs should contain only lowercase letters, numbers, and hyphens. Avoid spaces (use hyphens instead), special characters, accented letters, and uppercase letters. This ensures compatibility across all browsers and servers."),
        ("How long should a URL slug be?", "Keep slugs under 60 characters for optimal SEO and readability. Focus on 3 to 5 descriptive words that capture the page topic. Remove stop words like 'the', 'and', 'of', and 'in' unless they are essential to the meaning."),
        ("Can I change a URL slug after publishing?", "You can change a slug, but doing so changes the URL, which can break existing links and bookmarks. If you must change a slug, set up a 301 redirect from the old URL to the new one to preserve search rankings and prevent broken links."),
    ],
    "student-loan-repayment-calculator": [
        ("What federal student loan repayment plans are available?", "Federal student loan repayment plans include Standard (fixed payments over 10 years), Graduated (payments start low and increase), Extended (up to 25 years), and income-driven plans like IBR, PAYE, REPAYE, and ICR. Each plan has different eligibility requirements and forgiveness options."),
        ("How does income-driven repayment work?", "Income-driven repayment (IDR) plans cap your monthly payment at a percentage of your discretionary income, typically 10% to 20%. Payments adjust annually based on your income and family size. After 20 to 25 years of qualifying payments, any remaining balance is forgiven."),
        ("Should I consolidate my student loans?", "Consolidation combines multiple federal loans into one with a weighted average interest rate. It simplifies payments but may extend your repayment term and increase total interest paid. It can also make you eligible for certain repayment plans or forgiveness programs you did not previously qualify for."),
        ("Is it better to pay off student loans or invest?", "Compare your loan interest rate to expected investment returns. If your loans carry rates above 6%, paying them off provides a guaranteed return. For lower-rate loans, investing may yield higher long-term returns, especially in tax-advantaged accounts like a 401(k) with employer matching."),
        ("What is Public Service Loan Forgiveness?", "Public Service Loan Forgiveness (PSLF) forgives the remaining balance on Direct Loans after 120 qualifying monthly payments while working full-time for a qualifying employer, such as a government agency or nonprofit organization. The forgiven amount is not taxed as income."),
    ],
    "svg-editor": [
        ("What is SVG?", "SVG (Scalable Vector Graphics) is an XML-based format for two-dimensional vector images. Unlike raster formats like PNG or JPG, SVG images scale to any size without losing quality. They are widely used for logos, icons, illustrations, and web graphics."),
        ("Can I edit existing SVG files with this tool?", "Yes, you can open and edit existing SVG files directly in this editor. Upload your SVG file or paste the SVG code, and you can modify shapes, colors, paths, text, and other elements using the visual editor or by editing the underlying XML code."),
        ("What is the advantage of SVG over PNG?", "SVG files are resolution-independent, meaning they look crisp at any size on any screen. They typically have smaller file sizes for simple graphics, can be styled with CSS, animated with JavaScript, and are fully searchable and accessible. PNG is better for complex photographs."),
        ("Can I convert my SVG design to other formats?", "You can export your SVG design to PNG, JPG, or other raster formats from most SVG editors. This tool allows you to download your work as SVG for further editing or as a raster image at your preferred resolution for use in documents or presentations."),
        ("Is SVG supported in all web browsers?", "All modern web browsers (Chrome, Firefox, Safari, Edge) fully support SVG. Internet Explorer 9 and above also supports SVG with some limitations. SVG is safe to use for web projects, and any unsupported features can be addressed with fallback PNG images."),
    ],
    "take-home-pay-calculator": [
        ("What is take-home pay?", "Take-home pay is the amount of money you receive after all deductions are subtracted from your gross salary. These deductions include federal income tax, state income tax, Social Security, Medicare, and any voluntary deductions like health insurance or retirement contributions."),
        ("How do I calculate my take-home pay?", "Start with your gross salary, then subtract federal income tax (based on your tax bracket and filing status), state income tax, Social Security tax (6.2%), Medicare tax (1.45%), and any pre-tax deductions. This calculator automates all these calculations based on your specific situation."),
        ("Why is my take-home pay so much less than my salary?", "The gap between gross salary and take-home pay comes from mandatory payroll taxes (Social Security and Medicare totaling 7.65%), federal income tax (10% to 37% depending on bracket), state income tax (0% to 13.3% depending on state), and voluntary deductions."),
        ("How do tax brackets affect my take-home pay?", "Tax brackets apply progressively, meaning only the income within each bracket is taxed at that rate. For example, if you earn $60,000, the first portion is taxed at 10%, the next at 12%, and so on. You never pay your highest marginal rate on your entire income."),
        ("Does my filing status affect take-home pay?", "Yes, your filing status (Single, Married Filing Jointly, Head of Household) significantly affects your take-home pay. It determines your standard deduction amount and the income thresholds for each tax bracket. Married Filing Jointly generally results in lower taxes for dual-income households."),
    ],
    "text-case-converter": [
        ("What text cases does this converter support?", "This converter supports uppercase, lowercase, title case, sentence case, camelCase, PascalCase, snake_case, kebab-case, and toggle case. Each transformation is applied instantly as you type or paste text, and you can copy the result with one click."),
        ("What is the difference between camelCase and PascalCase?", "In camelCase, the first word starts with a lowercase letter and subsequent words are capitalized (for example, myVariableName). In PascalCase, every word starts with a capital letter, including the first (for example, MyVariableName). CamelCase is common in JavaScript; PascalCase is used for class names."),
        ("When should I use snake_case versus kebab-case?", "Snake_case (words separated by underscores) is the convention in Python, Ruby, and database column names. Kebab-case (words separated by hyphens) is standard for URLs, CSS class names, and HTML attributes. Each convention improves readability within its specific context."),
        ("How does title case work?", "Title case capitalizes the first letter of each major word while keeping minor words (like 'the', 'and', 'of', 'in') lowercase, unless they are the first or last word. It is the standard for headings, book titles, and article titles in English."),
        ("Can I convert text case for programming variable names?", "Yes, this tool can convert any text into programming-friendly formats like camelCase, PascalCase, snake_case, and CONSTANT_CASE. Simply paste your text, select the desired format, and copy the result to use directly in your code."),
    ],
    "text-to-speech": [
        ("How does text-to-speech work?", "Text-to-speech (TTS) technology converts written text into spoken audio using speech synthesis. Modern TTS systems use neural networks to produce natural-sounding voices. This tool uses your browser's built-in Web Speech API to generate audio directly on your device."),
        ("Can I choose different voices and languages?", "Yes, you can select from multiple voices and languages available through your browser's speech synthesis engine. The available voices depend on your operating system and browser. Most systems include both male and female voices in several languages."),
        ("Is this text-to-speech tool free?", "Yes, this tool is completely free with no usage limits or registration required. It runs entirely in your browser using the Web Speech API, so no data is sent to external servers. You can convert as much text as you need."),
        ("Can I save the audio output as a file?", "The availability of audio file downloads depends on the browser's speech synthesis implementation. Some browsers support saving the generated audio, while others only offer real-time playback. For saving audio files, a desktop TTS application may offer more export options."),
        ("What is the maximum text length for conversion?", "The text length limit depends on your browser and device capabilities. Most browsers handle several thousand characters without issues. For very long documents, consider breaking the text into smaller sections for smoother playback and better control over the reading position."),
    ],
    "timestamp-converter": [
        ("What is a Unix timestamp?", "A Unix timestamp is the number of seconds that have elapsed since January 1, 1970, at 00:00:00 UTC, known as the Unix epoch. It provides a simple, universal way to represent a specific moment in time as a single number, independent of time zones."),
        ("How do I convert a timestamp to a readable date?", "Enter the Unix timestamp (number of seconds since epoch) into this converter and it will display the corresponding date and time in both UTC and your local time zone. For example, timestamp 1700000000 corresponds to November 14, 2023 at 22:13:20 UTC."),
        ("What is the difference between seconds and milliseconds timestamps?", "Unix timestamps in seconds are 10 digits long (like 1700000000), while millisecond timestamps are 13 digits (like 1700000000000). JavaScript and Java commonly use milliseconds, while Python, PHP, and most Unix systems use seconds. This converter handles both formats."),
        ("Why do developers use Unix timestamps?", "Unix timestamps are timezone-independent, making them ideal for storing and comparing dates across systems in different time zones. They sort naturally as numbers, require minimal storage space, and avoid ambiguity caused by different date formats across countries."),
        ("What happens with the Year 2038 problem?", "The Year 2038 problem affects systems using 32-bit signed integers to store timestamps. The maximum value (2,147,483,647) corresponds to January 19, 2038 at 03:14:07 UTC. After this, the integer overflows. Most modern systems use 64-bit timestamps, which extend far beyond this date."),
    ],
    "timezone-converter": [
        ("How do I convert time between time zones?", "Select the source time zone, enter the time you want to convert, and choose the target time zone. The converter automatically accounts for the UTC offset difference between the two zones. You can also compare multiple time zones simultaneously."),
        ("What is UTC and why is it important?", "UTC (Coordinated Universal Time) is the global time standard from which all time zones are defined as offsets. It does not observe daylight saving time and serves as the reference point for international time coordination, aviation, computing, and scientific applications."),
        ("Does this converter account for daylight saving time?", "Yes, the converter uses your browser's timezone database which includes daylight saving time (DST) rules for each region. It automatically adjusts the conversion based on whether DST is currently in effect in the selected time zones."),
        ("What is the International Date Line?", "The International Date Line is an imaginary line at approximately 180 degrees longitude where the calendar date changes. Crossing it westward advances the date by one day, while crossing it eastward moves the date back one day. It zigzags to avoid splitting countries."),
        ("How do I schedule a meeting across multiple time zones?", "Enter the proposed meeting time in your local time zone, then add the time zones of all participants to see the equivalent time for each location. Aim for hours that fall within normal working times (9 AM to 6 PM) for as many participants as possible."),
    ],
    "upc-code-generator": [
        ("What is a UPC code?", "A UPC (Universal Product Code) is a 12-digit barcode used to identify retail products in the United States and Canada. Each product has a unique UPC that encodes the manufacturer and item number. It is the standard barcode you see on almost every product in stores."),
        ("How do I get a legitimate UPC code for my product?", "To get official UPC codes, join GS1 US and purchase a company prefix. This prefix forms the first part of your UPC codes, and you assign the remaining digits to individual products. Purchasing directly from GS1 ensures your codes are unique and accepted by all major retailers."),
        ("What is the difference between UPC-A and UPC-E?", "UPC-A is the standard 12-digit barcode used on most products. UPC-E is a compressed 6-digit version used on small packages where space is limited. UPC-E codes are derived from UPC-A codes by suppressing zeros, and they encode the same information."),
        ("Can I use this generator for actual retail products?", "This generator creates properly formatted UPC barcodes for testing, mockups, and educational purposes. For actual retail distribution, you need official UPC codes registered through GS1. Using unregistered codes can cause inventory conflicts with other products."),
        ("What is the check digit in a UPC code?", "The check digit is the last digit of a UPC code, calculated from the preceding 11 digits using a specific algorithm. It helps scanners detect errors by verifying the code was read correctly. If the check digit does not match the calculation, the scanner rejects the scan."),
    ],
    "url-encoder": [
        ("What is URL encoding?", "URL encoding (also called percent-encoding) replaces unsafe or reserved characters in a URL with a percent sign followed by their hexadecimal ASCII value. For example, a space becomes %20, and an ampersand becomes %26. This ensures URLs are transmitted correctly across the internet."),
        ("Why do URLs need to be encoded?", "URLs can only contain a limited set of ASCII characters. Characters like spaces, ampersands, question marks, and non-ASCII characters (accented letters, Chinese characters) must be encoded to be transmitted correctly. Without encoding, these characters can break URLs or cause misinterpretation."),
        ("What is the difference between encodeURI and encodeURIComponent?", "encodeURI encodes a full URI, preserving characters that have special meaning in URLs (like /, ?, and #). encodeURIComponent encodes individual URI components (like query parameters), encoding all special characters. Use encodeURIComponent for query string values."),
        ("When should I decode a URL?", "Decode URLs when you need to read the human-readable version of encoded text, such as extracting search queries from URLs or displaying encoded characters to users. For example, %E4%BD%A0%E5%A5%BD decodes to Chinese characters that would otherwise be unreadable."),
        ("Are there characters that should never be encoded?", "Unreserved characters (A-Z, a-z, 0-9, hyphen, period, underscore, and tilde) should not be encoded as they are safe in any part of a URL. Reserved characters (:, /, ?, #, @, etc.) should only be encoded when used outside their reserved purpose."),
    ],
    "url-shortener": [
        ("How does a URL shortener work?", "A URL shortener creates a compact link that redirects to the original long URL. When someone clicks the short link, the shortener service looks up the original URL in its database and redirects the browser to the full address. This makes links easier to share and remember."),
        ("Are shortened URLs safe to click?", "Shortened URLs can hide the true destination, so exercise caution with links from unknown sources. Reputable shorteners like bit.ly offer link preview features. You can also use URL expansion services to check where a short link leads before clicking it."),
        ("Do shortened URLs expire?", "It depends on the service. Major URL shorteners like bit.ly maintain links indefinitely as long as the service continues operating. Some services set expiration dates or delete links after periods of inactivity. Custom domain short links give you full control over link persistence."),
        ("Can I customize my shortened URL?", "Many URL shortening services allow custom aliases, letting you create memorable short links like yourdomain.com/sale instead of random characters. Custom short URLs are better for branding, easier to remember, and build more trust with recipients."),
        ("Why would I use a UTM builder with URL shortening?", "UTM parameters (source, medium, campaign) are appended to URLs to track marketing campaign performance in analytics tools like Google Analytics. Combining UTM parameters with URL shortening keeps links manageable while enabling detailed tracking of click sources and campaign effectiveness."),
    ],
    "uuid-generator": [
        ("What is a UUID?", "A UUID (Universally Unique Identifier) is a 128-bit number used to uniquely identify information in computer systems. Formatted as 32 hexadecimal digits in five groups separated by hyphens (like 550e8400-e29b-41d4-a716-446655440000), UUIDs are designed to be globally unique without a central authority."),
        ("What are the different UUID versions?", "UUID version 1 uses the current timestamp and MAC address. Version 4 is generated from random numbers and is the most commonly used. Version 5 uses SHA-1 hashing of a namespace and name. Version 7 (newer) combines a Unix timestamp with random data for sortable unique IDs."),
        ("When should I use UUIDs instead of auto-increment IDs?", "Use UUIDs when you need IDs that can be generated independently across distributed systems without coordination, when you want to prevent enumeration attacks, or when merging data from multiple databases. Auto-increment IDs are simpler and more efficient for single-database applications."),
        ("Are UUIDs truly unique?", "Version 4 UUIDs have 122 random bits, creating 5.3 x 10^36 possible values. The probability of generating a duplicate is astronomically low. You would need to generate 1 billion UUIDs per second for about 85 years to have a 50% chance of a single collision."),
        ("Can UUIDs be used as database primary keys?", "Yes, UUIDs work as primary keys, but they have trade-offs. They enable distributed ID generation and prevent enumeration. However, they use more storage (16 bytes versus 4 for integers), can cause index fragmentation in some databases, and are harder to communicate verbally."),
    ],
    "yaml-validator": [
        ("What is YAML?", "YAML (YAML Ain't Markup Language) is a human-readable data serialization format commonly used for configuration files. It uses indentation to represent structure and supports data types like strings, numbers, lists, and nested objects. Popular applications include Docker Compose, Kubernetes, Ansible, and CI/CD pipelines."),
        ("What are common YAML syntax errors?", "The most frequent YAML errors include incorrect indentation (YAML requires consistent spaces, not tabs), missing colons after keys, unquoted strings containing special characters, and improper list formatting. Mismatched indentation is the single most common cause of YAML parsing failures."),
        ("Can I use tabs for indentation in YAML?", "No, YAML strictly requires spaces for indentation. Tabs are not allowed and will cause parsing errors. Most YAML files use 2-space indentation, though any consistent number of spaces is valid. Configure your text editor to insert spaces when you press the Tab key."),
        ("How do I represent multi-line strings in YAML?", "YAML offers two multi-line string styles: the pipe character (|) preserves line breaks exactly as written, and the greater-than symbol (>) folds line breaks into spaces, creating a single flowing paragraph. Both are followed by the text on subsequent indented lines."),
        ("What is the difference between YAML and JSON?", "YAML supports comments, multi-line strings, and anchors/aliases for reuse, making it more human-friendly for configuration. JSON has stricter syntax, wider language support, and is better for data exchange between systems. Every valid JSON document is also valid YAML."),
    ],
    "yaml-to-json-converter": [
        ("Why would I convert YAML to JSON?", "Converting YAML to JSON is common when APIs require JSON input, when working with tools that only accept JSON, or when you need stricter data validation. JSON is universally supported by programming languages and web APIs, making it the preferred format for data interchange."),
        ("Does converting YAML to JSON lose any information?", "YAML comments are lost during conversion since JSON does not support comments. YAML anchors and aliases are resolved to their full values. All data values, structure, and types are preserved. If your YAML uses features without JSON equivalents, those features are expanded during conversion."),
        ("Can I convert JSON back to YAML?", "Yes, JSON-to-YAML conversion is straightforward because all valid JSON is also valid YAML. The conversion adds human-friendly formatting like indentation, removes braces and brackets, and optionally removes quotes from simple strings, making the result easier to read and edit."),
        ("How does YAML handle data types differently than JSON?", "YAML automatically infers data types: yes/no become booleans, unquoted numbers become integers or floats, and dates like 2026-03-26 become date objects. JSON requires explicit formatting: booleans must be true/false, numbers have no special handling, and dates are stored as strings."),
        ("What YAML features are not supported in JSON?", "JSON does not support comments, anchors and aliases (reference reuse), multi-line strings with pipe or fold operators, custom data types, or merge keys. These features are either expanded during conversion or lost entirely, which may affect readability but not data integrity."),
    ],
}


def process_tool(slug):
    filepath = f'/Users/mike/zovo-workspaces/zovo-tools/{slug}/index.html'
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {slug}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    if 'FAQPage' in content:
        print(f"SKIP (already has FAQ): {slug}")
        return False

    if slug not in TOOL_FAQS:
        print(f"SKIP (no FAQ data): {slug}")
        return False

    faqs = TOOL_FAQS[slug]

    # Build JSON-LD
    main_entity = []
    for q, a in faqs:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }

    json_ld = '<script type="application/ld+json">' + json.dumps(schema) + '</script>'

    # Build FAQ HTML
    faq_items = []
    for q, a in faqs:
        faq_items.append(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')

    faq_html = '<div class="faq-section" style="max-width:800px;margin:2rem auto;padding:0 20px;"><h2 style="color:#00ff88;font-size:1.4rem;margin-bottom:1rem;">Frequently Asked Questions</h2>' + ''.join(faq_items) + '</div>'

    # Add CSS for FAQ items if not already present
    faq_css = ''
    if '.faq-item' not in content:
        faq_css = '<style>.faq-section .faq-item{border-bottom:1px solid #2a2a3a;padding:16px 0}.faq-section .faq-item:last-child{border-bottom:none}.faq-section .faq-item h3{color:#e0e0e8;font-size:1.05rem;margin:0 0 8px 0;font-weight:500}.faq-section .faq-item p{color:#b0b0c0;font-size:0.95rem;line-height:1.7;margin:0}</style>'

    # Insert JSON-LD before </head>
    if '</head>' in content:
        content = content.replace('</head>', json_ld + faq_css + '</head>', 1)
    elif '<body' in content:
        idx = content.find('<body')
        content = content[:idx] + json_ld + faq_css + content[idx:]

    # Insert FAQ HTML before </html>
    if '</html>' in content:
        # Find last </html>
        idx = content.rfind('</html>')
        content = content[:idx] + faq_html + content[idx:]
    else:
        content = content + faq_html

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"DONE: {slug}")
    return True


# Process all tools
count = 0
for slug in TOOL_FAQS:
    success = process_tool(slug)
    if success:
        subprocess.run(['git', 'add', f'{slug}/index.html'], cwd='/Users/mike/zovo-workspaces/zovo-tools')
        result = subprocess.run(['git', 'commit', '-m', f'Add FAQ schema to {slug}'],
                              cwd='/Users/mike/zovo-workspaces/zovo-tools', capture_output=True, text=True)
        if result.returncode == 0:
            count += 1
            print(f"  Committed ({count})")
        else:
            print(f"  Commit failed: {result.stderr[:200]}")

        # Push every 20 commits
        if count > 0 and count % 20 == 0:
            print(f"  Pushing after {count} commits...")
            subprocess.run(['git', 'push'], cwd='/Users/mike/zovo-workspaces/zovo-tools')

print(f"\nAll done! {count} tools processed.")
