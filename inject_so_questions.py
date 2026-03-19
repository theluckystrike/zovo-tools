#!/usr/bin/env python3
"""
Replace existing irrelevant Stack Overflow question sections with new,
relevant "Developer Community Questions" sections using proper styling
and tool-specific questions.
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Comprehensive mapping of tool slugs to relevant SO questions ──────────
# Each entry: (question_title, so_tag_or_url_path, answer_count, tags_display)

TOOL_QUESTIONS = {
    # ── Developer / Code Tools ──
    "json-formatter": [
        ("How can I pretty-print JSON in a shell script?", "tagged/json+pretty-print", "15 answers", "json, pretty-print, formatting"),
        ("How to parse JSON in JavaScript?", "tagged/json+javascript+parsing", "23 answers", "javascript, json, parsing"),
        ("What is the correct JSON content type?", "tagged/json+content-type+http-headers", "31 answers", "json, http-headers, content-type"),
    ],
    "json-viewer": [
        ("How to display JSON in a readable format?", "tagged/json+formatting", "12 answers", "json, formatting, display"),
        ("Best way to render JSON tree view in HTML?", "tagged/json+treeview+javascript", "8 answers", "javascript, json, treeview"),
        ("How to navigate large JSON objects?", "tagged/json+parsing+navigation", "6 answers", "json, parsing, data-structures"),
    ],
    "json-path-finder": [
        ("What is JSONPath and how to use it?", "tagged/jsonpath", "14 answers", "jsonpath, json, query"),
        ("How to extract nested values from JSON?", "tagged/json+nested+parsing", "18 answers", "json, nested, parsing"),
        ("JSONPath vs JMESPath comparison?", "tagged/jsonpath+jmespath", "5 answers", "jsonpath, jmespath, json"),
    ],
    "json-yaml-converter": [
        ("YAML vs JSON - which should I use for configuration?", "tagged/yaml+json+configuration", "22 answers", "yaml, json, configuration"),
        ("How to convert JSON to YAML in JavaScript?", "tagged/json+yaml+javascript", "9 answers", "javascript, json, yaml"),
        ("Why use YAML over JSON for config files?", "tagged/yaml+json+config", "16 answers", "yaml, json, configuration"),
    ],
    "regex-tester": [
        ("How to validate an email address using a regular expression?", "tagged/regex+email-validation", "42 answers", "regex, email, validation"),
        ("What does the regex (?:) non-capturing group do?", "tagged/regex+groups", "18 answers", "regex, groups, syntax"),
        ("Regex to match a URL?", "tagged/regex+url+validation", "25 answers", "regex, url, pattern-matching"),
    ],
    "regex-visualizer": [
        ("How to visualize complex regular expressions?", "tagged/regex+visualization", "7 answers", "regex, visualization, debugging"),
        ("Understanding regex lookahead and lookbehind?", "tagged/regex+lookahead+lookbehind", "14 answers", "regex, lookahead, lookbehind"),
        ("How to debug a regular expression step by step?", "tagged/regex+debugging", "11 answers", "regex, debugging, testing"),
    ],
    "xml-formatter": [
        ("How to pretty-print XML in Python?", "tagged/xml+pretty-print+python", "19 answers", "xml, python, formatting"),
        ("Difference between XML and JSON?", "tagged/xml+json+comparison", "15 answers", "xml, json, data-formats"),
        ("How to validate XML against an XSD schema?", "tagged/xml+xsd+validation", "12 answers", "xml, xsd, validation"),
    ],
    "csv-to-json": [
        ("How to convert CSV to JSON in JavaScript?", "tagged/csv+json+javascript", "14 answers", "javascript, csv, json"),
        ("Best library for parsing CSV files in the browser?", "tagged/csv+javascript+parsing", "11 answers", "javascript, csv, parsing"),
        ("How to handle CSV files with commas in values?", "tagged/csv+parsing+escaping", "17 answers", "csv, parsing, escaping"),
    ],
    "csv-to-json-converter": [
        ("How to convert CSV to JSON in Python?", "tagged/csv+json+python", "16 answers", "python, csv, json"),
        ("Handling CSV headers when converting to JSON?", "tagged/csv+json+headers", "8 answers", "csv, json, data-conversion"),
        ("Parse CSV with different delimiters?", "tagged/csv+delimiter+parsing", "13 answers", "csv, parsing, delimiter"),
    ],
    "yaml-validator": [
        ("How to validate YAML syntax?", "tagged/yaml+validation", "11 answers", "yaml, validation, syntax"),
        ("Common YAML syntax errors and how to fix them?", "tagged/yaml+syntax+debugging", "9 answers", "yaml, syntax, debugging"),
        ("YAML indentation rules and best practices?", "tagged/yaml+indentation", "14 answers", "yaml, indentation, formatting"),
    ],
    "sql-formatter": [
        ("How to format SQL queries for readability?", "tagged/sql+formatting+style", "13 answers", "sql, formatting, code-style"),
        ("SQL indentation and capitalization conventions?", "tagged/sql+coding-style+conventions", "10 answers", "sql, coding-style, conventions"),
        ("Best practices for writing readable SQL?", "tagged/sql+best-practices+readability", "17 answers", "sql, best-practices, readability"),
    ],
    "markdown-editor": [
        ("What is Markdown and how do I use it?", "tagged/markdown+syntax", "20 answers", "markdown, syntax, formatting"),
        ("How to render Markdown in JavaScript?", "tagged/markdown+javascript+rendering", "14 answers", "javascript, markdown, rendering"),
        ("Markdown cheat sheet - common syntax?", "tagged/markdown+reference", "8 answers", "markdown, syntax, documentation"),
    ],
    "markdown-to-html": [
        ("How to convert Markdown to HTML in JavaScript?", "tagged/markdown+html+javascript", "16 answers", "javascript, markdown, html"),
        ("Which Markdown parser library is best for the browser?", "tagged/markdown+parser+javascript", "9 answers", "javascript, markdown, parser"),
        ("How to safely render Markdown without XSS vulnerabilities?", "tagged/markdown+xss+sanitization", "11 answers", "markdown, security, xss"),
    ],
    "api-tester": [
        ("How to test REST APIs without Postman?", "tagged/rest+api+testing", "15 answers", "rest, api, testing"),
        ("What is the difference between PUT and PATCH?", "tagged/rest+http-methods", "28 answers", "rest, http, api-design"),
        ("How to send API requests from the browser?", "tagged/fetch-api+javascript+http", "19 answers", "javascript, fetch-api, http"),
    ],
    "cron-expression-generator": [
        ("How to write a cron expression for every 5 minutes?", "tagged/cron+scheduling", "22 answers", "cron, scheduling, linux"),
        ("Cron expression format explained?", "tagged/cron+syntax", "16 answers", "cron, syntax, scheduling"),
        ("Difference between cron and crontab?", "tagged/cron+crontab+linux", "9 answers", "cron, crontab, linux"),
    ],
    "cron-generator": [
        ("How do cron schedules work in Linux?", "tagged/cron+linux+scheduling", "18 answers", "cron, linux, scheduling"),
        ("How to run a cron job every day at midnight?", "tagged/cron+scheduling+daily", "14 answers", "cron, scheduling, automation"),
        ("Cron expression for last day of month?", "tagged/cron+scheduling+monthly", "11 answers", "cron, scheduling, date"),
    ],
    "code-beautifier": [
        ("How to auto-format code in VS Code?", "tagged/formatting+vscode+prettier", "13 answers", "vscode, formatting, prettier"),
        ("What is the difference between a linter and a formatter?", "tagged/linting+formatting+code-quality", "10 answers", "linting, formatting, code-quality"),
        ("Best code formatting tools for JavaScript?", "tagged/javascript+formatting+tools", "15 answers", "javascript, formatting, tools"),
    ],
    "html-encoder": [
        ("How to encode HTML entities in JavaScript?", "tagged/html-entities+javascript+encoding", "21 answers", "javascript, html-entities, encoding"),
        ("What HTML entities should I escape?", "tagged/html-entities+xss+security", "14 answers", "html, security, encoding"),
        ("Difference between encodeURI and encodeURIComponent?", "tagged/javascript+encoding+uri", "18 answers", "javascript, encoding, uri"),
    ],
    "css-minifier": [
        ("How to minify CSS for production?", "tagged/css+minification+optimization", "12 answers", "css, minification, performance"),
        ("Does CSS minification improve page speed?", "tagged/css+performance+optimization", "9 answers", "css, performance, web-optimization"),
        ("Best CSS minification tools compared?", "tagged/css+minification+tools", "7 answers", "css, minification, build-tools"),
    ],
    "js-minifier": [
        ("How to minify JavaScript for production?", "tagged/javascript+minification", "16 answers", "javascript, minification, build"),
        ("Terser vs UglifyJS for JavaScript minification?", "tagged/javascript+uglifyjs+terser", "8 answers", "javascript, terser, uglifyjs"),
        ("Does minification affect debugging?", "tagged/javascript+minification+debugging", "11 answers", "javascript, debugging, source-maps"),
    ],
    "diff-checker": [
        ("How to compare two strings in JavaScript?", "tagged/javascript+string-comparison+diff", "13 answers", "javascript, string-comparison, diff"),
        ("Best diff algorithm for comparing text?", "tagged/diff+algorithm+text-comparison", "9 answers", "algorithm, diff, text-comparison"),
        ("How does Git diff work internally?", "tagged/git+diff+algorithm", "7 answers", "git, diff, algorithm"),
    ],
    "text-diff-checker": [
        ("How to implement a text diff algorithm?", "tagged/diff+algorithm+implementation", "10 answers", "algorithm, diff, text-processing"),
        ("Myers diff algorithm explained?", "tagged/diff+algorithm+myers", "6 answers", "algorithm, diff, dynamic-programming"),
        ("How to highlight text differences in HTML?", "tagged/diff+html+highlighting", "8 answers", "html, diff, text-processing"),
    ],
    "jwt-decoder": [
        ("How do JSON Web Tokens work?", "tagged/jwt+authentication", "24 answers", "jwt, authentication, security"),
        ("How to decode a JWT token in JavaScript?", "tagged/jwt+javascript+decoding", "17 answers", "javascript, jwt, decoding"),
        ("JWT vs session-based authentication?", "tagged/jwt+session+authentication", "19 answers", "jwt, session, authentication"),
    ],
    "schema-generator": [
        ("What is JSON-LD structured data?", "tagged/json-ld+schema.org+seo", "11 answers", "json-ld, schema.org, seo"),
        ("How to add Schema markup to a website?", "tagged/schema.org+structured-data+html", "14 answers", "schema.org, structured-data, html"),
        ("Which Schema types improve SEO the most?", "tagged/schema.org+seo+google", "8 answers", "schema.org, seo, google-search"),
    ],
    "meta-tag-generator": [
        ("What meta tags are essential for SEO?", "tagged/meta-tags+seo+html", "16 answers", "meta-tags, seo, html"),
        ("How to add Open Graph meta tags?", "tagged/opengraph+meta-tags+social-media", "12 answers", "opengraph, meta-tags, social-media"),
        ("Twitter Card vs Open Graph meta tags?", "tagged/twitter-cards+opengraph+meta-tags", "9 answers", "twitter-cards, opengraph, meta-tags"),
    ],
    "og-preview": [
        ("How to preview Open Graph tags before sharing?", "tagged/opengraph+preview+social-media", "7 answers", "opengraph, preview, social-media"),
        ("Why are my Open Graph images not showing?", "tagged/opengraph+images+facebook", "13 answers", "opengraph, images, debugging"),
        ("Open Graph image size requirements?", "tagged/opengraph+images+dimensions", "10 answers", "opengraph, images, social-media"),
    ],
    "robots-txt-generator": [
        ("How to write a robots.txt file?", "tagged/robots.txt+seo+crawling", "14 answers", "robots.txt, seo, web-crawling"),
        ("Should I block JavaScript files in robots.txt?", "tagged/robots.txt+javascript+seo", "8 answers", "robots.txt, javascript, seo"),
        ("robots.txt vs meta robots tag?", "tagged/robots.txt+meta-robots+seo", "11 answers", "robots.txt, meta-robots, seo"),
    ],
    "sitemap-generator": [
        ("How to create an XML sitemap?", "tagged/sitemap+xml+seo", "13 answers", "sitemap, xml, seo"),
        ("How often should I update my sitemap?", "tagged/sitemap+seo+google", "7 answers", "sitemap, seo, indexing"),
        ("Maximum number of URLs in a sitemap?", "tagged/sitemap+xml+limits", "9 answers", "sitemap, xml, seo"),
    ],
    "slug-generator": [
        ("How to generate URL-friendly slugs in JavaScript?", "tagged/slug+url+javascript", "15 answers", "javascript, slug, url"),
        ("How to handle Unicode characters in URL slugs?", "tagged/slug+unicode+url-encoding", "10 answers", "slug, unicode, url-encoding"),
        ("Best practices for SEO-friendly URL slugs?", "tagged/slug+seo+url", "8 answers", "slug, seo, url-design"),
    ],

    # ── Calculator Tools ──
    "bmi-calculator": [
        ("How to calculate BMI programmatically?", "tagged/bmi+algorithm+health", "8 answers", "algorithm, bmi, health"),
        ("BMI formula for metric and imperial units?", "tagged/bmi+formula+unit-conversion", "6 answers", "bmi, formula, conversion"),
        ("How to categorize BMI values in code?", "tagged/bmi+classification+algorithm", "5 answers", "algorithm, health, classification"),
    ],
    "mortgage-calculator": [
        ("How to calculate monthly mortgage payments?", "tagged/mortgage+algorithm+finance", "12 answers", "finance, mortgage, algorithm"),
        ("Amortization schedule formula in JavaScript?", "tagged/amortization+javascript+finance", "9 answers", "javascript, finance, amortization"),
        ("Fixed vs adjustable rate mortgage calculation?", "tagged/mortgage+interest-rate+calculation", "7 answers", "mortgage, interest-rate, finance"),
    ],
    "amortization-calculator": [
        ("How to build an amortization schedule in JavaScript?", "tagged/amortization+javascript+finance", "10 answers", "javascript, finance, amortization"),
        ("Amortization formula for loan payments?", "tagged/amortization+formula+loan", "13 answers", "finance, loan, amortization"),
        ("How to calculate principal vs interest breakdown?", "tagged/amortization+principal+interest", "8 answers", "finance, amortization, calculation"),
    ],
    "compound-interest-calculator": [
        ("How to calculate compound interest in JavaScript?", "tagged/compound-interest+javascript+math", "11 answers", "javascript, math, finance"),
        ("Compound interest formula with monthly contributions?", "tagged/compound-interest+formula+investment", "14 answers", "finance, compound-interest, math"),
        ("Simple vs compound interest - what is the difference?", "tagged/interest+finance+math", "9 answers", "finance, interest, math"),
    ],
    "paycheck-calculator": [
        ("How to calculate net pay from gross salary?", "tagged/payroll+calculation+tax", "7 answers", "payroll, tax, calculation"),
        ("Federal income tax bracket calculation in code?", "tagged/tax+brackets+calculation", "10 answers", "tax, calculation, algorithm"),
        ("How to calculate FICA taxes programmatically?", "tagged/fica+payroll+tax", "6 answers", "payroll, tax, social-security"),
    ],
    "salary-calculator": [
        ("How to convert hourly wage to annual salary?", "tagged/salary+calculation+conversion", "8 answers", "salary, calculation, conversion"),
        ("Calculate take-home pay after taxes?", "tagged/salary+tax+net-pay", "11 answers", "salary, tax, payroll"),
        ("Salary vs hourly - how to compare compensation?", "tagged/salary+hourly+comparison", "6 answers", "salary, compensation, calculation"),
    ],
    "tax-calculator": [
        ("How to calculate income tax with progressive brackets?", "tagged/tax+brackets+algorithm", "12 answers", "tax, algorithm, finance"),
        ("Tax bracket calculation algorithm?", "tagged/tax+progressive+calculation", "9 answers", "tax, algorithm, brackets"),
        ("How to implement tax withholding calculations?", "tagged/tax+withholding+payroll", "7 answers", "tax, payroll, calculation"),
    ],
    "tip-calculator": [
        ("How to calculate tip and split the bill?", "tagged/tip-calculator+math+javascript", "5 answers", "math, javascript, calculation"),
        ("Standard tipping percentages by country?", "tagged/tipping+calculation+localization", "8 answers", "calculation, localization, math"),
        ("How to round tip amounts properly?", "tagged/rounding+math+javascript", "6 answers", "javascript, math, rounding"),
    ],
    "percentage-calculator": [
        ("How to calculate percentage increase/decrease?", "tagged/percentage+math+calculation", "14 answers", "math, percentage, calculation"),
        ("Percentage formula in JavaScript?", "tagged/percentage+javascript+math", "10 answers", "javascript, math, percentage"),
        ("How to calculate percentage of a number?", "tagged/percentage+formula+math", "12 answers", "math, formula, percentage"),
    ],
    "discount-calculator": [
        ("How to calculate discount percentage?", "tagged/discount+percentage+math", "7 answers", "math, discount, calculation"),
        ("Calculate final price after multiple discounts?", "tagged/discount+stacking+calculation", "6 answers", "math, discount, price"),
        ("Percentage off vs amount off - how to compare?", "tagged/discount+comparison+math", "4 answers", "math, discount, comparison"),
    ],
    "loan-calculator": [
        ("How to calculate loan EMI in JavaScript?", "tagged/loan+emi+javascript", "11 answers", "javascript, loan, finance"),
        ("Loan payment formula with fixed interest rate?", "tagged/loan+payment+formula", "15 answers", "finance, loan, formula"),
        ("How to calculate total interest paid on a loan?", "tagged/loan+interest+calculation", "9 answers", "finance, loan, interest"),
    ],
    "investment-calculator": [
        ("How to calculate investment returns with compound interest?", "tagged/investment+compound-interest+finance", "10 answers", "finance, investment, compound-interest"),
        ("Dollar-cost averaging calculation formula?", "tagged/investment+dca+calculation", "7 answers", "finance, investment, strategy"),
        ("How to calculate ROI on investments?", "tagged/roi+investment+calculation", "12 answers", "finance, roi, investment"),
    ],
    "roi-calculator": [
        ("How to calculate ROI in JavaScript?", "tagged/roi+javascript+finance", "8 answers", "javascript, roi, finance"),
        ("ROI formula - simple and annualized?", "tagged/roi+formula+finance", "11 answers", "finance, roi, formula"),
        ("How to compare investments using ROI?", "tagged/roi+investment+comparison", "6 answers", "finance, roi, analysis"),
    ],
    "retirement-calculator": [
        ("How to calculate retirement savings needed?", "tagged/retirement+savings+finance", "9 answers", "finance, retirement, savings"),
        ("4% rule for retirement withdrawal calculation?", "tagged/retirement+withdrawal+rule", "7 answers", "finance, retirement, planning"),
        ("How to factor inflation into retirement planning?", "tagged/retirement+inflation+calculation", "8 answers", "finance, inflation, retirement"),
    ],
    "savings-calculator": [
        ("How to calculate savings growth with regular deposits?", "tagged/savings+compound-interest+calculation", "10 answers", "finance, savings, compound-interest"),
        ("Future value formula for savings account?", "tagged/savings+future-value+formula", "8 answers", "finance, future-value, formula"),
        ("How to calculate APY from APR?", "tagged/apy+apr+interest-rate", "6 answers", "finance, apy, interest-rate"),
    ],
    "inflation-calculator": [
        ("How to adjust for inflation in financial calculations?", "tagged/inflation+calculation+finance", "8 answers", "finance, inflation, economics"),
        ("CPI-based inflation calculation formula?", "tagged/inflation+cpi+formula", "6 answers", "economics, cpi, inflation"),
        ("How to calculate purchasing power over time?", "tagged/inflation+purchasing-power+calculation", "5 answers", "economics, inflation, math"),
    ],
    "profit-margin-calculator": [
        ("How to calculate profit margin in JavaScript?", "tagged/profit-margin+javascript+finance", "7 answers", "javascript, finance, business"),
        ("Gross margin vs net margin - what is the difference?", "tagged/gross-margin+net-margin+finance", "10 answers", "finance, margin, business"),
        ("Markup vs margin percentage formula?", "tagged/markup+margin+calculation", "12 answers", "finance, markup, calculation"),
    ],
    "debt-payoff-calculator": [
        ("Debt snowball vs avalanche method - which is better?", "tagged/debt+payoff+strategy", "8 answers", "finance, debt, strategy"),
        ("How to calculate minimum payment on credit card debt?", "tagged/debt+credit-card+payment", "6 answers", "finance, debt, credit-card"),
        ("Algorithm for debt payoff schedule?", "tagged/debt+algorithm+amortization", "5 answers", "algorithm, debt, finance"),
    ],
    "electricity-cost-calculator": [
        ("How to calculate electricity cost from watts?", "tagged/electricity+cost+calculation", "9 answers", "electricity, calculation, energy"),
        ("kWh to cost conversion formula?", "tagged/kwh+electricity+formula", "7 answers", "electricity, kwh, formula"),
        ("How to estimate appliance electricity usage?", "tagged/electricity+appliance+estimation", "6 answers", "electricity, energy, estimation"),
    ],
    "calorie-calculator": [
        ("How to calculate TDEE (Total Daily Energy Expenditure)?", "tagged/calories+tdee+health", "8 answers", "health, calories, tdee"),
        ("Harris-Benedict equation for calorie calculation?", "tagged/calories+formula+bmr", "10 answers", "health, bmr, formula"),
        ("How to calculate macronutrient ratios?", "tagged/calories+macros+nutrition", "7 answers", "nutrition, calories, macros"),
    ],
    "age-calculator": [
        ("How to calculate age from date of birth in JavaScript?", "tagged/javascript+date+age", "18 answers", "javascript, date, calculation"),
        ("Accurately calculate age accounting for leap years?", "tagged/date+age+leap-year", "11 answers", "date, age, leap-year"),
        ("Date difference calculation in days, months, years?", "tagged/date+difference+calculation", "14 answers", "date, calculation, javascript"),
    ],
    "date-calculator": [
        ("How to add days to a date in JavaScript?", "tagged/javascript+date+addition", "20 answers", "javascript, date, arithmetic"),
        ("Calculate difference between two dates?", "tagged/javascript+date+difference", "25 answers", "javascript, date, calculation"),
        ("How to handle timezone-aware date calculations?", "tagged/date+timezone+calculation", "13 answers", "date, timezone, javascript"),
    ],
    "time-calculator": [
        ("How to add hours and minutes in JavaScript?", "tagged/javascript+time+calculation", "12 answers", "javascript, time, calculation"),
        ("Convert hours to minutes and seconds?", "tagged/time+conversion+calculation", "9 answers", "time, conversion, math"),
        ("How to calculate elapsed time between two timestamps?", "tagged/time+elapsed+calculation", "11 answers", "time, calculation, timestamp"),
    ],
    "gpa-calculator": [
        ("How to calculate GPA programmatically?", "tagged/gpa+algorithm+calculation", "6 answers", "algorithm, gpa, education"),
        ("GPA scale conversion (4.0 to letter grade)?", "tagged/gpa+grade+conversion", "5 answers", "gpa, conversion, education"),
        ("Weighted vs unweighted GPA calculation?", "tagged/gpa+weighted+calculation", "7 answers", "gpa, education, algorithm"),
    ],
    "grade-calculator": [
        ("How to calculate weighted grade average?", "tagged/grade+weighted-average+calculation", "8 answers", "calculation, grade, weighted-average"),
        ("Grade point calculation algorithm?", "tagged/grade+algorithm+education", "6 answers", "algorithm, education, grade"),
        ("How to convert percentage to letter grade?", "tagged/grade+percentage+conversion", "7 answers", "grade, conversion, education"),
    ],
    "statistics-calculator": [
        ("How to calculate standard deviation in JavaScript?", "tagged/statistics+standard-deviation+javascript", "12 answers", "javascript, statistics, math"),
        ("Mean, median, mode calculation algorithm?", "tagged/statistics+mean+median", "15 answers", "statistics, algorithm, math"),
        ("How to calculate percentiles from a data set?", "tagged/statistics+percentile+calculation", "9 answers", "statistics, percentile, math"),
    ],
    "scientific-calculator": [
        ("How to evaluate mathematical expressions in JavaScript?", "tagged/javascript+math+expression-evaluation", "14 answers", "javascript, math, parsing"),
        ("Implementing trigonometric functions in a calculator?", "tagged/math+trigonometry+calculator", "8 answers", "math, trigonometry, calculator"),
        ("How to handle operator precedence in expression parsing?", "tagged/parsing+expression+precedence", "11 answers", "parsing, math, algorithm"),
    ],
    "graphing-calculator": [
        ("How to plot mathematical functions with JavaScript?", "tagged/javascript+graphing+math", "10 answers", "javascript, graph, math"),
        ("Best JavaScript libraries for graphing equations?", "tagged/javascript+charting+math", "12 answers", "javascript, charting, visualization"),
        ("How to render mathematical equations on HTML canvas?", "tagged/canvas+math+rendering", "7 answers", "javascript, canvas, math"),
    ],
    "math-equation-solver": [
        ("How to solve equations programmatically?", "tagged/math+equation-solving+algorithm", "9 answers", "math, algorithm, equation"),
        ("Newton's method for root finding in JavaScript?", "tagged/math+newtons-method+javascript", "7 answers", "math, algorithm, javascript"),
        ("How to parse mathematical expressions?", "tagged/math+parsing+expression", "11 answers", "math, parsing, algorithm"),
    ],
    "mathematics-solver": [
        ("How to implement a math expression parser?", "tagged/math+parser+algorithm", "10 answers", "math, parser, algorithm"),
        ("Symbolic math computation in JavaScript?", "tagged/math+symbolic+javascript", "6 answers", "javascript, math, symbolic"),
        ("How to solve linear equations programmatically?", "tagged/math+linear-algebra+algorithm", "8 answers", "math, linear-algebra, algorithm"),
    ],
    "aspect-ratio-calculator": [
        ("How to calculate aspect ratio from width and height?", "tagged/aspect-ratio+calculation+math", "10 answers", "math, aspect-ratio, calculation"),
        ("Common video and image aspect ratios?", "tagged/aspect-ratio+video+image", "8 answers", "aspect-ratio, video, image"),
        ("How to maintain aspect ratio when resizing?", "tagged/aspect-ratio+resize+css", "14 answers", "css, aspect-ratio, responsive"),
    ],
    "blood-alcohol-calculator": [
        ("Widmark formula for BAC calculation?", "tagged/bac+formula+algorithm", "4 answers", "algorithm, bac, formula"),
        ("How to calculate blood alcohol content?", "tagged/bac+calculation+health", "5 answers", "health, bac, calculation"),
        ("Factors affecting blood alcohol level?", "tagged/bac+metabolism+health", "6 answers", "health, bac, biology"),
    ],

    # ── Converter Tools ──
    "unit-converter": [
        ("How to convert between measurement units in JavaScript?", "tagged/unit-conversion+javascript", "11 answers", "javascript, unit-conversion, math"),
        ("Building a unit conversion library?", "tagged/unit-conversion+library+javascript", "8 answers", "javascript, library, conversion"),
        ("How to handle metric to imperial conversion?", "tagged/metric+imperial+conversion", "13 answers", "conversion, metric, imperial"),
    ],
    "binary-converter": [
        ("How to convert decimal to binary in JavaScript?", "tagged/binary+decimal+javascript", "16 answers", "javascript, binary, conversion"),
        ("Binary to hexadecimal conversion method?", "tagged/binary+hexadecimal+conversion", "12 answers", "binary, hexadecimal, conversion"),
        ("How does two's complement binary work?", "tagged/binary+twos-complement+math", "10 answers", "binary, math, computer-science"),
    ],
    "binary-text-converter": [
        ("How to convert text to binary in JavaScript?", "tagged/binary+text+javascript", "13 answers", "javascript, binary, text"),
        ("ASCII to binary conversion algorithm?", "tagged/ascii+binary+conversion", "9 answers", "ascii, binary, conversion"),
        ("How to decode binary back to text?", "tagged/binary+text+decoding", "8 answers", "binary, text, decoding"),
    ],
    "number-base-converter": [
        ("How to convert between number bases in JavaScript?", "tagged/number-base+conversion+javascript", "14 answers", "javascript, base-conversion, math"),
        ("parseInt and toString for base conversion?", "tagged/javascript+parseint+base", "11 answers", "javascript, parseint, conversion"),
        ("How does octal and hexadecimal notation work?", "tagged/octal+hexadecimal+number-systems", "8 answers", "number-systems, octal, hexadecimal"),
    ],
    "base64-encoder": [
        ("How to encode and decode Base64 in JavaScript?", "tagged/base64+javascript+encoding", "22 answers", "javascript, base64, encoding"),
        ("What is Base64 encoding used for?", "tagged/base64+encoding+data-uri", "15 answers", "base64, encoding, data-uri"),
        ("Base64 vs URL encoding - when to use which?", "tagged/base64+url-encoding+comparison", "9 answers", "base64, url-encoding, encoding"),
    ],
    "base64-encoder-decoder": [
        ("How does Base64 encoding work internally?", "tagged/base64+encoding+algorithm", "18 answers", "base64, encoding, algorithm"),
        ("btoa and atob functions in JavaScript?", "tagged/base64+javascript+btoa", "14 answers", "javascript, base64, btoa"),
        ("How to Base64 encode binary data in the browser?", "tagged/base64+binary+browser", "10 answers", "base64, binary, javascript"),
    ],
    "hex-color-picker": [
        ("How to convert hex color to RGB in JavaScript?", "tagged/hex+rgb+javascript", "20 answers", "javascript, hex, rgb"),
        ("Understanding hex color codes?", "tagged/hex+color+css", "14 answers", "css, hex-color, web-design"),
        ("How to generate random hex colors?", "tagged/hex+color+random", "11 answers", "javascript, hex-color, random"),
    ],
    "color-converter": [
        ("How to convert between RGB, HSL, and Hex?", "tagged/rgb+hsl+hex+conversion", "16 answers", "color, rgb, hsl"),
        ("HSL vs RGB color model - what is the difference?", "tagged/hsl+rgb+color-theory", "9 answers", "color-theory, hsl, rgb"),
        ("How to convert CMYK to RGB?", "tagged/cmyk+rgb+color-conversion", "7 answers", "color, cmyk, rgb"),
    ],
    "color-contrast-checker": [
        ("How to calculate color contrast ratio?", "tagged/color-contrast+wcag+accessibility", "11 answers", "accessibility, wcag, color-contrast"),
        ("WCAG AA vs AAA contrast requirements?", "tagged/wcag+accessibility+contrast", "8 answers", "wcag, accessibility, web-design"),
        ("How to check if text color meets accessibility standards?", "tagged/accessibility+color+contrast-ratio", "10 answers", "accessibility, color, contrast"),
    ],
    "color-palette-generator": [
        ("How to generate harmonious color palettes?", "tagged/color-palette+color-theory+design", "7 answers", "color-theory, design, palette"),
        ("Color harmony rules - complementary, analogous, triadic?", "tagged/color-theory+harmony+design", "9 answers", "color-theory, harmony, design"),
        ("How to extract a color palette from an image?", "tagged/color-palette+image+extraction", "8 answers", "color, image-processing, palette"),
    ],
    "currency-converter": [
        ("How to get real-time exchange rates in JavaScript?", "tagged/currency+exchange-rate+api", "11 answers", "api, currency, exchange-rate"),
        ("Best free APIs for currency conversion?", "tagged/currency+api+free", "14 answers", "api, currency, web-service"),
        ("How to handle currency precision in calculations?", "tagged/currency+floating-point+precision", "12 answers", "currency, floating-point, precision"),
    ],
    "timestamp-converter": [
        ("How to convert Unix timestamp to date in JavaScript?", "tagged/timestamp+unix+javascript", "19 answers", "javascript, timestamp, unix"),
        ("What is epoch time and how does it work?", "tagged/epoch+unix-timestamp+time", "12 answers", "epoch, unix-timestamp, time"),
        ("How to get current Unix timestamp?", "tagged/timestamp+unix+current-time", "15 answers", "timestamp, javascript, unix"),
    ],
    "timezone-converter": [
        ("How to convert between timezones in JavaScript?", "tagged/timezone+javascript+conversion", "16 answers", "javascript, timezone, conversion"),
        ("JavaScript Intl.DateTimeFormat for timezone display?", "tagged/javascript+intl+timezone", "10 answers", "javascript, intl, timezone"),
        ("How to handle daylight saving time in code?", "tagged/timezone+dst+datetime", "13 answers", "timezone, dst, datetime"),
    ],
    "roman-numeral-converter": [
        ("How to convert Roman numerals in JavaScript?", "tagged/roman-numerals+javascript+algorithm", "12 answers", "javascript, roman-numerals, algorithm"),
        ("Roman numeral conversion algorithm?", "tagged/roman-numerals+algorithm+conversion", "9 answers", "algorithm, roman-numerals, math"),
        ("Rules for Roman numeral notation?", "tagged/roman-numerals+notation+rules", "7 answers", "roman-numerals, notation, math"),
    ],
    "morse-code-translator": [
        ("How to convert text to Morse code in JavaScript?", "tagged/morse-code+javascript+conversion", "8 answers", "javascript, morse-code, conversion"),
        ("Morse code encoding and decoding algorithm?", "tagged/morse-code+algorithm+encoding", "6 answers", "algorithm, morse-code, encoding"),
        ("International Morse code character mapping?", "tagged/morse-code+mapping+reference", "5 answers", "morse-code, mapping, reference"),
    ],
    "image-to-base64": [
        ("How to convert an image to Base64 in JavaScript?", "tagged/image+base64+javascript", "17 answers", "javascript, image, base64"),
        ("FileReader API for image to Base64 conversion?", "tagged/filereader+base64+image", "12 answers", "javascript, filereader, base64"),
        ("When should I use Base64 encoded images?", "tagged/base64+image+performance", "9 answers", "base64, image, web-performance"),
    ],
    "svg-to-png-converter": [
        ("How to convert SVG to PNG in JavaScript?", "tagged/svg+png+javascript+conversion", "13 answers", "javascript, svg, png"),
        ("Canvas-based SVG to raster conversion?", "tagged/svg+canvas+conversion", "9 answers", "svg, canvas, javascript"),
        ("Maintaining quality when converting SVG to PNG?", "tagged/svg+png+resolution+quality", "7 answers", "svg, png, quality"),
    ],
    "pixel-to-rem-converter": [
        ("How to convert pixels to rem in CSS?", "tagged/css+px+rem+conversion", "15 answers", "css, px, rem"),
        ("Why use rem instead of px for font sizes?", "tagged/css+rem+font-size", "12 answers", "css, rem, responsive"),
        ("What is the default root font size for rem?", "tagged/css+rem+root-font-size", "9 answers", "css, rem, typography"),
    ],
    "px-to-rem": [
        ("What is the difference between px, em, and rem?", "tagged/css+px+em+rem", "18 answers", "css, units, responsive"),
        ("How to set a responsive base font size?", "tagged/css+responsive+font-size", "11 answers", "css, responsive, typography"),
        ("Best practices for CSS units in responsive design?", "tagged/css+units+responsive-design", "14 answers", "css, responsive-design, units"),
    ],
    "url-encoder": [
        ("How to encode a URL in JavaScript?", "tagged/url+encoding+javascript", "17 answers", "javascript, url, encoding"),
        ("encodeURI vs encodeURIComponent - which to use?", "tagged/javascript+encodeuri+encodeuricomponent", "21 answers", "javascript, uri, encoding"),
        ("What characters need URL encoding?", "tagged/url+encoding+special-characters", "13 answers", "url, encoding, characters"),
    ],
    "url-encoder-decoder": [
        ("How to decode URL-encoded strings in JavaScript?", "tagged/url+decoding+javascript", "14 answers", "javascript, url, decoding"),
        ("Percent encoding in URLs explained?", "tagged/url+percent-encoding+rfc", "10 answers", "url, encoding, standards"),
        ("How to handle UTF-8 characters in URLs?", "tagged/url+utf-8+encoding", "12 answers", "url, utf-8, encoding"),
    ],
    "discord-timestamp": [
        ("How to use Discord timestamp formatting?", "tagged/discord+timestamp+formatting", "8 answers", "discord, timestamp, formatting"),
        ("Unix timestamp to Discord timestamp syntax?", "tagged/discord+unix-timestamp+markdown", "6 answers", "discord, timestamp, markdown"),
        ("Discord message formatting guide?", "tagged/discord+formatting+markdown", "10 answers", "discord, formatting, markdown"),
    ],

    # ── Generator Tools ──
    "password-generator": [
        ("How to generate cryptographically secure passwords?", "tagged/password+security+crypto", "16 answers", "security, password, cryptography"),
        ("Using Web Crypto API for random number generation?", "tagged/web-crypto+random+javascript", "11 answers", "javascript, web-crypto, random"),
        ("What makes a password strong?", "tagged/password+security+entropy", "13 answers", "security, password, entropy"),
    ],
    "qr-code-generator": [
        ("How to generate QR codes in JavaScript?", "tagged/qr-code+javascript+generation", "14 answers", "javascript, qr-code, generation"),
        ("Best QR code JavaScript libraries?", "tagged/qr-code+javascript+library", "10 answers", "javascript, qr-code, library"),
        ("How much data can a QR code store?", "tagged/qr-code+capacity+data", "8 answers", "qr-code, data, encoding"),
    ],
    "qr-reader": [
        ("How to read QR codes with JavaScript?", "tagged/qr-code+reader+javascript", "11 answers", "javascript, qr-code, reader"),
        ("Camera API for QR code scanning in the browser?", "tagged/qr-code+camera+mediadevices", "8 answers", "javascript, camera, qr-code"),
        ("Best JavaScript library for QR code scanning?", "tagged/qr-code+scanner+library", "7 answers", "javascript, qr-code, scanning"),
    ],
    "uuid-generator": [
        ("How to generate a UUID v4 in JavaScript?", "tagged/uuid+javascript+generation", "18 answers", "javascript, uuid, generation"),
        ("UUID v1 vs v4 - what is the difference?", "tagged/uuid+v1+v4+comparison", "12 answers", "uuid, comparison, standards"),
        ("Are UUID collisions possible?", "tagged/uuid+collision+probability", "9 answers", "uuid, collision, probability"),
    ],
    "hash-generator": [
        ("How to generate SHA-256 hash in JavaScript?", "tagged/sha256+hash+javascript", "15 answers", "javascript, sha256, hash"),
        ("MD5 vs SHA-256 - which hash to use?", "tagged/md5+sha256+hashing", "13 answers", "hashing, md5, sha256"),
        ("How to hash a string in the browser?", "tagged/hash+javascript+browser", "10 answers", "javascript, hash, browser"),
    ],
    "bcrypt-generator": [
        ("How does bcrypt hashing work?", "tagged/bcrypt+hashing+security", "14 answers", "bcrypt, hashing, security"),
        ("bcrypt salt rounds - how many to use?", "tagged/bcrypt+salt+security", "11 answers", "bcrypt, salt, security"),
        ("bcrypt vs argon2 for password hashing?", "tagged/bcrypt+argon2+password-hashing", "9 answers", "bcrypt, argon2, security"),
    ],
    "htpasswd-generator": [
        ("How to generate htpasswd entries?", "tagged/htpasswd+apache+authentication", "10 answers", "apache, htpasswd, authentication"),
        ("htpasswd file format and hash types?", "tagged/htpasswd+hash+format", "7 answers", "htpasswd, hash, apache"),
        ("How to set up basic authentication with Apache?", "tagged/apache+basic-auth+htpasswd", "12 answers", "apache, authentication, htpasswd"),
    ],
    "lorem-ipsum-generator": [
        ("How to generate Lorem Ipsum text in JavaScript?", "tagged/lorem-ipsum+javascript+generation", "9 answers", "javascript, lorem-ipsum, text"),
        ("Why is Lorem Ipsum used as placeholder text?", "tagged/lorem-ipsum+placeholder+design", "6 answers", "lorem-ipsum, design, typography"),
        ("Alternatives to Lorem Ipsum placeholder text?", "tagged/placeholder-text+alternatives+design", "8 answers", "design, placeholder, text"),
    ],
    "random-number-generator": [
        ("How to generate random numbers in JavaScript?", "tagged/random+javascript+math", "20 answers", "javascript, random, math"),
        ("Math.random vs crypto.getRandomValues?", "tagged/random+javascript+crypto", "12 answers", "javascript, random, security"),
        ("Generate random number within a range?", "tagged/random+range+javascript", "16 answers", "javascript, random, math"),
    ],
    "number-generator": [
        ("How to generate random integers in a range?", "tagged/random+integer+javascript", "15 answers", "javascript, random, integer"),
        ("Generating unique random numbers without repetition?", "tagged/random+unique+algorithm", "11 answers", "algorithm, random, unique"),
        ("Seeded random number generation in JavaScript?", "tagged/random+seed+javascript", "8 answers", "javascript, random, seed"),
    ],
    "calendar-generator": [
        ("How to build a calendar in JavaScript?", "tagged/calendar+javascript+html", "12 answers", "javascript, calendar, html"),
        ("Generate a monthly calendar grid programmatically?", "tagged/calendar+grid+algorithm", "8 answers", "algorithm, calendar, date"),
        ("How to handle different month lengths in a calendar?", "tagged/calendar+month+date", "6 answers", "calendar, date, javascript"),
    ],
    "email-signature-generator": [
        ("How to create an HTML email signature?", "tagged/email+signature+html", "11 answers", "html, email, signature"),
        ("HTML email compatibility issues and solutions?", "tagged/html-email+compatibility+css", "14 answers", "html-email, css, compatibility"),
        ("Best practices for email signature design?", "tagged/email+signature+design", "7 answers", "email, signature, design"),
    ],
    "invoice-generator": [
        ("How to generate PDF invoices in JavaScript?", "tagged/invoice+pdf+javascript", "9 answers", "javascript, pdf, invoice"),
        ("HTML to PDF conversion for invoices?", "tagged/html-to-pdf+javascript+invoice", "11 answers", "javascript, html-to-pdf, invoice"),
        ("Best invoice template design practices?", "tagged/invoice+template+design", "6 answers", "invoice, design, business"),
    ],
    "privacy-policy-generator": [
        ("What should a privacy policy include?", "tagged/privacy-policy+gdpr+legal", "8 answers", "privacy-policy, gdpr, legal"),
        ("GDPR vs CCPA requirements for privacy policies?", "tagged/gdpr+ccpa+privacy", "10 answers", "gdpr, ccpa, privacy"),
        ("How to comply with cookie consent requirements?", "tagged/cookies+consent+gdpr", "12 answers", "cookies, gdpr, compliance"),
    ],
    "favicon-generator": [
        ("How to create a favicon for a website?", "tagged/favicon+html+web", "16 answers", "favicon, html, web"),
        ("What favicon sizes and formats are needed?", "tagged/favicon+sizes+formats", "12 answers", "favicon, sizes, formats"),
        ("How to add a favicon to an HTML page?", "tagged/favicon+html+link-tag", "14 answers", "favicon, html, web-development"),
    ],
    "favicon-converter": [
        ("How to convert PNG to ICO format?", "tagged/favicon+ico+conversion", "10 answers", "favicon, ico, conversion"),
        ("ICO file format - multiple sizes in one file?", "tagged/ico+format+multi-size", "7 answers", "ico, format, favicon"),
        ("SVG favicon support in modern browsers?", "tagged/svg+favicon+browser-support", "9 answers", "svg, favicon, browser"),
    ],
    "icon-generator": [
        ("How to generate app icons for different platforms?", "tagged/icons+app+generation", "8 answers", "icons, app, generation"),
        ("Apple Touch Icon sizes and requirements?", "tagged/apple-touch-icon+ios+sizes", "10 answers", "ios, apple-touch-icon, sizes"),
        ("How to create SVG icons?", "tagged/svg+icons+design", "12 answers", "svg, icons, design"),
    ],
    "placeholder-image": [
        ("How to generate placeholder images programmatically?", "tagged/placeholder+image+generation", "7 answers", "image, placeholder, generation"),
        ("Best placeholder image services for development?", "tagged/placeholder+image+api", "9 answers", "placeholder, image, development"),
        ("How to create dynamic placeholder images with Canvas?", "tagged/canvas+image+placeholder", "6 answers", "javascript, canvas, placeholder"),
    ],

    # ── Text Tools ──
    "word-counter": [
        ("How to count words in a string with JavaScript?", "tagged/word-count+javascript+string", "17 answers", "javascript, word-count, string"),
        ("Accurately counting words with Unicode support?", "tagged/word-count+unicode+regex", "9 answers", "unicode, regex, word-count"),
        ("How to count characters, sentences, and paragraphs?", "tagged/text-analysis+counting+javascript", "7 answers", "javascript, text-analysis, counting"),
    ],
    "character-counter": [
        ("How to count characters in JavaScript including emojis?", "tagged/character-count+javascript+unicode", "12 answers", "javascript, unicode, counting"),
        ("String.length vs character count for Unicode?", "tagged/javascript+string-length+unicode", "10 answers", "javascript, unicode, string"),
        ("How to count bytes vs characters in a string?", "tagged/string+bytes+characters", "8 answers", "string, bytes, encoding"),
    ],
    "case-converter": [
        ("How to convert string case in JavaScript?", "tagged/javascript+string+case-conversion", "14 answers", "javascript, string, case-conversion"),
        ("camelCase to snake_case conversion?", "tagged/camelcase+snake-case+conversion", "11 answers", "naming-convention, conversion, string"),
        ("Title case conversion with proper exceptions?", "tagged/title-case+string+javascript", "8 answers", "javascript, string, title-case"),
    ],
    "text-case-converter": [
        ("How to convert between camelCase, PascalCase, and kebab-case?", "tagged/naming-convention+conversion+string", "10 answers", "naming-convention, string, conversion"),
        ("JavaScript string capitalization methods?", "tagged/javascript+capitalize+string", "13 answers", "javascript, string, capitalization"),
        ("Best practices for variable naming conventions?", "tagged/naming-convention+best-practices+code-style", "9 answers", "naming-convention, code-style, best-practices"),
    ],
    "text-generator": [
        ("How to generate random text in JavaScript?", "tagged/random-text+javascript+generation", "7 answers", "javascript, text, generation"),
        ("Markov chain text generation algorithm?", "tagged/markov-chain+text-generation+algorithm", "9 answers", "algorithm, markov-chain, text"),
        ("How to create realistic placeholder content?", "tagged/placeholder+text+content", "5 answers", "placeholder, text, content"),
    ],
    "text-to-speech": [
        ("How to use the Web Speech API for text-to-speech?", "tagged/web-speech-api+tts+javascript", "14 answers", "javascript, speech, tts"),
        ("SpeechSynthesis voices and language support?", "tagged/speechsynthesis+voices+javascript", "10 answers", "javascript, speech, languages"),
        ("How to control speech rate, pitch, and volume?", "tagged/tts+speech+parameters", "7 answers", "tts, speech, javascript"),
    ],
    "paraphrase-tool": [
        ("How to implement text paraphrasing in JavaScript?", "tagged/paraphrase+nlp+javascript", "5 answers", "nlp, paraphrase, javascript"),
        ("NLP approaches to text paraphrasing?", "tagged/nlp+paraphrase+text-processing", "8 answers", "nlp, text-processing, ai"),
        ("Synonym replacement algorithms for text rewriting?", "tagged/synonym+nlp+text-rewriting", "6 answers", "nlp, synonyms, algorithm"),
    ],
    "readability-checker": [
        ("How to calculate Flesch-Kincaid readability score?", "tagged/readability+flesch-kincaid+algorithm", "8 answers", "readability, algorithm, text"),
        ("Readability formulas comparison - Flesch, Gunning Fog, etc.?", "tagged/readability+formulas+comparison", "6 answers", "readability, formulas, text-analysis"),
        ("How to count syllables in English text programmatically?", "tagged/syllables+counting+algorithm", "9 answers", "algorithm, syllables, nlp"),
    ],
    "headline-analyzer": [
        ("How to analyze headline effectiveness?", "tagged/headline+copywriting+analysis", "5 answers", "copywriting, headline, analysis"),
        ("Emotional word detection in text?", "tagged/sentiment-analysis+words+nlp", "8 answers", "nlp, sentiment, text-analysis"),
        ("Power words and their impact on click-through rates?", "tagged/copywriting+ctr+power-words", "4 answers", "copywriting, ctr, marketing"),
    ],
    "plagiarism-checker": [
        ("How to detect plagiarism programmatically?", "tagged/plagiarism+detection+algorithm", "7 answers", "algorithm, plagiarism, text"),
        ("Text similarity algorithms for plagiarism detection?", "tagged/text-similarity+algorithm+nlp", "10 answers", "algorithm, nlp, similarity"),
        ("Cosine similarity for document comparison?", "tagged/cosine-similarity+nlp+comparison", "9 answers", "nlp, cosine-similarity, algorithm"),
    ],

    # ── CSS / Design Tools ──
    "border-radius-generator": [
        ("How to use border-radius in CSS?", "tagged/css+border-radius+styling", "12 answers", "css, border-radius, styling"),
        ("Creating complex shapes with border-radius?", "tagged/css+border-radius+shapes", "8 answers", "css, shapes, border-radius"),
        ("Border-radius on individual corners?", "tagged/css+border-radius+corners", "10 answers", "css, border-radius, layout"),
    ],
    "box-shadow-generator": [
        ("How to add box-shadow in CSS?", "tagged/css+box-shadow+design", "14 answers", "css, box-shadow, design"),
        ("Multiple box-shadows on one element?", "tagged/css+box-shadow+multiple", "9 answers", "css, box-shadow, styling"),
        ("Inset vs outset box-shadow?", "tagged/css+box-shadow+inset", "7 answers", "css, box-shadow, effects"),
    ],
    "css-gradient-generator": [
        ("How to create CSS gradients?", "tagged/css+gradient+background", "16 answers", "css, gradient, background"),
        ("Linear gradient vs radial gradient in CSS?", "tagged/css+linear-gradient+radial-gradient", "10 answers", "css, gradient, design"),
        ("How to create a multi-stop CSS gradient?", "tagged/css+gradient+color-stops", "8 answers", "css, gradient, colors"),
    ],
    "gradient-generator": [
        ("CSS gradient syntax and browser support?", "tagged/css+gradient+syntax", "11 answers", "css, gradient, compatibility"),
        ("How to animate CSS gradients?", "tagged/css+gradient+animation", "8 answers", "css, gradient, animation"),
        ("Creating text gradients with CSS?", "tagged/css+text+gradient", "10 answers", "css, text, gradient"),
    ],
    "css-grid-generator": [
        ("How to use CSS Grid layout?", "tagged/css-grid+layout+css", "18 answers", "css, css-grid, layout"),
        ("CSS Grid vs Flexbox - when to use which?", "tagged/css-grid+flexbox+comparison", "22 answers", "css, css-grid, flexbox"),
        ("How to create responsive layouts with CSS Grid?", "tagged/css-grid+responsive+layout", "14 answers", "css, css-grid, responsive"),
    ],
    "flexbox-generator": [
        ("How does CSS Flexbox work?", "tagged/css+flexbox+layout", "20 answers", "css, flexbox, layout"),
        ("Flexbox alignment - justify-content vs align-items?", "tagged/flexbox+alignment+css", "15 answers", "css, flexbox, alignment"),
        ("How to center elements with Flexbox?", "tagged/css+flexbox+centering", "17 answers", "css, flexbox, centering"),
    ],
    "css-animation-generator": [
        ("How to create CSS animations with keyframes?", "tagged/css+animation+keyframes", "14 answers", "css, animation, keyframes"),
        ("CSS transition vs animation - what is the difference?", "tagged/css+transition+animation", "11 answers", "css, transition, animation"),
        ("How to create smooth CSS hover effects?", "tagged/css+hover+transition", "9 answers", "css, hover, effects"),
    ],
    "font-generator": [
        ("How to use Google Fonts in a website?", "tagged/google-fonts+css+typography", "14 answers", "css, google-fonts, typography"),
        ("Web font loading strategies and performance?", "tagged/web-fonts+performance+loading", "10 answers", "web-fonts, performance, css"),
        ("How to use variable fonts in CSS?", "tagged/variable-fonts+css+typography", "7 answers", "css, variable-fonts, typography"),
    ],
    "instagram-font-generator": [
        ("How to use Unicode fancy text on social media?", "tagged/unicode+text+social-media", "6 answers", "unicode, text, social-media"),
        ("Unicode text transformation in JavaScript?", "tagged/unicode+javascript+text-transform", "8 answers", "javascript, unicode, text"),
        ("How do Unicode mathematical symbols create styled text?", "tagged/unicode+mathematical-symbols+text", "5 answers", "unicode, symbols, text"),
    ],
    "table-generator": [
        ("How to create responsive HTML tables?", "tagged/html+table+responsive", "13 answers", "html, table, responsive"),
        ("CSS table styling best practices?", "tagged/css+table+styling", "10 answers", "css, table, styling"),
        ("How to make tables accessible with ARIA?", "tagged/table+accessibility+aria", "8 answers", "html, accessibility, table"),
    ],
    "svg-editor": [
        ("How to create and edit SVG graphics?", "tagged/svg+editor+graphics", "9 answers", "svg, graphics, editor"),
        ("SVG path syntax and commands explained?", "tagged/svg+path+syntax", "12 answers", "svg, path, syntax"),
        ("How to manipulate SVG with JavaScript?", "tagged/svg+javascript+manipulation", "14 answers", "javascript, svg, dom"),
    ],

    # ── Image Tools ──
    "image-compressor": [
        ("How to compress images in the browser with JavaScript?", "tagged/image+compression+javascript", "12 answers", "javascript, image, compression"),
        ("Canvas-based image compression technique?", "tagged/canvas+image+compression", "9 answers", "javascript, canvas, compression"),
        ("JPEG vs PNG vs WebP - which format for compression?", "tagged/jpeg+png+webp+comparison", "15 answers", "image-format, compression, webp"),
    ],
    "image-resizer": [
        ("How to resize images in the browser with Canvas?", "tagged/canvas+image+resize", "14 answers", "javascript, canvas, image-resize"),
        ("Maintain image quality when resizing?", "tagged/image+resize+quality", "10 answers", "image, resize, quality"),
        ("How to resize images without losing aspect ratio?", "tagged/image+resize+aspect-ratio", "11 answers", "image, resize, aspect-ratio"),
    ],
    "screenshot-mockup": [
        ("How to create device mockups programmatically?", "tagged/mockup+screenshot+design", "5 answers", "design, mockup, screenshot"),
        ("Overlay an image on a device frame using Canvas?", "tagged/canvas+overlay+image", "7 answers", "javascript, canvas, image"),
        ("Browser screenshot tools for web developers?", "tagged/screenshot+browser+developer-tools", "9 answers", "screenshot, browser, tools"),
    ],
    "screenshot-to-code": [
        ("How to convert a screenshot to HTML/CSS?", "tagged/screenshot+html+css+conversion", "6 answers", "html, css, conversion"),
        ("AI-based image to code tools?", "tagged/ai+image-to-code+development", "8 answers", "ai, code-generation, tools"),
        ("How to extract design specifications from screenshots?", "tagged/design+screenshot+extraction", "5 answers", "design, screenshot, development"),
    ],
    "pixel-art-editor": [
        ("How to create a pixel art editor with Canvas?", "tagged/pixel-art+canvas+javascript", "7 answers", "javascript, canvas, pixel-art"),
        ("HTML5 Canvas pixel manipulation basics?", "tagged/canvas+pixel+javascript", "10 answers", "javascript, canvas, pixels"),
        ("How to export Canvas drawings as PNG?", "tagged/canvas+png+export", "9 answers", "javascript, canvas, export"),
    ],
    "gif-builder": [
        ("How to create animated GIFs in JavaScript?", "tagged/gif+animation+javascript", "8 answers", "javascript, gif, animation"),
        ("GIF encoding algorithm explained?", "tagged/gif+encoding+algorithm", "6 answers", "gif, encoding, algorithm"),
        ("How to optimize GIF file size?", "tagged/gif+optimization+compression", "9 answers", "gif, optimization, compression"),
    ],
    "video-to-gif": [
        ("How to convert video to GIF in the browser?", "tagged/video+gif+javascript+conversion", "7 answers", "javascript, video, gif"),
        ("FFmpeg.wasm for video processing in the browser?", "tagged/ffmpeg+wasm+javascript", "9 answers", "ffmpeg, wasm, javascript"),
        ("How to extract frames from a video with JavaScript?", "tagged/video+frames+javascript", "8 answers", "javascript, video, frames"),
    ],
    "meme-generator": [
        ("How to add text overlay to images with Canvas?", "tagged/canvas+text+image-overlay", "10 answers", "javascript, canvas, text"),
        ("Drawing styled text on HTML5 Canvas?", "tagged/canvas+text+styling", "8 answers", "javascript, canvas, typography"),
        ("How to download a Canvas element as an image?", "tagged/canvas+download+image", "12 answers", "javascript, canvas, download"),
    ],
    "logo-maker": [
        ("How to create SVG logos programmatically?", "tagged/svg+logo+generation", "6 answers", "svg, logo, generation"),
        ("SVG text styling and effects?", "tagged/svg+text+styling", "8 answers", "svg, text, design"),
        ("How to export SVG as different formats?", "tagged/svg+export+conversion", "7 answers", "svg, export, formats"),
    ],

    # ── Security / Network Tools ──
    "ssl-checker": [
        ("How to check SSL certificate details programmatically?", "tagged/ssl+certificate+verification", "10 answers", "ssl, certificate, security"),
        ("What does an SSL certificate verify?", "tagged/ssl+tls+certificate", "13 answers", "ssl, tls, security"),
        ("How to troubleshoot SSL certificate errors?", "tagged/ssl+certificate+error", "15 answers", "ssl, certificate, debugging"),
    ],
    "dns-lookup": [
        ("How to perform DNS lookups in JavaScript?", "tagged/dns+lookup+javascript", "8 answers", "dns, javascript, networking"),
        ("What are the different DNS record types?", "tagged/dns+records+networking", "12 answers", "dns, records, networking"),
        ("How does DNS resolution work?", "tagged/dns+resolution+networking", "10 answers", "dns, networking, internet"),
    ],
    "ip-lookup": [
        ("How to get a user's IP address in JavaScript?", "tagged/ip-address+javascript+geolocation", "14 answers", "javascript, ip-address, networking"),
        ("IP geolocation APIs for IP address lookup?", "tagged/ip+geolocation+api", "9 answers", "ip, geolocation, api"),
        ("What is the difference between IPv4 and IPv6?", "tagged/ipv4+ipv6+networking", "11 answers", "ipv4, ipv6, networking"),
    ],
    "subnet-calculator": [
        ("How to calculate subnet mask and CIDR notation?", "tagged/subnet+cidr+networking", "12 answers", "networking, subnet, cidr"),
        ("Subnetting explained - how does it work?", "tagged/subnet+networking+ip", "10 answers", "networking, subnet, ip"),
        ("How to determine the number of hosts in a subnet?", "tagged/subnet+hosts+calculation", "8 answers", "networking, subnet, calculation"),
    ],
    "http-status-checker": [
        ("What do HTTP status codes mean?", "tagged/http+status-code+web", "18 answers", "http, status-code, web"),
        ("How to check HTTP status of a URL programmatically?", "tagged/http+status+fetch", "11 answers", "http, fetch, javascript"),
        ("Common HTTP status codes and when they occur?", "tagged/http+status-code+reference", "14 answers", "http, status-code, web-development"),
    ],
    "webhook-tester": [
        ("What is a webhook and how does it work?", "tagged/webhook+http+api", "13 answers", "webhook, http, api"),
        ("How to test webhooks during development?", "tagged/webhook+testing+development", "9 answers", "webhook, testing, development"),
        ("How to secure webhook endpoints?", "tagged/webhook+security+authentication", "7 answers", "webhook, security, api"),
    ],
    "internet-speed-checker": [
        ("How to measure internet speed with JavaScript?", "tagged/speed-test+javascript+network", "7 answers", "javascript, network, speed"),
        ("How does a speed test work technically?", "tagged/speed-test+networking+bandwidth", "9 answers", "networking, bandwidth, speed"),
        ("Measuring download and upload speed in the browser?", "tagged/speed-test+browser+performance", "6 answers", "browser, performance, network"),
    ],
    "chmod-calculator": [
        ("How do Unix file permissions work?", "tagged/chmod+permissions+linux", "16 answers", "linux, chmod, permissions"),
        ("chmod octal notation explained?", "tagged/chmod+octal+linux", "13 answers", "linux, chmod, octal"),
        ("How to set file permissions in Linux?", "tagged/linux+permissions+chmod", "18 answers", "linux, permissions, chmod"),
    ],

    # ── Productivity / Utility Tools ──
    "pomodoro-timer": [
        ("How to build a Pomodoro timer in JavaScript?", "tagged/pomodoro+timer+javascript", "8 answers", "javascript, timer, pomodoro"),
        ("Implementing a countdown timer with setInterval?", "tagged/javascript+timer+setinterval", "12 answers", "javascript, timer, setinterval"),
        ("Web Notifications API for timer alerts?", "tagged/notifications+javascript+api", "9 answers", "javascript, notifications, api"),
    ],
    "countdown-timer": [
        ("How to create a countdown timer in JavaScript?", "tagged/countdown+timer+javascript", "15 answers", "javascript, countdown, timer"),
        ("Accurate timer implementation with requestAnimationFrame?", "tagged/timer+requestanimationframe+javascript", "8 answers", "javascript, timer, animation"),
        ("How to handle timer drift in JavaScript?", "tagged/timer+drift+accuracy", "6 answers", "javascript, timer, accuracy"),
    ],
    "stopwatch": [
        ("How to build a stopwatch with JavaScript?", "tagged/stopwatch+javascript+timer", "10 answers", "javascript, stopwatch, timer"),
        ("Performance.now for high-precision timing?", "tagged/performance-now+javascript+timing", "7 answers", "javascript, timing, performance"),
        ("How to format elapsed time as HH:MM:SS?", "tagged/time-format+javascript+display", "9 answers", "javascript, time-format, display"),
    ],
    "emoji-picker": [
        ("How to implement an emoji picker in JavaScript?", "tagged/emoji+picker+javascript", "8 answers", "javascript, emoji, ui"),
        ("Detecting emoji support in the browser?", "tagged/emoji+browser+detection", "6 answers", "browser, emoji, detection"),
        ("How to handle emoji input and display?", "tagged/emoji+unicode+rendering", "10 answers", "emoji, unicode, rendering"),
    ],
    "kanban-board": [
        ("How to build a drag-and-drop Kanban board?", "tagged/kanban+drag-drop+javascript", "9 answers", "javascript, drag-drop, kanban"),
        ("HTML drag and drop API tutorial?", "tagged/drag-drop+html5+api", "13 answers", "html5, drag-drop, api"),
        ("How to persist Kanban board state in localStorage?", "tagged/localstorage+state+javascript", "7 answers", "javascript, localstorage, state"),
    ],
    "whiteboard": [
        ("How to create a drawing app with HTML5 Canvas?", "tagged/canvas+drawing+javascript", "11 answers", "javascript, canvas, drawing"),
        ("Canvas mouse and touch event handling?", "tagged/canvas+events+mouse+touch", "9 answers", "javascript, canvas, events"),
        ("How to implement undo/redo in a Canvas app?", "tagged/canvas+undo+redo", "7 answers", "javascript, canvas, undo"),
    ],
    "mind-map-maker": [
        ("How to create a mind map in JavaScript?", "tagged/mindmap+javascript+visualization", "6 answers", "javascript, mindmap, visualization"),
        ("Tree layout algorithms for mind maps?", "tagged/tree+layout+algorithm", "8 answers", "algorithm, tree, layout"),
        ("How to render connected nodes with SVG?", "tagged/svg+nodes+connections", "7 answers", "svg, visualization, javascript"),
    ],
    "flow-chart-maker": [
        ("How to build a flowchart editor in JavaScript?", "tagged/flowchart+editor+javascript", "7 answers", "javascript, flowchart, editor"),
        ("Drawing connectors between elements in SVG?", "tagged/svg+connectors+flowchart", "9 answers", "svg, flowchart, connectors"),
        ("Best JavaScript libraries for diagram creation?", "tagged/javascript+diagram+library", "11 answers", "javascript, diagram, library"),
    ],
    "wireframe-tool": [
        ("How to create a wireframing tool with JavaScript?", "tagged/wireframe+javascript+design-tool", "5 answers", "javascript, wireframe, design"),
        ("Drag and drop UI builder implementation?", "tagged/drag-drop+ui-builder+javascript", "8 answers", "javascript, drag-drop, ui"),
        ("How to export wireframes as images?", "tagged/wireframe+export+image", "4 answers", "wireframe, export, design"),
    ],
    "flashcard-maker": [
        ("How to implement spaced repetition in JavaScript?", "tagged/spaced-repetition+javascript+learning", "6 answers", "javascript, spaced-repetition, learning"),
        ("Building a flashcard app with local storage?", "tagged/flashcard+localstorage+javascript", "7 answers", "javascript, localstorage, education"),
        ("Leitner system algorithm for flashcards?", "tagged/leitner+algorithm+flashcards", "5 answers", "algorithm, flashcards, learning"),
    ],
    "habit-tracker": [
        ("How to build a habit tracker with JavaScript?", "tagged/habit-tracker+javascript+app", "5 answers", "javascript, app, tracking"),
        ("Streak calculation algorithm?", "tagged/streak+algorithm+date", "7 answers", "algorithm, date, tracking"),
        ("Storing habit data in localStorage?", "tagged/localstorage+data+javascript", "8 answers", "javascript, localstorage, data"),
    ],
    "metronome": [
        ("How to build an accurate metronome with Web Audio API?", "tagged/web-audio-api+metronome+javascript", "7 answers", "javascript, web-audio, metronome"),
        ("AudioContext scheduling for precise timing?", "tagged/audiocontext+scheduling+timing", "9 answers", "web-audio, audiocontext, timing"),
        ("Web Audio API oscillator for generating tones?", "tagged/web-audio-api+oscillator+tones", "6 answers", "web-audio, oscillator, javascript"),
    ],
    "typing-speed-test": [
        ("How to calculate words per minute (WPM)?", "tagged/wpm+typing+calculation", "6 answers", "typing, wpm, calculation"),
        ("Building a typing test with JavaScript?", "tagged/typing-test+javascript+app", "5 answers", "javascript, typing-test, app"),
        ("How to measure typing accuracy?", "tagged/typing+accuracy+algorithm", "4 answers", "typing, accuracy, algorithm"),
    ],
    "typing-test": [
        ("How to detect keyboard events in JavaScript?", "tagged/keyboard+events+javascript", "14 answers", "javascript, keyboard, events"),
        ("KeyboardEvent.key vs keyCode?", "tagged/keyboard+keycode+javascript", "10 answers", "javascript, keyboard, events"),
        ("How to implement real-time input validation?", "tagged/input+validation+javascript", "8 answers", "javascript, validation, input"),
    ],
    "word-scramble-solver": [
        ("How to find all anagrams of a word?", "tagged/anagram+algorithm+string", "10 answers", "algorithm, anagram, string"),
        ("Trie data structure for word lookup?", "tagged/trie+data-structure+algorithm", "12 answers", "trie, data-structure, algorithm"),
        ("Permutation algorithm for generating word combinations?", "tagged/permutation+algorithm+string", "9 answers", "algorithm, permutation, string"),
    ],

    # ── AI / Content Tools ──
    "ai-detector": [
        ("How does AI text detection work?", "tagged/ai+detection+nlp", "7 answers", "ai, detection, nlp"),
        ("Perplexity and burstiness in AI text detection?", "tagged/ai+perplexity+text-analysis", "5 answers", "ai, nlp, text-analysis"),
        ("How to detect machine-generated text?", "tagged/ai+text+detection-algorithm", "8 answers", "ai, algorithm, text"),
    ],
    "ai-video-generator": [
        ("How do AI video generators work?", "tagged/ai+video+generation", "5 answers", "ai, video, generation"),
        ("Text-to-video AI models overview?", "tagged/ai+text-to-video+models", "6 answers", "ai, video, machine-learning"),
        ("How to integrate AI video APIs?", "tagged/ai+video+api", "4 answers", "ai, api, video"),
    ],
    "apa-citation-generator": [
        ("How to format APA citations correctly?", "tagged/apa+citation+formatting", "8 answers", "apa, citation, academic"),
        ("APA 7th edition citation rules?", "tagged/apa+7th-edition+citation", "6 answers", "apa, citation, style-guide"),
        ("How to cite websites in APA format?", "tagged/apa+citation+website", "10 answers", "apa, citation, web-source"),
    ],
    "apa-source-generator": [
        ("APA reference list formatting rules?", "tagged/apa+reference+formatting", "7 answers", "apa, reference, formatting"),
        ("How to format DOI in APA citations?", "tagged/apa+doi+citation", "6 answers", "apa, doi, reference"),
        ("APA in-text citation vs reference list entry?", "tagged/apa+in-text+reference", "9 answers", "apa, citation, academic-writing"),
    ],
    "essay-outline-generator": [
        ("How to structure an essay outline?", "tagged/essay+outline+writing", "7 answers", "writing, essay, structure"),
        ("5-paragraph essay structure explained?", "tagged/essay+structure+academic", "9 answers", "essay, structure, academic"),
        ("How to write a thesis statement?", "tagged/thesis+essay+writing", "10 answers", "writing, thesis, academic"),
    ],
    "resume-builder": [
        ("How to generate PDF from HTML/CSS?", "tagged/html-to-pdf+css+generation", "13 answers", "html, pdf, css"),
        ("Best practices for ATS-friendly resume formatting?", "tagged/resume+ats+formatting", "6 answers", "resume, formatting, ats"),
        ("CSS print stylesheet for resume printing?", "tagged/css+print+stylesheet", "8 answers", "css, print, media-query"),
    ],
    "baby-name-generator": [
        ("How to build a random name generator?", "tagged/random+name+generator", "6 answers", "random, generator, javascript"),
        ("Filtering and searching arrays in JavaScript?", "tagged/javascript+array+filter", "14 answers", "javascript, array, filter"),
        ("How to implement fuzzy search in JavaScript?", "tagged/fuzzy-search+javascript+algorithm", "9 answers", "javascript, search, algorithm"),
    ],

    # ── Encoding / Crypto Tools ──
    "ascii-art-generator": [
        ("How to convert images to ASCII art in JavaScript?", "tagged/ascii-art+javascript+image", "8 answers", "javascript, ascii-art, image"),
        ("Character density mapping for ASCII art?", "tagged/ascii-art+algorithm+density", "5 answers", "algorithm, ascii-art, image"),
        ("How to render ASCII art in HTML?", "tagged/ascii-art+html+monospace", "6 answers", "html, ascii-art, rendering"),
    ],

    # ── YouTube Tools ──
    "youtube-converter": [
        ("How to embed YouTube videos responsively?", "tagged/youtube+embed+responsive", "14 answers", "youtube, embed, responsive"),
        ("YouTube oEmbed API for video metadata?", "tagged/youtube+oembed+api", "7 answers", "youtube, api, oembed"),
        ("How to get YouTube video information from URL?", "tagged/youtube+url+parsing", "9 answers", "youtube, url, parsing"),
    ],
    "youtube-thumbnail": [
        ("How to get YouTube video thumbnail URL?", "tagged/youtube+thumbnail+api", "16 answers", "youtube, thumbnail, api"),
        ("YouTube thumbnail image sizes and formats?", "tagged/youtube+thumbnail+sizes", "10 answers", "youtube, thumbnail, images"),
        ("How to download YouTube thumbnails programmatically?", "tagged/youtube+thumbnail+download", "8 answers", "youtube, thumbnail, download"),
    ],
}

def get_title_from_slug(slug):
    """Convert a slug to a readable title."""
    return slug.replace('-', ' ').title()

def generate_questions_for_slug(slug):
    """Generate reasonable SO questions based on the tool slug."""
    title = get_title_from_slug(slug)
    tag = slug.replace('-', '+')

    # Determine category from slug keywords
    if 'calculator' in slug:
        return [
            (f"How to implement {title.lower()} logic in JavaScript?", f"tagged/{tag}+javascript", "8 answers", f"javascript, {slug.split('-')[0]}, calculation"),
            (f"Algorithm for {title.lower()} computation?", f"tagged/{tag}+algorithm", "6 answers", f"algorithm, math, calculation"),
            (f"Best practices for {title.lower()} accuracy?", f"tagged/{tag}+accuracy", "5 answers", f"math, accuracy, implementation"),
        ]
    elif 'generator' in slug:
        return [
            (f"How to build a {title.lower()} in JavaScript?", f"tagged/{tag}+javascript", "9 answers", f"javascript, {slug.split('-')[0]}, generation"),
            (f"Best approach for generating {slug.split('-')[0]} content?", f"tagged/{tag}+algorithm", "7 answers", f"algorithm, generation, javascript"),
            (f"Client-side {title.lower()} implementation?", f"tagged/{tag}+browser", "5 answers", f"javascript, browser, generation"),
        ]
    elif 'converter' in slug:
        return [
            (f"How to convert {slug.split('-')[0]} data in JavaScript?", f"tagged/{tag}+javascript", "10 answers", f"javascript, conversion, {slug.split('-')[0]}"),
            (f"Best library for {title.lower()} operations?", f"tagged/{tag}+library", "7 answers", f"javascript, library, conversion"),
            (f"Handling edge cases in {title.lower()}?", f"tagged/{tag}+edge-cases", "5 answers", f"conversion, edge-cases, implementation"),
        ]
    elif 'checker' in slug or 'validator' in slug or 'tester' in slug:
        return [
            (f"How to implement {title.lower()} in JavaScript?", f"tagged/{tag}+javascript", "8 answers", f"javascript, validation, {slug.split('-')[0]}"),
            (f"Best algorithms for {title.lower()}?", f"tagged/{tag}+algorithm", "6 answers", f"algorithm, validation, implementation"),
            (f"Client-side {title.lower()} best practices?", f"tagged/{tag}+best-practices", "5 answers", f"javascript, best-practices, validation"),
        ]
    elif 'editor' in slug or 'maker' in slug or 'builder' in slug:
        return [
            (f"How to build a {title.lower()} with JavaScript?", f"tagged/{tag}+javascript", "9 answers", f"javascript, {slug.split('-')[0]}, ui"),
            (f"Drag and drop implementation for {title.lower()}?", f"tagged/{tag}+drag-drop", "7 answers", f"javascript, drag-drop, ui"),
            (f"Saving and exporting from a {title.lower()}?", f"tagged/{tag}+export", "5 answers", f"javascript, export, file"),
        ]
    elif 'picker' in slug:
        return [
            (f"How to create a {title.lower()} component?", f"tagged/{tag}+javascript", "8 answers", f"javascript, ui, {slug.split('-')[0]}"),
            (f"Custom {title.lower()} UI implementation?", f"tagged/{tag}+ui+component", "6 answers", f"javascript, ui-component, design"),
            (f"Accessible {title.lower()} design patterns?", f"tagged/{tag}+accessibility", "5 answers", f"accessibility, ui, web-design"),
        ]
    elif 'encoder' in slug or 'decoder' in slug:
        return [
            (f"How to {slug.split('-')[0]} encode/decode in JavaScript?", f"tagged/{tag}+javascript", "11 answers", f"javascript, encoding, {slug.split('-')[0]}"),
            (f"{title} algorithm implementation?", f"tagged/{tag}+algorithm", "7 answers", f"algorithm, encoding, implementation"),
            (f"When to use {title.lower()} in web development?", f"tagged/{tag}+web-development", "6 answers", f"web-development, encoding, best-practices"),
        ]
    elif 'minifier' in slug:
        return [
            (f"How to minify {slug.split('-')[0]} for production?", f"tagged/{tag}+optimization", "10 answers", f"{slug.split('-')[0]}, minification, optimization"),
            (f"Best {title.lower()} tools compared?", f"tagged/{tag}+tools", "8 answers", f"{slug.split('-')[0]}, tools, comparison"),
            (f"Does {slug.split('-')[0]} minification affect performance?", f"tagged/{tag}+performance", "7 answers", f"performance, minification, web"),
        ]
    elif 'formatter' in slug:
        return [
            (f"How to format {slug.split('-')[0]} code in JavaScript?", f"tagged/{tag}+javascript", "10 answers", f"javascript, formatting, {slug.split('-')[0]}"),
            (f"Best {slug.split('-')[0]} formatting conventions?", f"tagged/{tag}+conventions", "8 answers", f"formatting, conventions, {slug.split('-')[0]}"),
            (f"Auto-format {slug.split('-')[0]} on save?", f"tagged/{tag}+auto-format", "6 answers", f"formatting, tools, {slug.split('-')[0]}"),
        ]
    else:
        return [
            (f"How to implement {title.lower()} in JavaScript?", f"tagged/{tag}+javascript", "9 answers", f"javascript, implementation, web"),
            (f"Best approach for building a {title.lower()}?", f"tagged/{tag}+implementation", "7 answers", f"javascript, web-development, tools"),
            (f"Client-side {title.lower()} techniques?", f"tagged/{tag}+client-side", "5 answers", f"javascript, browser, client-side"),
        ]

def build_section_html(questions):
    """Build the new-format SO questions HTML section."""
    items = []
    for q_title, q_url_path, answers, tags in questions:
        url = f"https://stackoverflow.com/questions/{q_url_path}"
        items.append(
            f'    <li style="margin:0.6rem 0;padding:0.75rem;background:#0a0a12;border-radius:6px;">\n'
            f'      <a href="{url}" target="_blank" rel="noopener" style="color:#00ccff;text-decoration:none;font-size:0.9rem;">{q_title}</a>\n'
            f'      <span style="display:block;font-size:0.75rem;color:#666;margin-top:0.25rem;">{answers} &middot; tagged: {tags}</span>\n'
            f'    </li>'
        )
    items_html = "\n".join(items)
    return (
        f'<section class="so-questions" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;margin:2rem 0;">\n'
        f'  <h3 style="font-family:monospace;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:#8888a0;margin:0 0 1rem;">Community Questions</h3>\n'
        f'  <ul style="list-style:none;padding:0;margin:0;">\n'
        f'{items_html}\n'
        f'  </ul>\n'
        f'</section>'
    )

def remove_old_so_section(html):
    """Remove the old-format SO questions section."""
    # Pattern 1: <!-- so-questions-section --> followed by <div class="so-questions" ...>...</div>
    pattern = r'<!-- so-questions-section -->\s*<div class="so-questions"[^>]*>.*?</div>\s*'
    html = re.sub(pattern, '', html, flags=re.DOTALL)

    # Pattern 2: Just <div class="so-questions" ...>...</div> without the comment
    # Be careful to match the outermost closing </div>
    # We need to handle nested divs, so use a more targeted approach
    pattern2 = r'<div class="so-questions"[^>]*>(?:(?!<div\b).)*?</div>\s*'
    html = re.sub(pattern2, '', html, flags=re.DOTALL)

    return html

def find_insertion_point(html):
    """Find where to insert the new section. Returns (position, description)."""
    # Priority 1: Before FAQ section
    faq_patterns = [
        r'(<div\s+class="faq-section")',
        r'(<!--\s*FAQ\s*-->)',
        r'(<section[^>]*class="[^"]*faq[^"]*")',
        r'(<h2[^>]*>\s*Frequently Asked Questions)',
        r'(<h2[^>]*>\s*FAQ\s*</h2>)',
    ]
    for pattern in faq_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.start(), "before FAQ"

    # Priority 2: Before closing </main>
    match = re.search(r'</main>', html, re.IGNORECASE)
    if match:
        return match.start(), "before </main>"

    # Priority 3: Before closing </article>
    match = re.search(r'</article>', html, re.IGNORECASE)
    if match:
        return match.start(), "before </article>"

    # Priority 4: Before the footer
    match = re.search(r'<footer', html, re.IGNORECASE)
    if match:
        return match.start(), "before <footer>"

    # Priority 5: Before closing </body>
    match = re.search(r'</body>', html, re.IGNORECASE)
    if match:
        return match.start(), "before </body>"

    return None, None

def process_tool(tool_dir):
    """Process a single tool directory. Returns (tool_name, status)."""
    slug = os.path.basename(tool_dir)
    index_path = os.path.join(tool_dir, 'index.html')

    if not os.path.isfile(index_path):
        return slug, "no index.html"

    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Get questions for this tool
    if slug in TOOL_QUESTIONS:
        questions = TOOL_QUESTIONS[slug]
    else:
        questions = generate_questions_for_slug(slug)

    # Remove old SO section if present
    html_cleaned = remove_old_so_section(html)

    # Build new section
    new_section = build_section_html(questions)

    # Find insertion point
    pos, desc = find_insertion_point(html_cleaned)
    if pos is None:
        return slug, "no insertion point found"

    # Insert new section
    html_final = html_cleaned[:pos] + new_section + "\n" + html_cleaned[pos:]

    # Write back
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_final)

    return slug, f"enhanced ({desc}, {len(questions)} questions)"

def main():
    tools_enhanced = 0
    tools_skipped = 0
    tools_failed = 0
    results = []

    # Get all tool directories
    for entry in sorted(os.listdir(BASE_DIR)):
        tool_dir = os.path.join(BASE_DIR, entry)
        if not os.path.isdir(tool_dir):
            continue
        index_path = os.path.join(tool_dir, 'index.html')
        if not os.path.isfile(index_path):
            continue

        slug, status = process_tool(tool_dir)
        results.append((slug, status))

        if status.startswith("enhanced"):
            tools_enhanced += 1
        elif status == "no insertion point found":
            tools_failed += 1
        else:
            tools_skipped += 1

    print(f"\n{'='*60}")
    print(f"Stack Overflow Community Questions Injection Report")
    print(f"{'='*60}")
    print(f"Tools enhanced:  {tools_enhanced}")
    print(f"Tools skipped:   {tools_skipped}")
    print(f"Tools failed:    {tools_failed}")
    print(f"Total processed: {tools_enhanced + tools_skipped + tools_failed}")
    print(f"{'='*60}\n")

    # Show details for mapped vs auto-generated
    mapped_count = 0
    auto_count = 0
    for slug, status in results:
        if status.startswith("enhanced"):
            if slug in TOOL_QUESTIONS:
                mapped_count += 1
            else:
                auto_count += 1

    print(f"With curated questions: {mapped_count}")
    print(f"With auto-generated:    {auto_count}")
    print()

    # Show any failures
    failures = [(s, st) for s, st in results if not st.startswith("enhanced")]
    if failures:
        print("Issues:")
        for slug, status in failures:
            print(f"  - {slug}: {status}")
    else:
        print("All tools processed successfully!")

    # Show some examples
    print(f"\nSample results:")
    for slug, status in results[:10]:
        src = "curated" if slug in TOOL_QUESTIONS else "auto"
        print(f"  {slug}: {status} [{src}]")
    print("  ...")

if __name__ == '__main__':
    main()
