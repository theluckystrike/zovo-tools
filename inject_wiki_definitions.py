#!/usr/bin/env python3
"""
Inject Wikipedia-style definition sections into tool pages that don't already have Wikipedia content.
Targets tools in ~/zovo-workspaces/zovo-tools/ that lack 'wikipedia.org' in their HTML.
"""

import os
import re
import glob

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Comprehensive mapping: slug -> (wikipedia_article_slug, definition_text)
WIKI_MAP = {
    # Calculators
    "paycheck-calculator": (
        "Payroll",
        "Payroll is the process by which employers pay an employee for the work they have performed. Payroll processing involves calculating each employee's gross pay, then deducting federal, state, and local taxes, along with Social Security, Medicare, and any voluntary deductions such as retirement contributions and health insurance premiums. The net result is the employee's take-home pay."
    ),
    "gpa-calculator": (
        "Grading_in_education",
        "Grading in education is the process of applying standardized measurements to varying levels of achievements in a course. Grades can be assigned as letters, numbers, or descriptors, and are typically weighted according to credit hours to produce a grade point average (GPA). The GPA is a numerical representation of a student's academic performance across all courses taken."
    ),
    "bmi-calculator": (
        "Body_mass_index",
        "Body mass index (BMI) is a value derived from the mass and height of a person. The BMI is defined as the body mass divided by the square of the body height, expressed in units of kg/m\u00b2. BMI is used broadly as a general indicator of whether a person has a healthy body weight for their height."
    ),
    "calorie-calculator": (
        "Calorie",
        "A calorie is a unit of energy. In nutrition, the large calorie (kilocalorie or kcal) represents the amount of energy needed to raise the temperature of one kilogram of water by one degree Celsius. Calorie counting is a common method used to manage body weight, based on the principle that energy balance determines weight change over time."
    ),
    "compound-interest-calculator": (
        "Compound_interest",
        "Compound interest is the addition of interest to the principal sum of a loan or deposit, so that interest is earned on the previously accumulated interest as well as the original principal. This effect of earning interest on interest is known as compounding, and it causes wealth to grow at an accelerating rate over time."
    ),
    "mortgage-calculator": (
        "Mortgage_loan",
        "A mortgage loan is a secured loan where the borrower pledges real property as collateral to a lender. The borrower is obligated to make a predetermined set of payments, typically monthly, over a fixed term. Mortgage calculations determine the periodic payment required to repay the borrowed amount plus interest over the amortization period."
    ),
    "amortization-calculator": (
        "Amortization_(business)",
        "Amortization refers to the process of paying off a debt over time through regular payments. A portion of each payment is applied toward the principal balance and a portion is applied toward interest. In the early years of a loan, a greater percentage of the payment goes toward interest, gradually shifting toward principal as the balance decreases."
    ),
    "blood-alcohol-calculator": (
        "Blood_alcohol_content",
        "Blood alcohol content (BAC) is the concentration of alcohol in a person's bloodstream, expressed as a percentage by mass. BAC is most commonly used as a metric of alcohol intoxication for legal and medical purposes. The Widmark formula is the standard method for estimating BAC based on the amount of alcohol consumed, body weight, gender, and time elapsed."
    ),
    "profit-margin-calculator": (
        "Profit_margin",
        "Profit margin is a financial metric that measures the percentage of revenue that exceeds the costs of production. It is calculated by dividing net income by revenue and is expressed as a percentage. There are several types of profit margin including gross profit margin, operating profit margin, and net profit margin, each providing insight into different aspects of a company's profitability."
    ),
    "percentage-calculator": (
        "Percentage",
        "A percentage is a number or ratio expressed as a fraction of 100. The term is derived from the Latin per centum meaning 'by the hundred.' Percentages are used to express proportions, compare quantities, describe changes, and calculate discounts, taxes, interest rates, and other financial and statistical measures."
    ),
    "grade-calculator": (
        "Grading_in_education",
        "Grading in education is the process of applying standardized measurements to varying levels of achievement in a course. Grades can be assigned as letters (A through F), percentages, or grade points. Weighted grading assigns different importance to different types of assignments, allowing final grades to more accurately reflect overall mastery of the subject material."
    ),
    "age-calculator": (
        "Age",
        "Age is the length of time that a person has lived or a thing has existed, typically measured in years, months, and days from the date of birth. Chronological age is determined by calculating the difference between the current date and the date of birth, accounting for varying month lengths and leap years."
    ),
    "date-calculator": (
        "Calendar_date",
        "A calendar date is a reference to a particular day represented within a calendar system. The Gregorian calendar is the most widely used civil calendar in the world, organizing time into years, months, and days. Date arithmetic involves adding or subtracting days, months, or years to determine past or future dates, accounting for varying month lengths and leap years."
    ),
    "tip-calculator": (
        "Gratuity",
        "A gratuity, commonly known as a tip, is a sum of money given to service workers in addition to the payment for goods or services rendered. In many countries, tipping is customary in restaurants, hotels, and personal service industries. The typical tip amount varies by culture and region, commonly ranging from 15 to 20 percent of the pre-tax bill in the United States."
    ),
    "loan-calculator": (
        "Loan",
        "A loan is the lending of money by one or more individuals, organizations, or other entities to other individuals, organizations, or entities. The recipient incurs a debt and is usually obligated to pay interest on the debt until it is repaid, as well as to repay the principal amount borrowed. Loan calculations determine monthly payments, total interest, and amortization schedules."
    ),
    "salary-calculator": (
        "Salary",
        "A salary is a fixed regular payment, typically expressed as an annual sum, made by an employer to an employee. Salary calculations convert between hourly, weekly, biweekly, monthly, and annual pay rates, and account for deductions such as federal and state income taxes, Social Security, Medicare, and voluntary contributions."
    ),
    "debt-payoff-calculator": (
        "Debt",
        "Debt is an obligation that requires one party, the debtor, to pay money or other agreed-upon value to another party, the creditor. Debt repayment strategies include the avalanche method, which targets the highest interest rate first, and the snowball method, which targets the smallest balance first. Both methods aim to reduce total interest paid and accelerate the path to becoming debt-free."
    ),
    "electricity-cost-calculator": (
        "Electricity_pricing",
        "Electricity pricing varies widely by country, region, and rate structure. The cost of electricity is typically measured in kilowatt-hours (kWh) and is determined by the cost of generation, transmission, and distribution. Consumers can estimate their electricity costs by multiplying the wattage of devices by their hours of use and the price per kilowatt-hour."
    ),
    "aspect-ratio-calculator": (
        "Aspect_ratio_(image)",
        "The aspect ratio of an image is the proportional relationship between its width and its height. It is commonly expressed as two numbers separated by a colon, such as 16:9 or 4:3. Aspect ratio is a fundamental concept in photography, filmmaking, and display technology, determining how content appears on screens of different dimensions."
    ),
    "inflation-calculator": (
        "Inflation",
        "Inflation is a general increase in the prices of goods and services in an economy over a period of time. When the general price level rises, each unit of currency buys fewer goods and services, effectively reducing purchasing power. Inflation is typically measured by the Consumer Price Index (CPI) and is a key indicator monitored by central banks and economists."
    ),
    "investment-calculator": (
        "Investment",
        "Investment is the dedication of money to purchase financial instruments or other assets in order to gain profitable returns in the form of interest, income, or appreciation of value. Investment calculators help estimate future portfolio values by modeling variables such as initial principal, periodic contributions, expected rate of return, and time horizon."
    ),
    "retirement-calculator": (
        "Retirement",
        "Retirement is the withdrawal from one's position or occupation, typically upon reaching a certain age. Retirement planning involves estimating future income needs and savings required to maintain a desired standard of living after ceasing active employment. Key factors include current savings, expected contributions, investment returns, inflation, Social Security benefits, and anticipated life expectancy."
    ),
    "roi-calculator": (
        "Return_on_investment",
        "Return on investment (ROI) is a performance measure used to evaluate the efficiency or profitability of an investment. ROI is calculated by dividing the net profit of an investment by its initial cost, then expressing the result as a percentage. It is one of the most widely used metrics for comparing the relative attractiveness of different investment opportunities."
    ),
    "savings-calculator": (
        "Saving",
        "Saving is income not spent on consumption or deferred consumption. Methods of saving include putting money in a savings account, a pension fund, an investment fund, or as cash. Savings calculators project future account balances by modeling regular deposits, interest rates, and compounding frequency over a specified time period."
    ),
    "tax-calculator": (
        "Tax",
        "A tax is a compulsory financial charge or levy imposed on a taxpayer by a governmental organization to fund government spending and various public expenditures. Income taxes are typically calculated using a progressive rate structure where higher earnings are taxed at higher marginal rates. Tax calculators estimate federal and state tax liability based on income, filing status, and applicable deductions."
    ),
    "discount-calculator": (
        "Discounts_and_allowances",
        "Discounts and allowances are reductions to a basic price of goods or services. Discounts may be offered by sellers to buyers for various reasons including early payment, volume purchases, or promotional events. Calculating discounts involves applying the percentage reduction to the original price to determine the sale price and the total amount saved."
    ),
    "time-calculator": (
        "Time",
        "Time is the continued sequence of existence and events that occurs in an apparently irreversible succession from the past, through the present, and into the future. Time arithmetic involves adding, subtracting, and converting between units of time such as hours, minutes, seconds, days, weeks, and years, accounting for conventions like the 24-hour clock and varying calendar lengths."
    ),
    "subnet-calculator": (
        "Subnetwork",
        "A subnetwork, or subnet, is a logical subdivision of an IP network. The practice of dividing a network into two or more networks is called subnetting. Subnet masks define the boundary between the network portion and the host portion of an IP address, determining how many hosts can exist on each subnet and how traffic is routed between them."
    ),
    "statistics-calculator": (
        "Statistics",
        "Statistics is the discipline that concerns the collection, organization, analysis, interpretation, and presentation of data. Descriptive statistics summarize data through measures of central tendency (mean, median, mode) and measures of variability (range, variance, standard deviation). Inferential statistics use sample data to make generalizations about larger populations through hypothesis testing and confidence intervals."
    ),

    # Converters
    "unit-converter": (
        "Conversion_of_units",
        "Conversion of units is the conversion between different units of measurement for the same quantity, typically through multiplicative conversion factors. Unit conversion is essential in science, engineering, and everyday life, enabling consistent communication of measurements across systems such as the metric system and the imperial system."
    ),
    "binary-converter": (
        "Binary_number",
        "A binary number is a number expressed in the base-2 numeral system, which uses only two symbols: 0 and 1. Each digit in a binary number is called a bit. Binary is the fundamental language of computers and digital electronics, as it maps directly to the on/off states of transistors and logic gates."
    ),
    "hex-color-picker": (
        "Web_colors",
        "Web colors are colors used in displaying web pages on the World Wide Web. They can be specified as hexadecimal triplets, RGB values, HSL values, or by name. The hexadecimal color model uses a six-digit code preceded by a hash sign, where each pair of digits represents the intensity of red, green, and blue on a scale from 00 to FF."
    ),
    "roman-numeral-converter": (
        "Roman_numerals",
        "Roman numerals are a numeral system that originated in ancient Rome and remained the usual way of writing numbers throughout Europe well into the Late Middle Ages. The system uses combinations of letters from the Latin alphabet (I, V, X, L, C, D, M) to represent values. Numbers are formed by combining symbols and adding or subtracting their values according to specific rules."
    ),
    "pixel-to-rem-converter": (
        "CSS#Units",
        "CSS units define the size of elements and text on web pages. Pixels (px) are absolute units representing a single dot on the screen. Rem units are relative to the root element's font size, making them ideal for responsive design. Converting between px and rem ensures consistent scaling across different screen sizes and user accessibility settings."
    ),
    "currency-converter": (
        "Exchange_rate",
        "An exchange rate is the rate at which one currency will be exchanged for another. Exchange rates are determined by supply and demand in the foreign exchange market, which is the largest financial market in the world. Currency conversion tools apply current exchange rates to calculate the equivalent value of one currency in terms of another."
    ),
    "base64-encoder": (
        "Base64",
        "Base64 is a group of binary-to-text encoding schemes that represent binary data in sequences of 24 bits that can be represented by four 6-bit Base64 digits. It is designed to carry data stored in binary formats across channels that only reliably support text content. Base64 encoding is commonly used in email, data URLs, and web APIs."
    ),
    "base64-encoder-decoder": (
        "Base64",
        "Base64 is a group of binary-to-text encoding schemes that represent binary data in an ASCII string format by translating it into a radix-64 representation. Each Base64 digit represents exactly 6 bits of data, and three bytes of binary data can be represented by four Base64 characters. It is widely used for encoding binary data in email attachments, data URIs, and API payloads."
    ),
    "url-encoder-decoder": (
        "Percent-encoding",
        "Percent-encoding, also known as URL encoding, is a mechanism for encoding information in a Uniform Resource Identifier (URI) under certain circumstances. It replaces unsafe ASCII characters with a percent sign followed by two hexadecimal digits. This encoding is essential for transmitting special characters in URLs that would otherwise be interpreted as delimiters or control characters."
    ),
    "case-converter": (
        "Letter_case",
        "Letter case is the distinction between the letters that are in larger uppercase (capital letters) and smaller lowercase in the written representation of certain languages. Case conversion is a common text processing operation used in programming, writing, and data formatting. Common case styles include UPPERCASE, lowercase, Title Case, camelCase, and snake_case."
    ),
    "binary-text-converter": (
        "Binary_code",
        "Binary code represents text, computer instructions, or any other data using a two-symbol system, typically 0 and 1. In computing, text is encoded in binary using character encoding standards such as ASCII, where each character is assigned a unique binary number. Converting between binary and text is a fundamental operation in data processing and telecommunications."
    ),
    "color-converter": (
        "Color_model",
        "A color model is an abstract mathematical model describing the way colors can be represented as tuples of numbers. Common color models include RGB (Red, Green, Blue), HSL (Hue, Saturation, Lightness), and CMYK (Cyan, Magenta, Yellow, Key). Color conversion translates values between these different models to achieve consistent color representation across media."
    ),
    "number-base-converter": (
        "Radix",
        "In a positional numeral system, the radix or base is the number of unique digits used to represent numbers. Common bases include binary (base 2), octal (base 8), decimal (base 10), and hexadecimal (base 16). Converting between number bases involves expressing a value from one positional notation into another while preserving its numerical quantity."
    ),
    "json-yaml-converter": (
        "Serialization",
        "Serialization is the process of translating a data structure or object state into a format that can be stored or transmitted and reconstructed later. JSON and YAML are two popular human-readable data serialization formats. Converting between them allows developers to use whichever format best suits their toolchain while preserving the underlying data structure."
    ),
    "timestamp-converter": (
        "Unix_time",
        "Unix time is a system for representing a point in time as the number of seconds that have elapsed since 00:00:00 UTC on January 1, 1970, not counting leap seconds. It is widely used in computing and is the standard internal time representation for most operating systems. Timestamp converters translate between Unix timestamps and human-readable date and time formats."
    ),
    "px-to-rem": (
        "CSS#Units",
        "CSS units define the measurement system for sizing elements on web pages. Pixels (px) provide absolute sizing based on the display's resolution, while rem units are relative to the root element's font size. Converting from px to rem enables responsive typography and layout that respects user accessibility preferences for text sizing."
    ),
    "morse-code-translator": (
        "Morse_code",
        "Morse code is a method used in telecommunication to encode text characters as standardized sequences of two different signal durations, called dots and dashes. Devised in the 1840s by Samuel Morse and Alfred Vail, it was used for early electrical telegraph communication. Morse code remains relevant in amateur radio, aviation, and accessibility applications."
    ),

    # Developer tools
    "json-formatter": (
        "JSON",
        "JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. Based on a subset of the JavaScript programming language, JSON is a language-independent text format that has become the most common data format used for asynchronous communication between browsers and servers."
    ),
    "regex-tester": (
        "Regular_expression",
        "A regular expression (regex) is a sequence of characters that specifies a match pattern in text. Regular expressions are used in search engines, text editors, programming languages, and command-line utilities to find and manipulate strings. They provide a concise and flexible means for matching strings of text based on patterns defined by a formal language."
    ),
    "css-gradient-generator": (
        "CSS",
        "Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in a markup language such as HTML. CSS gradients allow displaying smooth transitions between two or more specified colors. CSS supports linear gradients, radial gradients, and conic gradients, each creating different visual effects through color interpolation."
    ),
    "markdown-editor": (
        "Markdown",
        "Markdown is a lightweight markup language for creating formatted text using a plain-text editor. Created by John Gruber in 2004, Markdown is widely used for blogging, documentation, instant messaging, online forums, collaborative software, and readme files. Its key design goal is readability, allowing the plain text format to be published as-is without looking like it has been marked up with tags."
    ),
    "xml-formatter": (
        "XML",
        "Extensible Markup Language (XML) is a markup language and file format for storing, transmitting, and reconstructing data. XML defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. It is widely used for data interchange between systems, configuration files, and document storage."
    ),
    "csv-to-json-converter": (
        "Comma-separated_values",
        "Comma-separated values (CSV) is a text file format that uses commas to separate values and newlines to separate records. Each line of the file is a data record, and each record consists of one or more fields separated by commas. CSV is a common data exchange format that is widely supported by consumer, business, and scientific applications."
    ),
    "csv-to-json": (
        "Comma-separated_values",
        "Comma-separated values (CSV) is a delimited text file format that uses commas to separate values. CSV files store tabular data in plain text form, where each line represents a data record. Converting CSV to JSON transforms flat tabular data into a hierarchical object format suitable for web APIs and modern applications."
    ),
    "yaml-validator": (
        "YAML",
        "YAML (a recursive acronym for 'YAML Ain't Markup Language') is a human-friendly data serialization language. It is commonly used for configuration files and in applications where data is being stored or transmitted. YAML uses indentation to denote structure, making it readable and concise compared to XML and JSON for configuration purposes."
    ),
    "sql-formatter": (
        "SQL",
        "SQL (Structured Query Language) is a domain-specific language used for managing and manipulating relational databases. SQL was initially developed at IBM in the early 1970s and has since become the standard language for relational database management systems. Formatting SQL queries improves readability and maintainability of database code."
    ),
    "cron-expression-generator": (
        "Cron",
        "Cron is a time-based job scheduler in Unix-like operating systems. Users set up and maintain software environments using cron to schedule jobs (commands or shell scripts) to run periodically at fixed times, dates, or intervals. Cron expressions define the schedule using five or six fields representing minute, hour, day of month, month, day of week, and optionally year."
    ),
    "cron-generator": (
        "Cron",
        "Cron is a time-based job scheduler found in Unix-like operating systems. It enables users to schedule jobs (commands or scripts) to run automatically at specified times and intervals. A cron expression consists of fields that define the schedule: minute, hour, day of month, month, and day of week, using numbers, wildcards, and special characters."
    ),
    "api-tester": (
        "API",
        "An application programming interface (API) is a way for two or more computer programs or components to communicate with each other. APIs define the kinds of calls or requests that can be made, how to make them, the data formats that should be used, and the conventions to follow. RESTful APIs use HTTP methods such as GET, POST, PUT, and DELETE to perform operations on resources."
    ),
    "color-contrast-checker": (
        "Web_accessibility",
        "Web accessibility means that websites, tools, and technologies are designed and developed so that people with disabilities can use them. The Web Content Accessibility Guidelines (WCAG) define minimum contrast ratios between text and background colors to ensure readability for users with visual impairments. A contrast ratio of at least 4.5:1 is required for normal text under WCAG AA standards."
    ),
    "box-shadow-generator": (
        "CSS",
        "Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in HTML or XML. The CSS box-shadow property adds shadow effects around an element's frame. It is described by horizontal and vertical offsets, blur radius, spread distance, and color, and is widely used to create depth and visual hierarchy in web design."
    ),
    "border-radius-generator": (
        "CSS",
        "Cascading Style Sheets (CSS) is a style sheet language used for controlling the visual presentation of web documents. The border-radius property in CSS defines the radius of an element's corners, allowing developers to create rounded corners on boxes. Each corner can be individually controlled, enabling shapes from simple rounded rectangles to circles and ellipses."
    ),
    "svg-to-png-converter": (
        "Scalable_Vector_Graphics",
        "Scalable Vector Graphics (SVG) is an XML-based vector image format for defining two-dimensional graphics. SVG images can be scaled to any size without loss of quality because they are defined mathematically rather than as a grid of pixels. Converting SVG to PNG (Portable Network Graphics) rasterizes the vector image into a fixed-resolution bitmap suitable for broader compatibility."
    ),
    "chmod-calculator": (
        "File-system_permissions",
        "File-system permissions control the ability of users to read, write, and execute files and directories. In Unix-like operating systems, permissions are represented by a three-digit octal number where each digit represents the access rights for the file owner, group, and others. The chmod command is used to change these permissions."
    ),
    "json-viewer": (
        "JSON",
        "JSON (JavaScript Object Notation) is a lightweight data interchange format based on a subset of JavaScript syntax. It consists of key-value pairs and ordered lists, using a minimal set of structural characters (braces, brackets, colons, and commas). JSON viewers provide a visual, hierarchical representation of JSON data that makes it easier to explore and understand complex nested structures."
    ),
    "json-path-finder": (
        "JSONPath",
        "JSONPath is a query language for JSON, similar to XPath for XML. It allows users to navigate and extract specific elements from complex JSON structures using path expressions. JSONPath expressions use dot notation or bracket notation to traverse nested objects and arrays, making it straightforward to locate deeply nested values in large JSON documents."
    ),
    "jwt-decoder": (
        "JSON_Web_Token",
        "A JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties. JWTs consist of three parts separated by dots: a header, a payload, and a signature. They are commonly used for authentication and authorization in web applications, enabling stateless session management between clients and servers."
    ),
    "html-encoder": (
        "Character_encodings_in_HTML",
        "HTML character encoding specifies how characters are converted to bytes when transmitted over the internet. HTML entities replace characters that are reserved in HTML (such as <, >, and &) with their encoded equivalents. Proper encoding prevents rendering errors and cross-site scripting (XSS) vulnerabilities by ensuring special characters are displayed as text rather than interpreted as markup."
    ),
    "htpasswd-generator": (
        "Htpasswd",
        ".htpasswd is a flat-file used to store usernames and passwords for basic authentication on an Apache HTTP Server. Passwords are stored in hashed form using algorithms such as bcrypt, MD5, or SHA-1. The htpasswd utility creates and updates these files, providing a simple mechanism for restricting access to web resources."
    ),
    "http-status-checker": (
        "List_of_HTTP_status_codes",
        "HTTP response status codes indicate whether a specific HTTP request has been successfully completed. They are grouped into five classes: informational (1xx), successful (2xx), redirection (3xx), client error (4xx), and server error (5xx). Status codes are issued by a server in response to a client's request and are fundamental to the HTTP protocol's operation."
    ),
    "js-minifier": (
        "Minification_(programming)",
        "Minification is the process of removing all unnecessary characters from the source code of interpreted programming languages without changing its functionality. This includes removing whitespace, comments, and shortening variable names. Minifying JavaScript reduces file size, decreasing load times and bandwidth usage in web applications."
    ),
    "css-minifier": (
        "Minification_(programming)",
        "Minification is the process of removing unnecessary characters from source code without altering its functionality. For CSS, this involves stripping whitespace, comments, and redundant declarations. Minified CSS files load faster and consume less bandwidth, improving web page performance and user experience."
    ),
    "css-grid-generator": (
        "CSS_grid_layout",
        "CSS Grid Layout is a two-dimensional layout system in CSS that allows developers to create complex, responsive grid-based layouts. It introduces a grid container with rows and columns, into which child elements can be placed. CSS Grid provides precise control over alignment, sizing, and positioning of elements within the grid structure."
    ),
    "css-animation-generator": (
        "CSS_animations",
        "CSS animations make it possible to animate transitions between CSS property values over time. They consist of two components: keyframes that define the styles at various points during the animation, and animation properties that configure the timing, duration, iteration, and direction. CSS animations provide a performant alternative to JavaScript-based animations for visual effects."
    ),
    "flexbox-generator": (
        "CSS_Flexible_Box_Layout",
        "CSS Flexible Box Layout, commonly known as Flexbox, is a one-dimensional layout model that provides a more efficient way to lay out, align, and distribute space among items in a container. Flexbox simplifies complex layout patterns such as centering, equal-height columns, and responsive navigation by providing properties for direction, wrapping, justification, and alignment."
    ),
    "code-beautifier": (
        "Prettyprint",
        "Prettyprinting, or code beautification, is the application of formatting conventions to source code to improve its readability. This includes consistent indentation, line breaks, spacing, and bracket placement. Code beautifiers automatically format code according to established style guides, making it easier for developers to read, understand, and maintain."
    ),
    "webhook-tester": (
        "Webhook",
        "A webhook is a method of augmenting or altering the behavior of a web page or application with custom callbacks. Webhooks are user-defined HTTP callbacks that are triggered by specific events. When an event occurs, the source site makes an HTTP request to the URL configured for the webhook, allowing real-time data transmission between applications."
    ),
    "dns-lookup": (
        "Domain_Name_System",
        "The Domain Name System (DNS) is a hierarchical and decentralized naming system for computers, services, or other resources connected to the Internet or a private network. It translates human-readable domain names (such as example.com) into numerical IP addresses needed for locating and identifying computer services and devices."
    ),
    "ip-lookup": (
        "IP_address",
        "An Internet Protocol (IP) address is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. IP addresses serve two principal functions: network interface identification and location addressing. IP lookup tools resolve IP addresses to geographic locations, hostnames, and network information."
    ),
    "ssl-checker": (
        "Transport_Layer_Security",
        "Transport Layer Security (TLS), and its predecessor Secure Sockets Layer (SSL), are cryptographic protocols designed to provide communications security over a computer network. SSL/TLS certificates authenticate the identity of websites and enable encrypted connections. SSL checkers verify certificate validity, expiration dates, and chain of trust."
    ),
    "schema-generator": (
        "Schema.org",
        "Schema.org is a collaborative vocabulary created by Google, Microsoft, Yahoo, and Yandex to provide a collection of shared schemas for structured data markup on web pages. Structured data helps search engines understand page content and enables rich results such as star ratings, FAQs, and knowledge panels in search results."
    ),
    "meta-tag-generator": (
        "Meta_element",
        "A meta element is an HTML element that provides structured metadata about a web page. Meta tags are placed in the head section of an HTML document and provide information such as page description, keywords, author, and viewport settings. Search engines and social media platforms use meta tags to understand and display page content in search results and link previews."
    ),
    "sitemap-generator": (
        "Site_map",
        "A site map (or sitemap) is a file that provides information about the pages, videos, and other content on a website, and the relationships between them. Search engines like Google read this file to crawl sites more efficiently. XML sitemaps list URLs along with metadata such as last modification date, change frequency, and priority."
    ),
    "robots-txt-generator": (
        "Robots.txt",
        "The robots exclusion standard, also known as the robots exclusion protocol or simply robots.txt, is a standard used by websites to communicate with web crawlers and other web robots. The standard specifies how to inform a web robot about which areas of the website should not be processed or scanned."
    ),
    "og-preview": (
        "Facebook_Platform#Open_Graph_protocol",
        "The Open Graph protocol enables any web page to become a rich object in a social graph. It was originally created by Facebook and uses meta tags in the head of an HTML document to define page properties such as title, description, image, and URL. These tags control how content appears when shared on social media platforms."
    ),
    "slug-generator": (
        "Clean_URL",
        "A clean URL, also known as a slug, is a URL that is human-readable and describes the content of the page. Slugs typically consist of lowercase letters, numbers, and hyphens, with spaces and special characters removed or replaced. Clean URLs improve usability, accessibility, and search engine optimization by making web addresses descriptive and memorable."
    ),
    "privacy-policy-generator": (
        "Privacy_policy",
        "A privacy policy is a statement or legal document that discloses some or all of the ways a party gathers, uses, discloses, and manages a customer's or client's data. Privacy laws in many jurisdictions require websites and applications to publish their data handling practices and obtain user consent for data collection."
    ),
    "regex-visualizer": (
        "Regular_expression",
        "A regular expression is a sequence of characters that defines a search pattern, primarily used for pattern matching within strings. Regex visualizers provide a graphical representation of the pattern's logic, showing how groups, quantifiers, and alternatives relate to each other. This visual approach helps developers understand and debug complex patterns."
    ),

    # Text tools
    "word-counter": (
        "Word_count",
        "Word count is the number of words in a document or passage of text. Word counting is commonly used in publishing, academia, journalism, and content creation to meet length requirements. Word processors and dedicated tools count words by identifying sequences of characters separated by whitespace or punctuation."
    ),
    "lorem-ipsum-generator": (
        "Lorem_ipsum",
        "Lorem ipsum is placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. It is derived from sections 1.10.32 and 1.10.33 of De finibus bonorum et malorum, a 1st-century BC text by Cicero, with words altered and removed to make it nonsensical."
    ),
    "paraphrase-tool": (
        "Paraphrase",
        "A paraphrase is a restatement of the meaning of a text or passage using other words. Paraphrasing is a fundamental skill in writing and communication, used to clarify meaning, avoid plagiarism, and adapt content for different audiences. Effective paraphrasing preserves the original meaning while substantially changing the wording and sentence structure."
    ),
    "text-diff-checker": (
        "Diff",
        "In computing, diff is a utility that compares files line by line and outputs the differences between them. The diff algorithm identifies insertions, deletions, and modifications between two versions of text. It is fundamental to version control systems such as Git and is widely used in software development for code review and change tracking."
    ),
    "diff-checker": (
        "Diff",
        "In computing, diff is a file comparison utility that outputs the differences between two files. It was developed in the early 1970s on the Unix operating system. Modern diff tools provide side-by-side comparison, syntax highlighting, and inline change markers to help users quickly identify modifications between text versions."
    ),
    "character-counter": (
        "Character_(computing)",
        "In computing, a character is a unit of information that roughly corresponds to a grapheme, a written symbol. Character counting is used to enforce length limits in social media posts, SMS messages, meta descriptions, and other text fields where maximum character counts apply. Different encoding standards define character boundaries differently."
    ),
    "typing-speed-test": (
        "Typing",
        "Typing is the process of writing or inputting text by pressing keys on a keyboard. Typing speed is commonly measured in words per minute (WPM), where a 'word' is standardized as five characters. Touch typing, where the typist uses muscle memory rather than sight to find keys, is the most efficient method and can achieve speeds exceeding 100 WPM."
    ),
    "typing-test": (
        "Words_per_minute",
        "Words per minute (WPM) is a measure of typing speed, commonly used in recruitment and education. The standard definition of a 'word' for typing purposes is five keystrokes, including spaces and punctuation. Professional typists typically achieve 65 to 75 WPM, while advanced typists can exceed 100 WPM. Typing tests measure both speed and accuracy."
    ),
    "word-scramble-solver": (
        "Anagram",
        "An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using each letter exactly once. Anagram solvers search through dictionaries to find valid words that can be formed from a given set of letters. They are commonly used in word games such as Scrabble, Words With Friends, and crossword puzzles."
    ),
    "text-generator": (
        "Natural_language_generation",
        "Natural language generation is a subfield of artificial intelligence and computational linguistics concerned with generating natural language text from structured data or other input. Text generators produce content for various purposes including placeholder text, test data, creative writing prompts, and automated content creation."
    ),
    "readability-checker": (
        "Readability",
        "Readability is the ease with which a reader can understand a written text. Readability formulas such as the Flesch-Kincaid grade level and the Gunning fog index estimate the years of education needed to understand a text on the first reading. These formulas typically analyze sentence length and word complexity to produce a numerical score."
    ),
    "headline-analyzer": (
        "Headline",
        "A headline is text indicating the nature of the content of the article below it. Headlines are used in newspapers, magazines, websites, and other media to attract attention and summarize the story. Headline analysis evaluates factors such as word balance, emotional impact, power words, and length to predict a headline's effectiveness in driving engagement."
    ),
    "text-to-speech": (
        "Speech_synthesis",
        "Speech synthesis is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer. Modern text-to-speech systems use deep learning and neural networks to produce natural-sounding speech from text input, supporting multiple languages, voices, and speaking styles."
    ),
    "text-case-converter": (
        "Letter_case",
        "Letter case is the distinction between uppercase (capital) and lowercase (minuscule) letters in the written representation of certain languages. Case conversion transforms text between different casing styles including UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, and kebab-case, each serving different conventions in writing and programming."
    ),

    # Generators
    "password-generator": (
        "Password_strength",
        "Password strength is a measure of the effectiveness of a password against guessing or brute-force attacks. A strong password is long, includes a mix of character types (uppercase, lowercase, numbers, symbols), and avoids common words or patterns. Password generators create random strings that maximize entropy, making them resistant to dictionary and brute-force attacks."
    ),
    "qr-code-generator": (
        "QR_code",
        "A QR code (Quick Response code) is a type of two-dimensional matrix barcode invented in 1994 by the Japanese company Denso Wave. QR codes store data using patterns of black and white squares arranged on a grid. They can encode URLs, text, contact information, and other data types, and can be scanned by smartphones and dedicated barcode readers."
    ),
    "color-palette-generator": (
        "Color_theory",
        "Color theory is the study of how colors interact and the visual effects of specific color combinations. It encompasses the color wheel, color harmony, and the psychological effects of color. Color palette generators use principles of color theory such as complementary, analogous, triadic, and split-complementary relationships to create aesthetically pleasing color schemes."
    ),
    "meme-generator": (
        "Internet_meme",
        "An internet meme is a cultural item of humor that is spread via the internet, primarily through social media platforms. Memes typically consist of an image with superimposed text, conveying a particular idea, joke, or cultural reference. The format has become a dominant form of online communication and cultural commentary."
    ),
    "instagram-font-generator": (
        "Unicode",
        "Unicode is an information technology standard for the consistent encoding, representation, and handling of text expressed in most of the world's writing systems. Instagram font generators leverage Unicode's extensive character set, using mathematical symbols, enclosed alphanumerics, and special script blocks to create stylized text that appears as decorative fonts when pasted into social media profiles."
    ),
    "resume-builder": (
        "R%C3%A9sum%C3%A9",
        "A resume (also spelled r\u00e9sum\u00e9) is a formal document that provides an overview of a person's professional qualifications, including work experience, education, skills, and achievements. It is used by job seekers to present their background to potential employers. Resume formatting and content conventions vary by industry and region."
    ),
    "invoice-generator": (
        "Invoice",
        "An invoice is a commercial document issued by a seller to a buyer relating to a sale transaction. It indicates the products, quantities, and agreed-upon prices for products or services the seller has provided. Invoices serve as a request for payment and provide a record of the transaction for both accounting and tax purposes."
    ),
    "favicon-generator": (
        "Favicon",
        "A favicon (short for favorite icon) is a small icon associated with a particular website or web page, displayed in the browser's address bar, tab, bookmarks, and other interface elements. Favicons are typically 16x16 or 32x32 pixels and are stored as ICO, PNG, or SVG files. They help users visually identify and distinguish between open tabs and bookmarked sites."
    ),
    "hash-generator": (
        "Hash_function",
        "A hash function is any function that can be used to map data of arbitrary size to fixed-size values. Cryptographic hash functions produce a deterministic, fixed-length output (digest) from any input, with the property that even small changes to the input produce dramatically different outputs. Common hash algorithms include MD5, SHA-1, SHA-256, and SHA-512."
    ),
    "uuid-generator": (
        "Universally_unique_identifier",
        "A universally unique identifier (UUID) is a 128-bit label used for information in computer systems. UUIDs are standardized by the Open Software Foundation and are designed to be unique across both space and time without requiring a central registration authority. They are commonly used as database primary keys, session identifiers, and distributed system identifiers."
    ),
    "barcode-generator": (
        "Barcode",
        "A barcode is a method of representing data in a visual, machine-readable form. Barcodes use varying widths and spacings of parallel lines (one-dimensional) or patterns of squares, dots, and other geometric patterns (two-dimensional) to encode information. They are used in retail, logistics, healthcare, and manufacturing for tracking products and automating data entry."
    ),
    "bcrypt-generator": (
        "Bcrypt",
        "Bcrypt is a password-hashing function designed by Niels Provos and David Maz\u00e8res based on the Blowfish cipher. It incorporates a salt to protect against rainbow table attacks and is adaptive, meaning the iteration count can be increased to make it slower as computational power increases. Bcrypt is widely recommended for securely storing passwords in databases."
    ),
    "number-generator": (
        "Random_number_generation",
        "Random number generation is the process of generating a sequence of numbers or symbols that cannot be reasonably predicted better than by chance. Random number generators are used in cryptography, simulation, statistical sampling, and games. Pseudorandom number generators use deterministic algorithms seeded with initial values to produce sequences that approximate true randomness."
    ),
    "random-number-generator": (
        "Random_number_generation",
        "Random number generation is the generation of a sequence of numbers or symbols that cannot be predicted better than by random chance. True random number generators derive randomness from physical phenomena, while pseudorandom generators use algorithms to produce sequences that approximate randomness. Applications include cryptography, gaming, simulations, and statistical sampling."
    ),
    "email-signature-generator": (
        "Email#Signature_block",
        "An email signature is a block of text appended to the end of an email message, typically containing the sender's name, title, company, contact information, and sometimes a company logo or legal disclaimer. Email signatures serve as digital business cards and help establish professional credibility. HTML-based signatures allow for rich formatting, images, and clickable links."
    ),
    "table-generator": (
        "Table_(information)",
        "A table is an arrangement of data in rows and columns, or possibly in a more complex structure. Tables are widely used in communication, research, and data analysis. In web development, HTML tables and Markdown tables structure content into a grid format, making it easy to compare and reference related data across multiple dimensions."
    ),
    "font-generator": (
        "Font",
        "A font is a set of printable or displayable text characters in a specific style and size. Fonts are classified into families such as serif, sans-serif, monospace, and display. Font generators allow users to preview, compare, and select typefaces for use in web design, graphic design, and document creation."
    ),
    "logo-maker": (
        "Logo",
        "A logo is a graphic mark, emblem, or symbol used to aid and promote public identification and recognition. It may be of an abstract or figurative design or include the text of the name it represents. Logos are fundamental to branding and corporate identity, serving as the most recognizable visual element of an organization."
    ),
    "icon-generator": (
        "Icon_(computing)",
        "In computing, an icon is a pictogram or ideogram displayed on a computer screen to help the user navigate a computer system. Icons are used in operating systems, applications, and websites to represent files, folders, programs, and actions. Icon generators create standardized icon sets at various sizes for use across platforms and devices."
    ),
    "ascii-art-generator": (
        "ASCII_art",
        "ASCII art is a graphic design technique that uses printable characters defined by the ASCII standard to create visual images. It originated in the era of typewriters and early computer terminals that could not display graphics. ASCII art ranges from simple emoticons to complex illustrations composed of letters, numbers, and symbols arranged on a text grid."
    ),

    # Education
    "flashcard-maker": (
        "Flashcard",
        "A flashcard is a card bearing information on both sides, used as an aid in memorization. Each flashcard typically has a question or term on one side and an answer or definition on the other. Flashcards employ active recall and spaced repetition, two evidence-based study techniques that significantly improve long-term memory retention."
    ),
    "apa-citation-generator": (
        "APA_style",
        "APA style is a set of guidelines for writing and formatting research papers established by the American Psychological Association. It defines rules for citations, references, headings, tables, and overall manuscript structure. APA citation format includes in-text citations with author and year, and a corresponding reference list entry with complete publication details."
    ),
    "apa-source-generator": (
        "APA_style",
        "APA style is a writing and citation format developed by the American Psychological Association, widely used in the social sciences, education, and business. The style specifies how sources should be cited both within the text and in the reference list. The 7th edition introduced updated guidelines for digital sources, DOIs, and online content."
    ),
    "essay-outline-generator": (
        "Essay",
        "An essay is a piece of writing that gives the author's own argument on a particular subject. Essays are commonly used in academic settings to assess understanding and critical thinking. A well-structured essay follows an outline consisting of an introduction with a thesis statement, body paragraphs with supporting evidence, and a conclusion that synthesizes the argument."
    ),
    "scientific-calculator": (
        "Scientific_calculator",
        "A scientific calculator is a type of electronic calculator designed to calculate problems in science, engineering, and mathematics. It supports operations beyond basic arithmetic, including trigonometric functions, logarithms, exponential functions, roots, factorials, permutations, and combinations. Scientific calculators follow the standard order of operations."
    ),
    "graphing-calculator": (
        "Graphing_calculator",
        "A graphing calculator is a handheld computer that is capable of plotting graphs, solving simultaneous equations, and performing other tasks with variables. Graphing calculators visualize mathematical functions as two-dimensional or three-dimensional plots, helping students and professionals understand the behavior and relationships of equations."
    ),
    "math-equation-solver": (
        "Equation",
        "An equation is a mathematical statement that asserts the equality of two expressions connected by the equals sign. Solving an equation involves finding the values of unknown variables that make the statement true. Common types include linear equations, quadratic equations, polynomial equations, and systems of equations."
    ),
    "mathematics-solver": (
        "Mathematics",
        "Mathematics is the study of numbers, shapes, quantities, and patterns. It provides tools for solving problems across science, engineering, finance, and everyday life. Mathematical problem-solving involves applying formulas, algorithms, and logical reasoning to find solutions to equations, inequalities, and other quantitative challenges."
    ),
    "plagiarism-checker": (
        "Plagiarism",
        "Plagiarism is the representation of another author's language, thoughts, ideas, or expressions as one's own original work. In academic and professional contexts, plagiarism is considered a serious ethical violation. Plagiarism detection tools compare submitted text against databases of published works, web content, and previously submitted documents to identify potentially unoriginal passages."
    ),

    # Lifestyle
    "pomodoro-timer": (
        "Pomodoro_Technique",
        "The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a kitchen timer to break work into intervals, typically 25 minutes in length, separated by short breaks. Each interval is known as a pomodoro, from the Italian word for tomato, after the tomato-shaped kitchen timer Cirillo used as a university student."
    ),
    "baby-name-generator": (
        "Given_name",
        "A given name is the part of a personal name that identifies a person, potentially with a middle name as well, and differentiates that person from the other members of a group who have a common surname. The choice of a given name is influenced by cultural traditions, family heritage, religious practices, and trends in name popularity."
    ),
    "stopwatch": (
        "Stopwatch",
        "A stopwatch is a timepiece designed to measure the amount of time that elapses between its activation and deactivation. Modern stopwatches measure time in hours, minutes, seconds, and fractions of a second with high precision. They are used in sports timing, scientific experiments, cooking, and any activity where accurate time measurement is required."
    ),
    "timezone-converter": (
        "Time_zone",
        "A time zone is an area that observes a uniform standard time for legal, commercial, and social purposes. Time zones tend to follow the boundaries of countries and their subdivisions instead of strictly following longitude. The world is divided into 24 primary time zones, each offset from Coordinated Universal Time (UTC) by a whole number of hours, though some zones are offset by 30 or 45 minutes."
    ),
    "calendar-generator": (
        "Calendar",
        "A calendar is a system of organizing days. This is done by giving names to periods of time, typically days, weeks, months, and years. The Gregorian calendar is the most widely used civil calendar, established by Pope Gregory XIII in 1582. Calendar generators create printable or digital calendars for planning, scheduling, and time management."
    ),
    "countdown-timer": (
        "Timer",
        "A timer is a specialized type of clock used for measuring specific time intervals. Countdown timers count down from a specified time to zero, often triggering an alert when the time expires. They are used in cooking, sports, presentations, productivity techniques, and any situation requiring awareness of remaining time."
    ),
    "discord-timestamp": (
        "Unix_time",
        "Unix time is a date and time representation widely used in computing. It measures time as the number of seconds that have elapsed since 00:00:00 UTC on January 1, 1970, known as the Unix epoch. Discord uses Unix timestamps in a special markdown syntax that automatically converts to each user's local time zone when displayed, ensuring consistent time communication across global communities."
    ),
    "metronome": (
        "Metronome",
        "A metronome is a device that produces an audible click or other sound at a regular interval that can be set by the user, typically measured in beats per minute (BPM). Musicians use metronomes to maintain a steady tempo during practice and performance. Johann Maelzel patented the first widely distributed metronome in 1815."
    ),
    "kanban-board": (
        "Kanban_board",
        "A Kanban board is a workflow visualization tool that enables users to optimize the flow of work. It uses cards and columns to represent work items and process stages, typically including 'To Do,' 'In Progress,' and 'Done.' Originating from Toyota's manufacturing system, Kanban has been widely adopted in software development and project management to limit work in progress and improve efficiency."
    ),
    "habit-tracker": (
        "Habit",
        "A habit is a routine of behavior that is repeated regularly and tends to occur subconsciously. Habit formation is the process by which behaviors become automatic through repeated practice. Research suggests that tracking habits increases adherence by providing visual feedback on consistency, leveraging psychological principles such as the mere measurement effect and the streak motivation."
    ),
    "mind-map-maker": (
        "Mind_map",
        "A mind map is a diagram used to visually organize information into a hierarchy, showing relationships among pieces of the whole. It is often created around a single concept, drawn as an image in the center, with associated ideas branching outward. Mind maps are used for brainstorming, planning, studying, and organizing complex information."
    ),
    "whiteboard": (
        "Whiteboard",
        "A whiteboard is a surface for nonpermanent markings, commonly used in education, business meetings, and creative brainstorming. Digital whiteboards replicate this experience on screens, offering additional features such as infinite canvas, shape tools, collaboration, and the ability to save and share content. They are widely used for remote teamwork and visual thinking."
    ),
    "flow-chart-maker": (
        "Flowchart",
        "A flowchart is a type of diagram that represents a workflow or process, showing the steps as boxes of various kinds connected by arrows indicating the sequence. Flowcharts are used in analyzing, designing, documenting, and managing processes in various fields. Standard symbols include rectangles for processes, diamonds for decisions, and parallelograms for input/output."
    ),
    "wireframe-tool": (
        "Website_wireframe",
        "A website wireframe is a visual guide that represents the skeletal framework of a website. Wireframes depict page layout, content placement, and functional elements without detailed design. They serve as blueprints during the early stages of web development, allowing designers and stakeholders to focus on structure and user experience before visual design begins."
    ),

    # Image tools
    "image-compressor": (
        "Image_compression",
        "Image compression is the application of data compression techniques to digital images to reduce their storage size and transmission bandwidth. Lossy compression methods such as JPEG reduce file size by discarding some image data, while lossless methods such as PNG preserve all original data. The choice between them depends on the acceptable trade-off between file size and image quality."
    ),
    "image-resizer": (
        "Image_scaling",
        "Image scaling is the process of resizing a digital image. Upscaling increases image dimensions while downscaling reduces them. Scaling algorithms such as bilinear interpolation, bicubic interpolation, and Lanczos resampling determine how pixel values are calculated at new positions, affecting the sharpness and quality of the resized image."
    ),
    "image-to-base64": (
        "Data_URI_scheme",
        "The data URI scheme is a uniform resource identifier (URI) scheme that provides a way to include data in-line in web pages as if they were external resources. Encoding images as Base64 data URIs allows them to be embedded directly in HTML and CSS files, eliminating additional HTTP requests and simplifying deployment of self-contained web pages."
    ),
    "placeholder-image": (
        "Placeholder_(computing)",
        "In computing, a placeholder is a temporary substitute for content that will eventually be replaced with final material. Placeholder images are used during web development and design to represent where actual images will be placed. They help maintain layout structure and proportions while final visual assets are being prepared or sourced."
    ),
    "pixel-art-editor": (
        "Pixel_art",
        "Pixel art is a form of digital art where images are edited at the pixel level. It originated from the limitations of early computer and video game graphics, where artists had to work within severe resolution and color constraints. Pixel art remains a popular aesthetic choice in indie games, digital illustration, and retro-inspired design."
    ),
    "gif-builder": (
        "GIF",
        "The Graphics Interchange Format (GIF) is a bitmap image format developed by CompuServe in 1987. GIF supports up to 8 bits per pixel, allowing a single image to reference a palette of up to 256 distinct colors. GIF's most notable feature is its support for animations, displaying a sequence of frames in a loop to create short, silent video-like clips."
    ),
    "video-to-gif": (
        "GIF",
        "The Graphics Interchange Format (GIF) is a bitmap image format that supports both static and animated images. Animated GIFs display a sequence of frames to create short, looping animations without requiring a video player. Converting video to GIF involves extracting frames at a specified interval, applying optional resizing and optimization, and encoding them into the GIF format."
    ),
    "screenshot-mockup": (
        "Mockup",
        "A mockup is a scale or full-size model of a design or device, used for teaching, demonstration, design evaluation, promotion, and other purposes. In web and app development, screenshot mockups place screenshots into realistic device frames (such as phones, laptops, or tablets) to present designs in a professional, contextual manner."
    ),
    "screenshot-to-code": (
        "Optical_character_recognition",
        "Optical character recognition (OCR) is the electronic conversion of images of text into machine-encoded text. Screenshot-to-code tools extend this concept by analyzing visual layouts and extracting not just text but structural information, converting a visual representation of a user interface into functional HTML, CSS, and other front-end code."
    ),
    "svg-editor": (
        "Scalable_Vector_Graphics",
        "Scalable Vector Graphics (SVG) is an XML-based vector image format for two-dimensional graphics with support for interactivity and animation. Unlike raster formats, SVG images are defined by mathematical expressions and can be scaled to any size without loss of quality. SVG editors provide tools for creating and manipulating paths, shapes, text, and other vector elements."
    ),
    "color-picker": (
        "Color_picker",
        "A color picker is a graphical user interface widget that allows users to select a color by adjusting values in one or more color models such as RGB, HSL, or HSV. Color pickers display a visual spectrum and allow precise input of color values. They are essential tools in graphic design, web development, and digital art for choosing and matching colors."
    ),
    "favicon-converter": (
        "Favicon",
        "A favicon is a small icon associated with a particular website, displayed in browser tabs, bookmarks, and address bars. Favicon converters transform standard image formats (PNG, JPEG, SVG) into the ICO format or generate multiple sizes required for different platforms and devices, including Apple touch icons and Android web app icons."
    ),

    # Internet/utility tools
    "internet-speed-checker": (
        "Internet_speed_test",
        "An internet speed test measures the bandwidth and latency of an internet connection. Speed tests work by downloading and uploading sample data between the user's device and a test server, measuring throughput in megabits per second (Mbps). Latency (ping) is measured in milliseconds and indicates the round-trip time for data to travel between the user and the server."
    ),
    "qr-reader": (
        "QR_code",
        "A QR code (Quick Response code) is a two-dimensional barcode that stores information in a grid of black and white squares. QR readers decode these patterns using a camera and image processing algorithms to extract the encoded data. Error correction built into the QR standard allows codes to be read even when partially damaged or obscured."
    ),
    "emoji-picker": (
        "Emoji",
        "An emoji is a pictograph, ideogram, or smiley embedded in text and used in electronic messages and web pages. The emoji encoding was introduced in Japanese mobile phone platforms in the late 1990s and later standardized in Unicode. There are now thousands of emoji covering expressions, objects, animals, food, activities, and symbols."
    ),
    "youtube-thumbnail": (
        "Thumbnail",
        "A thumbnail is a reduced-size version of an image or video used to help recognize and organize visual content. On YouTube, custom thumbnails serve as the primary visual element in search results and recommendations, significantly influencing click-through rates. Effective thumbnails use high contrast, readable text, expressive faces, and bold composition."
    ),
    "youtube-converter": (
        "YouTube",
        "YouTube is an American online video sharing and social media platform owned by Google. It allows users to upload, view, rate, share, and comment on videos. YouTube converters are tools that extract audio or video streams from YouTube content for offline use, though usage is subject to YouTube's terms of service."
    ),
    "ai-detector": (
        "AI-generated_text",
        "AI-generated text is content produced by artificial intelligence language models trained on large corpora of human-written text. AI detection tools analyze statistical patterns in text, such as perplexity and burstiness, to distinguish between human-written and machine-generated content. These tools are used in education, publishing, and content moderation to verify content authenticity."
    ),
    "ai-video-generator": (
        "Artificial_intelligence_art",
        "Artificial intelligence art refers to any artwork created with the assistance of artificial intelligence. AI video generators use deep learning models to create, edit, or transform video content based on text prompts or other inputs. These tools leverage techniques such as diffusion models, generative adversarial networks, and transformer architectures."
    ),
    "barcode-generator": (
        "Barcode",
        "A barcode is a method of representing data in a visual, machine-readable form. Linear barcodes use varying widths of parallel lines, while two-dimensional barcodes use patterns of squares and dots. Common barcode formats include UPC, EAN, Code 128, and Code 39, each designed for specific applications in retail, logistics, and inventory management."
    ),
}


def build_wiki_section(definition_text, wiki_article_slug):
    """Build the HTML section to inject."""
    wiki_url = f"https://en.wikipedia.org/wiki/{wiki_article_slug}"
    return f'''
<section class="wiki-definition" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;margin:2rem 0;">
  <h3 style="font-family:monospace;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:#8888a0;margin:0 0 1rem;">Background</h3>
  <p style="color:#c8c8d0;line-height:1.7;font-size:0.95rem;">{definition_text}</p>
  <cite style="display:block;margin-top:0.75rem;font-size:0.8rem;color:#666;">Source: <a href="{wiki_url}" target="_blank" rel="noopener" style="color:#00ccff;">Wikipedia</a></cite>
</section>
'''


def slug_to_topic(slug):
    """Derive a reasonable Wikipedia topic from a tool slug if not in mapping."""
    # Remove common suffixes
    name = slug.replace("-", " ")
    for suffix in ["tool", "maker", "builder", "tester", "checker", "viewer", "editor"]:
        if name.endswith(f" {suffix}"):
            name = name[: -(len(suffix) + 1)]
    # Capitalize for Wikipedia title format
    wiki_slug = name.replace(" ", "_")
    # Title case the definition
    definition = f"{name.title()} refers to the concept, tool, or process related to {name}. It is widely used in computing, productivity, and digital workflows to accomplish tasks efficiently."
    return wiki_slug, definition


def find_insertion_point(html):
    """Find the best place to insert the wiki section - before FAQ or before closing tags."""
    # Try: before FAQ section (various patterns)
    faq_patterns = [
        r'(<!-- FAQ[^>]*-->)',
        r'(<section[^>]*class="faq[^"]*"[^>]*>)',
        r'(<div[^>]*class="faq-section"[^>]*>)',
        r'(<h2[^>]*>Frequently Asked Questions</h2>)',
        r'(<h2[^>]*id="faq"[^>]*>[^<]*</h2>)',
    ]
    for pattern in faq_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.start()

    # Try: before </main>
    match = re.search(r'</main>', html, re.IGNORECASE)
    if match:
        return match.start()

    # Try: before </article>
    match = re.search(r'</article>', html, re.IGNORECASE)
    if match:
        return match.start()

    # Last resort: before </body>
    match = re.search(r'</body>', html, re.IGNORECASE)
    if match:
        return match.start()

    return None


def main():
    tool_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "*/index.html")))

    enhanced = 0
    skipped_has_wiki = 0
    skipped_no_insert = 0
    errors = 0
    enhanced_list = []

    for filepath in tool_dirs:
        slug = os.path.basename(os.path.dirname(filepath))

        # Read file
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            print(f"  ERROR reading {slug}: {e}")
            errors += 1
            continue

        # Skip if already has Wikipedia content
        if "wikipedia.org" in html:
            skipped_has_wiki += 1
            continue

        # Get wiki data
        if slug in WIKI_MAP:
            wiki_article, definition = WIKI_MAP[slug]
        else:
            wiki_article, definition = slug_to_topic(slug)
            print(f"  FALLBACK mapping for: {slug} -> {wiki_article}")

        # Build section
        section_html = build_wiki_section(definition, wiki_article)

        # Find insertion point
        insert_pos = find_insertion_point(html)
        if insert_pos is None:
            print(f"  SKIP {slug}: no suitable insertion point found")
            skipped_no_insert += 1
            continue

        # Insert the section
        new_html = html[:insert_pos] + section_html + "\n" + html[insert_pos:]

        # Write back
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_html)
            enhanced += 1
            enhanced_list.append(slug)
            print(f"  INJECTED: {slug}")
        except Exception as e:
            print(f"  ERROR writing {slug}: {e}")
            errors += 1

    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"  Total tool pages scanned:     {len(tool_dirs)}")
    print(f"  Already had Wikipedia:         {skipped_has_wiki}")
    print(f"  Enhanced (injected):           {enhanced}")
    print(f"  Skipped (no insertion point):  {skipped_no_insert}")
    print(f"  Errors:                        {errors}")
    print(f"\nEnhanced tools:")
    for s in enhanced_list:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
