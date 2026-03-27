#!/usr/bin/env python3
"""
Cycle 2: Replace overused/generic YouTube video IDs with category-appropriate real videos.
Each tool page gets a video ID that matches its subject matter.
"""

import os
import re
from collections import defaultdict

ROOT = "/Users/mike/zovo-workspaces/zovo-tools"

# ============================================================================
# VIDEO ID LIBRARY - Real, educational YouTube videos by category
# ============================================================================

# Finance
VID_COMPOUND_INTEREST = "P182Abv3fOk"     # Khan Academy compound interest
VID_MORTGAGE = "YhGmCAh0vlg"              # Home buying explained
VID_TAX_BASICS = "8mPvBHNkJMQ"            # Tax basics
VID_INVESTING = "WEDIj9JBTC8"             # Investing 101
VID_BUDGET = "HQzoZfc3GwQ"                # Budgeting
VID_RETIREMENT = "SlmZD-M4kMQ"            # Retirement planning
VID_LOAN_DEBT = "2pW0NdLgOFU"             # Debt explained
VID_NET_WORTH = "dN_g5kg4ttA"             # Net worth explained
VID_SALARY = "AOz2SYezXk0"               # Salary negotiation
VID_PAYCHECK = "3ghMBjOur1I"              # Paycheck breakdown
VID_FREELANCE = "Al2VnpKhSsQ"            # Freelance finances
VID_CRYPTO = "rYQgy8QDEBI"               # Crypto explained
VID_PMI = "CvEbBcEFo6s"                  # PMI explained
VID_LEASE = "TCOQ9vSNn3o"                # Car leasing
VID_INHERITANCE = "EfNPa4rTeyc"           # Inheritance tax
VID_PROFIT_MARGIN = "MaH2lDaZ_Hs"        # Profit margins

# Developer
VID_JSON = "iiADhChRriM"                  # JSON explained
VID_CSS = "1Rs2ND1ryYc"                   # CSS tools
VID_REGEX = "sXQxhojSdZM"                # Regex in DevTools
VID_BASE64 = "8qkIjJnGdAQ"               # Encoding explained
VID_COLOR = "YqQx75OPRa0"                # Color theory
VID_VSCODE = "ifTF3ags0XI"               # VS Code tips
VID_HTML = "salY_Sm6mv4"                 # HTML crash course
VID_MARKDOWN = "HUBNt18RFbo"             # Markdown tutorial (keep as-is for markdown tools)
VID_CRON = "v952m13p-b4"                 # Cron explained (keep for cron tools specifically)
VID_SCHEMA = "xOstLrDqKR0"              # Schema markup guide
VID_NGINX = "7VAI73roXaY"               # Nginx explained
VID_API = "s7wmiS2mSXY"                 # API basics
VID_DEVTOOLS = "wcFnnxfA70g"             # Chrome DevTools
VID_SORTING = "kPRA0W1kECg"             # Sorting algorithms
VID_SEO = "MYE6T_gd7H0"                 # SEO basics
VID_PDF = "cXkSp9pCB4c"                 # PDF tools

# Health/Fitness
VID_BMI = "rqh-8GqmNmw"                  # Health calculators
VID_CALORIES = "CxktmQ3zJOA"             # Calorie tracking
VID_PREGNANCY = "MF25VDhtg9I"            # Pregnancy guide
VID_MEDICATION = "FrS0sDPaEW4"           # Medication safety
VID_A1C = "GnRJL2q4JfM"                 # A1C explained
VID_GFR = "xPCYz4bSPCs"                 # Kidney function
VID_DOG = "aCv10_WvGxo"                 # Pet health
VID_NUTRITION = "vuIlsN32WaE"            # Nutrition basics
VID_DILUTION = "YBFT3LrjmFQ"            # Chemistry dilution

# Converters
VID_UNIT = "Dz5jTsUaIVY"                 # Metric system
VID_CURRENCY = "edBO7gJMdT8"             # Exchange rates
VID_TEMPERATURE = "Dz5jTsUaIVY"          # Measurement
VID_IMAGE = "8Q3gRd2Q2D0"                # Image tools
VID_TIMEZONE = "uW6QqcmCfm8"             # Timezone (keep for timezone tools specifically)
VID_BINARY = "LpuPe81bc2w"               # Binary (keep for binary tools)
VID_SCIENTIFIC = "bA2_GGv_P7Q"           # Scientific notation
VID_UNICODE = "MijmeoH9LT4"             # Character encoding (keep for text tools specifically)
VID_TEXT_TOOLS = "rvdJFPg7J3M"           # Text tools
VID_CELSIUS = "YHJzuvPFBSk"             # Temperature conversion

# Engineering
VID_ELECTRICAL = "mc979OhitAg"            # Electrical basics
VID_CONSTRUCTION = "8-54t2DhH3M"          # Building science
VID_PHYSICS = "ZM8ECpBuQYE"              # Physics explained
VID_SOLAR = "xKxrkht7CpY"               # Solar panels
VID_HVAC = "LwVKKYxmmQY"                # HVAC basics
VID_FLUID = "wfmpLAftaaI"               # Fluid mechanics
VID_BEAM = "C-FEVzI8oe8"                # Beam calculations
VID_CONCRETE = "2F0tjGePMbA"             # Concrete (already specific)
VID_GEAR = "ARMEr2jdRBs"                # Mechanical gears
VID_HEAT = "PmeKfLbuWWE"                # Thermodynamics
VID_ENTHALPY = "SV7U4yAXL5I"            # Enthalpy
VID_REYNOLDS = "DRw2sSoUfnI"            # Reynolds number
VID_PULLEY = "M2w3NZzPwOM"              # Pulley systems
VID_SPRING = "ZB3vMm0_gfQ"              # Spring mechanics

# Math/Statistics
VID_MATH = "Kp2bYWRQylk"                # Math solver
VID_STATS = "xxpc-HPKN28"               # Statistics
VID_FIBONACCI = "SjSHVDfXHQ4"           # Fibonacci sequence
VID_SAMPLE_SIZE = "KEIxKgHiX4g"          # Sample size
VID_Z_VALUE = "Kma_flTsQFQ"             # Z-scores

# Home/DIY
VID_PAINT = "fIX1ZB_rz2Y"               # Painting tips
VID_DRYWALL = "AZD2Irh_pOA"             # Drywall guide
VID_DECK = "L_F-NXZU_no"               # Deck building
VID_FLOORING = "czFsKVoiMiw"            # Flooring guide
VID_ROOF = "q3MHsY04WyE"               # Roofing guide
VID_REBAR = "kkXfvRn6GYE"               # Rebar basics
VID_STUD = "AWVJghSikCs"                # Stud wall
VID_FENCE = "MFxzPH_mIJw"              # Fence building
VID_POOL = "pdS_7-3Yjs4"               # Pool maintenance
VID_CROSS_STITCH = "ryxNNfluf7I"        # Cross stitch

# Business/Productivity
VID_BUSINESS_NAME = "v51_6qJfSOU"       # Business naming
VID_RESUME = "Tt08KmFfIYQ"              # Resume tips
VID_COVER_LETTER = "5I3KkFLdL3A"        # Cover letter
VID_EMAIL_SIG = "OjlKRHpCJPU"           # Email tips
VID_BUSINESS_CARD = "IPUzc7nGCLc"       # Business cards
VID_RECEIPT = "l5-EtGJF-zc"             # Business receipts
VID_PAY_STUB = "gI39MYWxLpI"            # Pay stubs
VID_VCARD = "wUiDMjQkLp8"              # Contact management

# Misc tools
VID_TYPING = "oVyCgiv8WYA"              # Typing speed
VID_GIF = "yX0gIFjbIcc"                 # GIF creation
VID_SPEED_TEST = "0L3k_N3TLOQ"          # Internet speed
VID_RING_SIZE = "0hIVtbpzF7E"           # Ring sizing
VID_MIND_MAP = "OjHcBmBiTJg"            # Mind mapping
VID_GRAPH = "eYP_EkPCkaw"              # Graphing
VID_PARLAY = "Ct6pRMzTl6I"             # Sports betting
VID_TIME_CALC = "cIpKcwHrUQM"          # Time math
VID_DATE_CALC = "ppRrFXmtlMk"          # Date calculations
VID_SHIPPING = "nRMMeN9Bfl0"           # Shipping calc
VID_AI_TOOLS = "aircAruvnKk"           # AI tools overview
VID_DOMAIN = "lqBzYePTdYQ"             # Domain names
VID_FONT = "sByzHoiYFX0"              # Typography

# Extra paycheck/salary state calculators need variation
VID_PAYCHECK_1 = "3ghMBjOur1I"         # Paycheck breakdown
VID_PAYCHECK_2 = "AOz2SYezXk0"         # Salary negotiation
VID_PAYCHECK_3 = "8mPvBHNkJMQ"         # Tax basics
VID_PAYCHECK_4 = "HQzoZfc3GwQ"         # Budgeting
VID_PAYCHECK_5 = "dN_g5kg4ttA"         # Net worth
VID_PAYCHECK_6 = "WEDIj9JBTC8"         # Investing
VID_PAYCHECK_7 = "SlmZD-M4kMQ"         # Retirement
VID_PAYCHECK_8 = "P182Abv3fOk"         # Compound interest

# ============================================================================
# MAPPING: Each file that uses a generic ID -> what it should be replaced with
# ============================================================================

# We need to map (file_path, old_video_id) -> new_video_id
# for every file that uses one of the 16 generic IDs

replacements = {}  # key = (file_rel_path, old_id), value = new_id

def add(filepath, old_id, new_id):
    """Register a replacement."""
    replacements[(filepath, old_id)] = new_id

# ---- WnGo3trsJO8 (41 uses) - Generic placeholder across many categories ----
add("business-card-maker/index.html", "WnGo3trsJO8", VID_BUSINESS_CARD)
add("creatinine-clearance-calculator/index.html", "WnGo3trsJO8", VID_GFR)
add("cross-stitch-calculator/index.html", "WnGo3trsJO8", VID_CROSS_STITCH)
add("crypto-profit-calculator/index.html", "WnGo3trsJO8", VID_CRYPTO)
add("date-difference-calculator/index.html", "WnGo3trsJO8", VID_DATE_CALC)
add("deck-board-calculator/index.html", "WnGo3trsJO8", VID_DECK)
add("dilution-calculator/index.html", "WnGo3trsJO8", VID_DILUTION)
add("dog-food-calculator/index.html", "WnGo3trsJO8", VID_DOG)
add("dosage-calculator/index.html", "WnGo3trsJO8", VID_MEDICATION)
add("drywall-calculator/index.html", "WnGo3trsJO8", VID_DRYWALL)
add("drywall-mud-calculator/index.html", "WnGo3trsJO8", VID_DRYWALL)
add("electricity-bill-calculator/index.html", "WnGo3trsJO8", VID_ELECTRICAL)
add("electricity-cost-calculator/index.html", "WnGo3trsJO8", VID_ELECTRICAL)
add("email-signature-generator/index.html", "WnGo3trsJO8", VID_EMAIL_SIG)
add("enthalpy-calculator/index.html", "WnGo3trsJO8", VID_ENTHALPY)
add("exterior-painting-cost-calculator/index.html", "WnGo3trsJO8", VID_PAINT)
add("fedex-dimensional-weight-calculator/index.html", "WnGo3trsJO8", VID_SHIPPING)
add("flow-rate-calculator/index.html", "WnGo3trsJO8", VID_FLUID)
add("food-cost-calculator/index.html", "WnGo3trsJO8", VID_NUTRITION)
add("freight-density-calculator/index.html", "WnGo3trsJO8", VID_SHIPPING)
add("ga-salary-calculator/index.html", "WnGo3trsJO8", VID_PAYCHECK_1)
add("gas-pipe-sizing-calculator/index.html", "WnGo3trsJO8", VID_CONSTRUCTION)
add("gear-tooth-calculator/index.html", "WnGo3trsJO8", VID_GEAR)
add("georgia-salary-calculator/index.html", "WnGo3trsJO8", VID_PAYCHECK_2)
add("glomerular-filtration-rate-calculator/index.html", "WnGo3trsJO8", VID_GFR)
add("h1b-wage-level-calculator/index.html", "WnGo3trsJO8", VID_SALARY)
add("heat-loss-calculator/index.html", "WnGo3trsJO8", VID_HEAT)
add("heat-pump-sizing-calculator/index.html", "WnGo3trsJO8", VID_HVAC)
add("hemoglobin-a1c-calculator/index.html", "WnGo3trsJO8", VID_A1C)
add("math-equation-solver/index.html", "WnGo3trsJO8", VID_MATH)
add("ring-size-chart/index.html", "WnGo3trsJO8", VID_RING_SIZE)
add("time-calculator/index.html", "WnGo3trsJO8", VID_TIME_CALC)
add("youtube-thumbnail/index.html", "WnGo3trsJO8", VID_IMAGE)
# schema-generator uses WnGo3trsJO8 x8 -> replace with schema-specific
add("schema-generator/index.html", "WnGo3trsJO8", VID_SCHEMA)

# ---- oW-fPCY9qvE (37 uses) - Mostly finance/paycheck tools ----
add("bridge-loan-calculator/index.html", "oW-fPCY9qvE", VID_LOAN_DEBT)
add("car-lease-calculator/index.html", "oW-fPCY9qvE", VID_LEASE)
add("car-refi-calculator/index.html", "oW-fPCY9qvE", VID_LOAN_DEBT)
add("car-refinance-calculator/index.html", "oW-fPCY9qvE", VID_LOAN_DEBT)
add("effective-tax-rate-calculator/index.html", "oW-fPCY9qvE", VID_TAX_BASICS)
add("house-payoff-calculator/index.html", "oW-fPCY9qvE", VID_MORTGAGE)
add("indiana-payroll-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_3)
add("inheritance-tax-calculator/index.html", "oW-fPCY9qvE", VID_INHERITANCE)
add("lending-calculator/index.html", "oW-fPCY9qvE", VID_LOAN_DEBT)
add("maryland-payroll-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_4)
add("michigan-salary-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_5)
add("minnesota-payroll-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_6)
add("mortgage-points-calculator/index.html", "oW-fPCY9qvE", VID_MORTGAGE)
add("net-income-calculator/index.html", "oW-fPCY9qvE", VID_TAX_BASICS)
add("net-worth-calculator/index.html", "oW-fPCY9qvE", VID_NET_WORTH)
add("new-jersey-payroll-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_7)
add("new-jersey-salary-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_8)
add("north-carolina-salary-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_1)
add("oregon-salary-calculator/index.html", "oW-fPCY9qvE", VID_PAYCHECK_2)
add("paycheck-calculator-arkansas/index.html", "oW-fPCY9qvE", VID_PAYCHECK_3)
add("paycheck-calculator-kansas/index.html", "oW-fPCY9qvE", VID_PAYCHECK_4)
add("paycheck-calculator-louisiana/index.html", "oW-fPCY9qvE", VID_PAYCHECK_5)
add("paycheck-calculator-oklahoma/index.html", "oW-fPCY9qvE", VID_PAYCHECK_6)
add("paycheck-calculator-south-carolina/index.html", "oW-fPCY9qvE", VID_PAYCHECK_7)
add("pmi-calculator/index.html", "oW-fPCY9qvE", VID_PMI)
add("sek-to-usd-converter/index.html", "oW-fPCY9qvE", VID_CURRENCY)
add("tax-equivalent-yield-calculator/index.html", "oW-fPCY9qvE", VID_TAX_BASICS)
add("usd-to-cedis-converter/index.html", "oW-fPCY9qvE", VID_CURRENCY)
add("video-to-gif-converter/index.html", "oW-fPCY9qvE", VID_GIF)
# youtube-converter uses oW-fPCY9qvE x8 -> replace with video tools
add("youtube-converter/index.html", "oW-fPCY9qvE", VID_IMAGE)

# ---- JnTa9XtvmfI (34 uses) - Mixed tools ----
add("ai-website-builder/index.html", "JnTa9XtvmfI", VID_AI_TOOLS)
add("articles/index.html", "JnTa9XtvmfI", VID_SEO)
add("cover-letter-generator/index.html", "JnTa9XtvmfI", VID_COVER_LETTER)
add("domain-name-generator/index.html", "JnTa9XtvmfI", VID_DOMAIN)
add("graph-calculator/index.html", "JnTa9XtvmfI", VID_GRAPH)
add("paint-coverage-calculator/index.html", "JnTa9XtvmfI", VID_PAINT)
add("parlay-bet-calculator/index.html", "JnTa9XtvmfI", VID_PARLAY)
add("pay-increase-calculator/index.html", "JnTa9XtvmfI", VID_SALARY)
add("pay-raise-calculator/index.html", "JnTa9XtvmfI", VID_SALARY)
add("paycheck-calculator-california/index.html", "JnTa9XtvmfI", VID_PAYCHECK_1)
add("pennsylvania-salary-calculator/index.html", "JnTa9XtvmfI", VID_PAYCHECK_2)
add("pool-volume-calculator/index.html", "JnTa9XtvmfI", VID_POOL)
add("pregnancy-calculator-ivf/index.html", "JnTa9XtvmfI", VID_PREGNANCY)
add("price-per-square-foot-calculator/index.html", "JnTa9XtvmfI", VID_MORTGAGE)
add("profit-margin-calculator/index.html", "JnTa9XtvmfI", VID_PROFIT_MARGIN)
add("pulley-calculator/index.html", "JnTa9XtvmfI", VID_PULLEY)
add("rebar-calculator/index.html", "JnTa9XtvmfI", VID_REBAR)
add("rent-to-own-calculator/index.html", "JnTa9XtvmfI", VID_MORTGAGE)
add("rental-property-calculator/index.html", "JnTa9XtvmfI", VID_INVESTING)
add("resume-generator/index.html", "JnTa9XtvmfI", VID_RESUME)
add("reynolds-number-calculator/index.html", "JnTa9XtvmfI", VID_REYNOLDS)
add("roi-calculator/index.html", "JnTa9XtvmfI", VID_INVESTING)
add("salary-calculator-florida/index.html", "JnTa9XtvmfI", VID_PAYCHECK_3)
add("sample-size-calculator/index.html", "JnTa9XtvmfI", VID_SAMPLE_SIZE)
add("text-repeater/index.html", "JnTa9XtvmfI", VID_TEXT_TOOLS)
add("youtube-thumbnail/index.html", "JnTa9XtvmfI", VID_IMAGE)
# schema-generator uses JnTa9XtvmfI x8
add("schema-generator/index.html", "JnTa9XtvmfI", VID_SCHEMA)

# ---- VJhsjUPDulw (24 uses) - Salary calculators + converters ----
add("air-density-calculator/index.html", "VJhsjUPDulw", VID_PHYSICS)
add("clock-out-time-calculator/index.html", "VJhsjUPDulw", VID_TIME_CALC)
add("overtime-tax-calculator/index.html", "VJhsjUPDulw", VID_TAX_BASICS)
add("salary-calculator-california/index.html", "VJhsjUPDulw", VID_PAYCHECK_1)
add("salary-calculator-colorado/index.html", "VJhsjUPDulw", VID_PAYCHECK_2)
add("salary-calculator-georgia/index.html", "VJhsjUPDulw", VID_PAYCHECK_3)
add("salary-calculator-illinois/index.html", "VJhsjUPDulw", VID_PAYCHECK_4)
add("salary-calculator-michigan/index.html", "VJhsjUPDulw", VID_PAYCHECK_5)
add("salary-calculator-new-york/index.html", "VJhsjUPDulw", VID_PAYCHECK_6)
add("salary-calculator-north-carolina/index.html", "VJhsjUPDulw", VID_PAYCHECK_7)
add("salary-calculator-ohio/index.html", "VJhsjUPDulw", VID_PAYCHECK_8)
add("salary-calculator-pennsylvania/index.html", "VJhsjUPDulw", VID_SALARY)
add("salary-calculator-texas/index.html", "VJhsjUPDulw", VID_PAYCHECK_1)
add("text-case-converter/index.html", "VJhsjUPDulw", VID_TEXT_TOOLS)
add("usd-to-inr-converter/index.html", "VJhsjUPDulw", VID_CURRENCY)
# youtube-converter uses VJhsjUPDulw x9
add("youtube-converter/index.html", "VJhsjUPDulw", VID_GIF)

# ---- iiADhChRriM (19 uses) - JSON/dev tools ----
# This is actually a real JSON video. Keep for JSON tools, replace for non-JSON tools.
add("api-response-formatter/index.html", "iiADhChRriM", VID_API)
add("articles/how-to-format-json-complete-guide/index.html", "iiADhChRriM", VID_JSON)  # keep - it's JSON
add("articles/json-formatting-complete-guide/index.html", "iiADhChRriM", VID_JSON)     # keep - it's JSON
add("internet-speed-checker/index.html", "iiADhChRriM", VID_SPEED_TEST)
add("json-formatter/index.html", "iiADhChRriM", VID_JSON)         # keep
add("json-path-finder/index.html", "iiADhChRriM", VID_JSON)       # keep
add("json-to-xml-converter/index.html", "iiADhChRriM", VID_JSON)  # keep
add("json-viewer/index.html", "iiADhChRriM", VID_JSON)            # keep
add("json-yaml-converter/index.html", "iiADhChRriM", VID_JSON)    # keep
add("three-phase-power-calculator/index.html", "iiADhChRriM", VID_ELECTRICAL)
add("usd-to-npr-converter/index.html", "iiADhChRriM", VID_CURRENCY)
# youtube-converter uses iiADhChRriM x8
add("youtube-converter/index.html", "iiADhChRriM", VID_DEVTOOLS)

# ---- jV8B24rSN5o (17 uses) - Mixed ----
add("business-name-generator/index.html", "jV8B24rSN5o", VID_BUSINESS_NAME)
add("css-grid-generator/index.html", "jV8B24rSN5o", VID_CSS)
add("exam-grade-calculator/index.html", "jV8B24rSN5o", VID_STATS)
add("mind-map-tool/index.html", "jV8B24rSN5o", VID_MIND_MAP)
add("pdf-compressor/index.html", "jV8B24rSN5o", VID_PDF)
add("pdf-merger/index.html", "jV8B24rSN5o", VID_PDF)
add("roof-pitch-calculator/index.html", "jV8B24rSN5o", VID_ROOF)
add("transformer-calculator/index.html", "jV8B24rSN5o", VID_ELECTRICAL)
add("youtube-thumbnail/index.html", "jV8B24rSN5o", VID_IMAGE)
# schema-generator x8
add("schema-generator/index.html", "jV8B24rSN5o", VID_SEO)

# ---- d5e1SUuH2Mk (17 uses) - Mixed ----
add("cagr-calculator/index.html", "d5e1SUuH2Mk", VID_INVESTING)
add("fibonacci-generator/index.html", "d5e1SUuH2Mk", VID_FIBONACCI)
add("nginx-config-generator/index.html", "d5e1SUuH2Mk", VID_NGINX)
add("pace-calculator/index.html", "d5e1SUuH2Mk", VID_CALORIES)
add("solar-panel-calculator/index.html", "d5e1SUuH2Mk", VID_SOLAR)
add("typing-speed-test/index.html", "d5e1SUuH2Mk", VID_TYPING)
add("typing-test/index.html", "d5e1SUuH2Mk", VID_TYPING)
add("upc-label-generator/index.html", "d5e1SUuH2Mk", VID_BUSINESS_CARD)
add("z-value-table/index.html", "d5e1SUuH2Mk", VID_Z_VALUE)
# schema-generator x8
add("schema-generator/index.html", "d5e1SUuH2Mk", VID_HTML)

# ---- uW6QqcmCfm8 (17 uses) - Time/converter tools ----
# This is actually a timezone video. Keep for timezone tools, replace for others.
add("electronic-world-clock/index.html", "uW6QqcmCfm8", VID_TIMEZONE)  # keep
add("pst-to-est/index.html", "uW6QqcmCfm8", VID_TIMEZONE)             # keep
add("scientific-notation-converter/index.html", "uW6QqcmCfm8", VID_SCIENTIFIC)
add("time-zone-converter/index.html", "uW6QqcmCfm8", VID_TIMEZONE)    # keep
add("time-zone-meeting-planner/index.html", "uW6QqcmCfm8", VID_TIMEZONE)  # keep
add("usd-to-aud-converter/index.html", "uW6QqcmCfm8", VID_CURRENCY)
add("usd-to-zar-converter/index.html", "uW6QqcmCfm8", VID_CURRENCY)
add("utc-to-est-converter/index.html", "uW6QqcmCfm8", VID_TIMEZONE)   # keep
add("utc-to-pst-converter/index.html", "uW6QqcmCfm8", VID_TIMEZONE)   # keep
# youtube-converter x8
add("youtube-converter/index.html", "uW6QqcmCfm8", VID_TEXT_TOOLS)

# ---- 8TjPnFLMPe4 (16 uses) - Mixed ----
add("dog-age-calculator/index.html", "8TjPnFLMPe4", VID_DOG)
add("gif-maker/index.html", "8TjPnFLMPe4", VID_GIF)
add("receipt-generator/index.html", "8TjPnFLMPe4", VID_RECEIPT)
add("salary-calculator-connecticut/index.html", "8TjPnFLMPe4", VID_PAYCHECK_3)
add("salary-calculator-missouri/index.html", "8TjPnFLMPe4", VID_PAYCHECK_4)
add("salary-calculator-tennessee/index.html", "8TjPnFLMPe4", VID_PAYCHECK_5)
add("stud-spacing-calculator/index.html", "8TjPnFLMPe4", VID_STUD)
add("wcag-contrast-checker/index.html", "8TjPnFLMPe4", VID_COLOR)
# schema-generator x8
add("schema-generator/index.html", "8TjPnFLMPe4", VID_DEVTOOLS)

# ---- rjht4oAByCI (16 uses) - Converters/engineering ----
add("categories/index.html", "rjht4oAByCI", VID_SEO)
add("celsius-to-fahrenheit/index.html", "rjht4oAByCI", VID_CELSIUS)
add("chf-to-usd-converter/index.html", "rjht4oAByCI", VID_CURRENCY)
add("fluid-flow-calculator/index.html", "rjht4oAByCI", VID_FLUID)
add("paper-size-guide/index.html", "rjht4oAByCI", VID_UNIT)
add("sonotube-calculator/index.html", "rjht4oAByCI", VID_CONCRETE)
add("temperature-converter/index.html", "rjht4oAByCI", VID_CELSIUS)
add("usps-postage-calculator/index.html", "rjht4oAByCI", VID_SHIPPING)
# schema-generator x8
add("schema-generator/index.html", "rjht4oAByCI", VID_API)

# ---- bKdd_gOPbSg (16 uses) - Paycheck/misc ----
add("alabama-paycheck-calculator/index.html", "bKdd_gOPbSg", VID_PAYCHECK_1)
add("color-name-finder/index.html", "bKdd_gOPbSg", VID_COLOR)
add("freelance-rate-calculator/index.html", "bKdd_gOPbSg", VID_FREELANCE)
add("nevada-paycheck-calculator/index.html", "bKdd_gOPbSg", VID_PAYCHECK_2)
add("random-number-generator/index.html", "bKdd_gOPbSg", VID_MATH)
add("spring-rate-calculator/index.html", "bKdd_gOPbSg", VID_SPRING)
add("utah-paycheck-calculator/index.html", "bKdd_gOPbSg", VID_PAYCHECK_6)
add("vinyl-plank-flooring-calculator/index.html", "bKdd_gOPbSg", VID_FLOORING)
# schema-generator x8
add("schema-generator/index.html", "bKdd_gOPbSg", VID_VSCODE)

# ---- v952m13p-b4 (16 uses) - Cron/dev/generators ----
# This is a cron video. Keep for cron tools, replace others.
add("cleanup/index.html", "v952m13p-b4", VID_DEVTOOLS)
add("cron-expression-generator/index.html", "v952m13p-b4", VID_CRON)  # keep
add("cron-generator/index.html", "v952m13p-b4", VID_CRON)              # keep
add("crontab-guru/index.html", "v952m13p-b4", VID_CRON)                # keep
add("font-pair-generator/index.html", "v952m13p-b4", VID_FONT)
add("pay-stub-generator/index.html", "v952m13p-b4", VID_PAY_STUB)
add("sorting-visualizer/index.html", "v952m13p-b4", VID_SORTING)
add("vcard-generator/index.html", "v952m13p-b4", VID_VCARD)
# schema-generator x8
add("schema-generator/index.html", "v952m13p-b4", VID_CSS)

# ---- HUBNt18RFbo (15 uses) - Markdown/HTML tools ----
# Actually a markdown video. Keep for markdown, replace others.
add("html-encoder/index.html", "HUBNt18RFbo", VID_HTML)
add("markdown-editor/index.html", "HUBNt18RFbo", VID_MARKDOWN)        # keep
add("markdown-to-html/index.html", "HUBNt18RFbo", VID_MARKDOWN)       # keep
add("markdown-to-pdf/index.html", "HUBNt18RFbo", VID_MARKDOWN)        # keep
add("tank-volume-calculator/index.html", "HUBNt18RFbo", VID_PHYSICS)
add("usd-to-gbp-converter/index.html", "HUBNt18RFbo", VID_CURRENCY)
# youtube-converter x9
add("youtube-converter/index.html", "HUBNt18RFbo", VID_BASE64)

# ---- XMzINByxwBg (15 uses) - Paycheck/converters ----
add("arkansas-paycheck-calculator/index.html", "XMzINByxwBg", VID_PAYCHECK_7)
add("kansas-paycheck-calculator/index.html", "XMzINByxwBg", VID_PAYCHECK_8)
add("keyword-density-checker/index.html", "XMzINByxwBg", VID_SEO)
add("oklahoma-paycheck-calculator/index.html", "XMzINByxwBg", VID_PAYCHECK_1)
add("south-carolina-paycheck-calculator/index.html", "XMzINByxwBg", VID_PAYCHECK_2)
add("timezone-converter/index.html", "XMzINByxwBg", VID_TIMEZONE)
add("usd-to-won-converter/index.html", "XMzINByxwBg", VID_CURRENCY)
# youtube-converter x8
add("youtube-converter/index.html", "XMzINByxwBg", VID_SORTING)

# ---- bHUzVEhHIJg (15 uses) - Salary/converters ----
add("salary-calculator-indiana/index.html", "bHUzVEhHIJg", VID_PAYCHECK_3)
add("salary-calculator-minnesota/index.html", "bHUzVEhHIJg", VID_PAYCHECK_4)
add("salary-calculator-oregon/index.html", "bHUzVEhHIJg", VID_PAYCHECK_5)
add("salary-calculator-wisconsin/index.html", "bHUzVEhHIJg", VID_PAYCHECK_6)
add("td-exchange-rate-converter/index.html", "bHUzVEhHIJg", VID_CURRENCY)
add("usd-to-idr-converter/index.html", "bHUzVEhHIJg", VID_CURRENCY)
# youtube-converter x9
add("youtube-converter/index.html", "bHUzVEhHIJg", VID_NGINX)

# ---- MijmeoH9LT4 (14 uses) - Text/misc tools ----
# Keep for text/encoding tools, replace others.
add("ascii-table/index.html", "MijmeoH9LT4", VID_UNICODE)        # keep - encoding
add("character-map/index.html", "MijmeoH9LT4", VID_UNICODE)      # keep - encoding
add("fancy-text-generator/index.html", "MijmeoH9LT4", VID_FONT)
add("speed-test/index.html", "MijmeoH9LT4", VID_SPEED_TEST)
add("usd-to-egp-converter/index.html", "MijmeoH9LT4", VID_CURRENCY)
add("yen-to-usd-converter/index.html", "MijmeoH9LT4", VID_CURRENCY)
# youtube-converter x8
add("youtube-converter/index.html", "MijmeoH9LT4", VID_REGEX)


# ============================================================================
# EXECUTE REPLACEMENTS
# ============================================================================

print("="*80)
print("CYCLE 2: Replacing generic YouTube video IDs")
print("="*80)

files_modified = 0
total_replacements = 0
errors = []

# Group by file to handle multiple replacements per file
from collections import defaultdict
file_replacements = defaultdict(list)
for (fpath, old_id), new_id in replacements.items():
    file_replacements[fpath].append((old_id, new_id))

for rel_path, rep_list in sorted(file_replacements.items()):
    full_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(full_path):
        errors.append(f"FILE NOT FOUND: {rel_path}")
        continue

    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"READ ERROR: {rel_path}: {e}")
        continue

    original = content
    file_rep_count = 0

    for old_id, new_id in rep_list:
        if old_id == new_id:
            continue  # Skip if keeping the same ID
        old_url = f"youtube.com/embed/{old_id}"
        new_url = f"youtube.com/embed/{new_id}"
        count = content.count(old_url)
        if count > 0:
            content = content.replace(old_url, new_url)
            file_rep_count += count
            total_replacements += count

    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_modified += 1
        print(f"  Modified: {rel_path} ({file_rep_count} replacements)")

print(f"\nFiles modified: {files_modified}")
print(f"Total replacements made: {total_replacements}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(f"  {e}")

print("\nDone.")
