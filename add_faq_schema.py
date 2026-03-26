#!/usr/bin/env python3
"""Add FAQPage JSON-LD schema to tools that are missing it."""

import re
import json
import os

# FAQ data for each tool - 5 specific, domain-relevant questions each
TOOL_FAQS = {
    "a1c-calculator": [
        ("What is A1C and what does it measure?", "A1C (also called HbA1c or glycated hemoglobin) is a blood test that measures your average blood sugar level over the past 2 to 3 months. It reflects the percentage of hemoglobin proteins in your red blood cells that have glucose attached to them."),
        ("What A1C level is considered normal?", "A normal A1C level is below 5.7%. An A1C between 5.7% and 6.4% indicates prediabetes, while an A1C of 6.5% or higher on two separate tests indicates diabetes."),
        ("How do you convert A1C to estimated average glucose?", "The formula to convert A1C to estimated average glucose (eAG) in mg/dL is: eAG = 28.7 x A1C - 46.7. For example, an A1C of 7% equals an eAG of approximately 154 mg/dL."),
        ("How often should you get an A1C test?", "For people without diabetes, an A1C test every 3 years is generally recommended after age 45. For people with diabetes, testing every 3 to 6 months is typical, depending on how well blood sugar is controlled."),
        ("Can A1C results be inaccurate?", "Yes, certain conditions can affect A1C accuracy, including iron deficiency anemia, kidney disease, recent blood transfusions, sickle cell disease, and some hemoglobin variants. In these cases, your doctor may use alternative tests.")
    ],
    "annuity-calculator": [
        ("What is an annuity?", "An annuity is a financial product that provides a series of regular payments over a specified period or for a lifetime. Annuities are typically purchased from insurance companies and can be used for retirement income planning."),
        ("What is the difference between an immediate and deferred annuity?", "An immediate annuity begins making payments shortly after purchase, usually within one year. A deferred annuity accumulates funds during a growth phase before payments begin at a future date you specify."),
        ("How is the present value of an annuity calculated?", "The present value of an annuity is calculated using the formula PV = PMT x [(1 - (1 + r)^-n) / r], where PMT is the payment amount, r is the interest rate per period, and n is the total number of periods."),
        ("What is a fixed annuity vs a variable annuity?", "A fixed annuity guarantees a specific interest rate and predictable payments. A variable annuity ties returns to the performance of investment sub-accounts, meaning payments can fluctuate based on market conditions."),
        ("Are annuity payments taxable?", "Annuity taxation depends on how the annuity was funded. If purchased with pre-tax dollars (like from a 401k), the entire payment is taxable. If purchased with after-tax dollars, only the earnings portion of each payment is taxed.")
    ],
    "army-fitness-calculator": [
        ("What is the Army Combat Fitness Test (ACFT)?", "The ACFT is the U.S. Army's official physical fitness test consisting of six events: the 3 Repetition Maximum Deadlift, Standing Power Throw, Hand Release Push-Up, Sprint-Drag-Carry, Leg Tuck or Plank, and 2-Mile Run."),
        ("What is the minimum passing score on the ACFT?", "The minimum passing score on the ACFT is 60 points per event, for a total minimum score of 360 out of a possible 600 points. Each event is scored on a 0-100 point scale."),
        ("How does the Army tape test measure body fat?", "The Army tape test measures body fat by taking circumference measurements at specific body locations. For men, measurements are taken at the neck and abdomen. For women, measurements are taken at the neck, waist, and hips."),
        ("What are the Army body fat percentage standards?", "Maximum allowable body fat percentages vary by age. For men ages 17-20 it is 20%, ages 21-27 it is 22%, ages 28-39 it is 24%, and ages 40+ it is 26%. For women, the limits are 30%, 32%, 34%, and 36% respectively."),
        ("How often do soldiers take the ACFT?", "Soldiers are required to take the ACFT at least twice per year. The test became the official Army fitness test in October 2022, replacing the Army Physical Fitness Test (APFT).")
    ],
    "audio-converter": [
        ("What audio formats can be converted online?", "Common audio formats that can be converted include MP3, WAV, FLAC, AAC, OGG, WMA, and M4A. Each format has different characteristics for quality, file size, and compatibility."),
        ("Does converting audio reduce sound quality?", "Converting between lossy formats (like MP3 to AAC) can reduce quality because each compression step discards data. Converting from a lossless format (like FLAC or WAV) to a lossy format preserves maximum quality for that codec."),
        ("What is the difference between lossy and lossless audio?", "Lossy formats like MP3 and AAC compress audio by permanently removing data that is less perceptible to human hearing, resulting in smaller files. Lossless formats like FLAC and WAV preserve all original audio data with no quality loss."),
        ("What bitrate should I use for MP3 conversion?", "For general listening, 128 kbps is acceptable quality. For higher quality, 192 kbps is a good balance of quality and file size. For near-CD quality, use 320 kbps, which is the maximum bitrate for MP3."),
        ("Is it safe to convert audio files in a browser?", "Yes, browser-based audio converters that process files locally on your device are safe because your audio files never leave your computer. The conversion happens entirely in your browser using JavaScript.")
    ],
    "baby-percentile-calculator": [
        ("What does a baby's growth percentile mean?", "A growth percentile shows how your baby's measurements compare to other children of the same age and sex. For example, if your baby is at the 75th percentile for weight, it means 75% of babies that age weigh less and 25% weigh more."),
        ("What is the difference between WHO and CDC growth charts?", "WHO growth charts (used for ages 0-2) are based on breastfed babies as the standard and represent how children should grow. CDC growth charts (used for ages 2-20) are based on how children in the U.S. actually grew during specific time periods."),
        ("What percentile range is considered normal for babies?", "Percentiles between the 5th and 95th are generally considered within the normal range. What matters most is that your baby follows a consistent growth curve over time, rather than a single percentile reading."),
        ("How often should baby growth be measured?", "During the first year, baby growth is typically measured at each well-child visit: at birth, 1, 2, 4, 6, 9, and 12 months. After age 1, measurements are usually taken at annual check-ups."),
        ("What does head circumference percentile indicate?", "Head circumference percentile helps track brain growth and development. A head circumference that is consistently very large or very small, or that suddenly crosses multiple percentile lines, may prompt your pediatrician to evaluate further.")
    ],
    "barcode-label-maker": [
        ("What barcode types can be generated for labels?", "Common barcode types include UPC-A and UPC-E for retail products, EAN-13 for international retail, Code 128 for shipping and logistics, Code 39 for inventory, QR codes for URLs and data, and Data Matrix for small items."),
        ("What resolution is needed for printable barcode labels?", "For reliable scanning, barcode labels should be printed at a minimum of 300 DPI. Higher resolutions of 600 DPI or more are recommended for very small barcodes or barcodes with fine detail like QR codes."),
        ("What is the minimum size for a scannable barcode?", "The minimum size depends on the barcode type. UPC-A barcodes should be at least 1.175 inches wide and 1.02 inches tall at 100% magnification. QR codes should be at least 1 x 1 cm for reliable scanning with standard readers."),
        ("Can barcode labels be printed on a regular printer?", "Yes, barcode labels can be printed on regular inkjet or laser printers using label sheets. For high-volume or durable labels, thermal printers with specialized label stock are recommended."),
        ("What is the quiet zone on a barcode label?", "The quiet zone is the blank margin surrounding a barcode that allows scanners to detect where the barcode begins and ends. It should be at least 10 times the width of the narrowest bar, or a minimum of 2.5mm on each side.")
    ],
    "bcrypt-generator": [
        ("What is bcrypt and why is it used for password hashing?", "Bcrypt is a password hashing algorithm based on the Blowfish cipher. It is used because it includes a built-in salt to prevent rainbow table attacks and has an adjustable cost factor that makes brute-force attacks computationally expensive."),
        ("What is a bcrypt salt round or cost factor?", "The cost factor (also called salt rounds or work factor) determines how many iterations bcrypt performs. Each increment doubles the computation time. A cost factor of 10 means 2^10 (1,024) iterations. Higher values are more secure but slower."),
        ("What cost factor should I use for bcrypt?", "A cost factor of 10-12 is commonly recommended for most applications as of 2024. The goal is to make hashing take about 100-300 milliseconds. You should benchmark on your hardware and increase the cost factor as computing power improves."),
        ("Can a bcrypt hash be reversed or decrypted?", "No, bcrypt is a one-way hashing function and cannot be reversed. To verify a password, you hash the input with the same salt and compare the result to the stored hash. This is why bcrypt is suitable for password storage."),
        ("What does a bcrypt hash string look like?", "A bcrypt hash is a 60-character string that includes the algorithm version, cost factor, salt, and hash. For example: $2b$10$N9qo8uLOickgx2ZMRZoMye. The prefix $2b$ indicates the bcrypt version, and 10 is the cost factor.")
    ],
    "binary-calculator": [
        ("How does binary arithmetic addition work?", "Binary addition follows the same rules as decimal addition but uses only digits 0 and 1. The key rules are: 0+0=0, 0+1=1, 1+0=1, and 1+1=10 (which means 0 with a carry of 1 to the next position)."),
        ("What is two's complement in binary?", "Two's complement is a method for representing negative numbers in binary. To find the two's complement, invert all bits (change 0s to 1s and vice versa) and add 1. For example, -5 in 8-bit two's complement is 11111011."),
        ("How do you multiply binary numbers?", "Binary multiplication works like decimal multiplication but is simpler because you only multiply by 0 or 1. Multiply the top number by each bit of the bottom number, shift each partial product left, and add all partial products together."),
        ("What is the difference between binary, octal, and hexadecimal?", "Binary is base-2 (digits 0-1), octal is base-8 (digits 0-7), and hexadecimal is base-16 (digits 0-9 and A-F). Each octal digit represents exactly 3 binary bits, and each hexadecimal digit represents exactly 4 binary bits."),
        ("How do you convert binary to decimal?", "To convert binary to decimal, multiply each bit by 2 raised to the power of its position (starting from 0 on the right), then sum the results. For example, binary 1101 = 1x8 + 1x4 + 0x2 + 1x1 = 13 in decimal.")
    ],
    "binary-search-visualizer": [
        ("What is binary search and how does it work?", "Binary search is an efficient algorithm that finds a target value in a sorted array by repeatedly dividing the search space in half. It compares the target to the middle element and eliminates the half where the target cannot exist."),
        ("What is the time complexity of binary search?", "Binary search has a time complexity of O(log n), where n is the number of elements. This means that for an array of 1 million elements, binary search needs at most about 20 comparisons, compared to up to 1 million for linear search."),
        ("Why must the array be sorted for binary search?", "Binary search relies on the ability to eliminate half of the remaining elements at each step by comparing the target to the middle element. This elimination only works correctly when elements are in sorted order."),
        ("What is the difference between iterative and recursive binary search?", "Iterative binary search uses a loop with low and high pointers, while recursive binary search calls itself with updated boundaries. Both have O(log n) time complexity, but iterative uses O(1) space while recursive uses O(log n) stack space."),
        ("When should you use binary search instead of linear search?", "Use binary search when the data is sorted and you need to perform multiple searches, as the O(log n) per search outweighs the O(n log n) sorting cost. For a single search on unsorted data, linear search with O(n) is more appropriate.")
    ],
    "binary-text-converter": [
        ("How is text represented in binary?", "Text is represented in binary using character encoding standards like ASCII or UTF-8. Each character is assigned a numeric code, which is then expressed in binary. For example, the letter A is ASCII code 65, which is 01000001 in binary."),
        ("What is the difference between ASCII and UTF-8 binary encoding?", "ASCII uses 7 bits to represent 128 characters (English letters, numbers, and basic symbols). UTF-8 is a variable-width encoding that uses 1 to 4 bytes and can represent over 1.1 million characters, including all world languages and emoji."),
        ("How many bits does each text character use?", "In ASCII, each character uses 7 bits (often stored as 8 bits with a leading zero). In UTF-8, standard English characters use 8 bits (1 byte), while accented characters use 16 bits and emoji typically use 32 bits (4 bytes)."),
        ("Can binary be converted back to readable text?", "Yes, binary can be converted back to text by grouping the binary digits into 8-bit bytes, converting each byte to its decimal value, and then mapping that value to the corresponding character using the appropriate encoding (ASCII or UTF-8)."),
        ("What is the binary representation of common characters?", "Some common binary values include: space is 00100000, the digit 0 is 00110000, uppercase A is 01000001, lowercase a is 01100001, and the newline character is 00001010.")
    ],
    "binary-to-decimal-converter": [
        ("How do you convert binary to decimal manually?", "To convert binary to decimal, assign each bit a power of 2 based on its position from right to left (starting at 2^0). Multiply each bit by its positional value and sum the results. For example, 1011 = 8+0+2+1 = 11."),
        ("What is the largest decimal number that 8 bits can represent?", "An 8-bit unsigned binary number can represent values from 0 to 255 (2^8 - 1 = 255). If using signed representation (two's complement), the range is -128 to 127."),
        ("Can binary fractions be converted to decimal?", "Yes, binary fractions work the same way but with negative powers of 2. For binary 0.101, calculate 1x2^-1 + 0x2^-2 + 1x2^-3 = 0.5 + 0 + 0.125 = 0.625 in decimal."),
        ("Why does the binary system use only 0 and 1?", "Binary uses only 0 and 1 because digital electronic circuits have two stable states: on (high voltage) and off (low voltage). This two-state system is the most reliable way to store and process data in computer hardware."),
        ("What is the binary equivalent of decimal 100?", "The decimal number 100 in binary is 1100100. You can verify this: 64 + 32 + 0 + 0 + 4 + 0 + 0 = 100.")
    ],
    "blood-pressure-calculator": [
        ("What do the two numbers in a blood pressure reading mean?", "The top number (systolic) measures the pressure in your arteries when your heart beats. The bottom number (diastolic) measures the pressure between beats when your heart is resting. Both are measured in millimeters of mercury (mmHg)."),
        ("What is considered normal blood pressure?", "Normal blood pressure is defined as a systolic reading below 120 mmHg and a diastolic reading below 80 mmHg. Elevated blood pressure is systolic 120-129 with diastolic below 80. Stage 1 hypertension starts at 130/80 mmHg."),
        ("How many readings should I take for an accurate average?", "Medical guidelines recommend taking at least 2-3 readings one minute apart and averaging them. For home monitoring, take readings at the same time each day for at least 7 days before calculating a meaningful average."),
        ("When is the best time to measure blood pressure?", "The best times to measure blood pressure are in the morning before eating or taking medications, and in the evening. Avoid measuring within 30 minutes of exercise, caffeine, or smoking, and sit quietly for 5 minutes before taking a reading."),
        ("What is the difference between home and clinical blood pressure readings?", "Home blood pressure readings tend to be lower than clinical readings due to white coat syndrome (anxiety at the doctor's office). Home readings above 135/85 mmHg are generally considered equivalent to clinical readings above 140/90 mmHg.")
    ],
    "bmi-calculator-metric": [
        ("How is BMI calculated using metric units?", "BMI is calculated by dividing weight in kilograms by height in meters squared. The formula is BMI = weight (kg) / height (m)^2. For example, a person weighing 70 kg who is 1.75 m tall has a BMI of 70 / (1.75 x 1.75) = 22.9."),
        ("What are the BMI categories for adults?", "The standard BMI categories are: underweight (below 18.5), normal weight (18.5 to 24.9), overweight (25.0 to 29.9), and obese (30.0 and above). Obesity is further divided into Class I (30-34.9), Class II (35-39.9), and Class III (40+)."),
        ("Is BMI an accurate measure of body fat?", "BMI is a useful screening tool but has limitations. It does not distinguish between muscle and fat mass, so muscular athletes may have high BMI despite low body fat. It also does not account for age, sex, bone density, or fat distribution."),
        ("Does BMI differ for different ethnic groups?", "Yes, BMI health risk thresholds differ by ethnicity. The WHO suggests that Asian populations may have increased health risks at lower BMI values (above 23) compared to European populations, due to differences in body fat distribution."),
        ("Should children use the same BMI scale as adults?", "No, children and adolescents use BMI-for-age percentiles rather than fixed categories. A child's BMI is compared to other children of the same age and sex, with the 85th to 95th percentile considered overweight and above the 95th considered obese.")
    ],
    "bmi-prime-calculator": [
        ("What is BMI Prime and how does it differ from regular BMI?", "BMI Prime is the ratio of your actual BMI to the upper limit of normal BMI (25). It is calculated as BMI / 25. A BMI Prime of 1.0 means you are at the upper boundary of normal weight. Values below 1.0 indicate normal weight, above 1.0 indicate overweight."),
        ("How do you calculate BMI Prime?", "BMI Prime is calculated by dividing your BMI by 25 (the upper limit of the normal BMI range). For example, if your BMI is 22.5, your BMI Prime is 22.5 / 25 = 0.90, meaning you are 10% below the upper normal limit."),
        ("What is a healthy BMI Prime value?", "A healthy BMI Prime value falls between 0.74 and 1.00, which corresponds to a BMI of 18.5 to 25.0. A BMI Prime below 0.74 suggests underweight, while above 1.00 indicates overweight."),
        ("Why is BMI Prime useful compared to standard BMI?", "BMI Prime is useful because it provides a single, dimensionless number that immediately shows how far you are from the normal weight threshold. A value of 1.20 tells you instantly that you are 20% above the upper normal limit."),
        ("Can BMI Prime be used across different populations?", "BMI Prime can be adapted for different populations by changing the reference BMI value. For example, using a cutoff of 23 instead of 25 for Asian populations would better reflect their different risk thresholds.")
    ],
    "bmr-calculator": [
        ("What is Basal Metabolic Rate (BMR)?", "Basal Metabolic Rate is the number of calories your body needs to maintain basic life-sustaining functions at rest, such as breathing, circulation, and cell production. BMR typically accounts for 60-75% of your total daily energy expenditure."),
        ("What is the difference between the Mifflin-St Jeor and Harris-Benedict equations?", "The Mifflin-St Jeor equation (1990) is generally considered more accurate for modern populations. The Harris-Benedict equation (1919) tends to overestimate BMR by about 5%. Most nutritionists now prefer the Mifflin-St Jeor formula."),
        ("How do I calculate Total Daily Energy Expenditure from BMR?", "TDEE is calculated by multiplying your BMR by an activity factor: sedentary (x1.2), lightly active (x1.375), moderately active (x1.55), very active (x1.725), or extremely active (x1.9). This gives your total daily calorie needs."),
        ("What factors affect BMR?", "Key factors affecting BMR include age (decreases about 1-2% per decade after 20), sex (men typically have higher BMR due to more muscle mass), body composition (more muscle means higher BMR), and genetics."),
        ("Does BMR change with diet and exercise?", "Yes, extreme calorie restriction can lower BMR by 15-30% through metabolic adaptation. Regular strength training can increase BMR by building muscle mass. Each pound of muscle burns approximately 6-7 calories per day at rest.")
    ],
    "body-mass-index-calculator": [
        ("What is the Body Mass Index formula?", "BMI is calculated as weight divided by height squared. In metric units: BMI = kg / m^2. In imperial units: BMI = (lbs / in^2) x 703. For example, a 150-pound person who is 5'8\" tall has a BMI of 22.8."),
        ("What BMI is considered healthy for adults?", "A BMI between 18.5 and 24.9 is considered a healthy weight for adults. Below 18.5 is classified as underweight, 25-29.9 is overweight, and 30 or above is classified as obese according to the World Health Organization."),
        ("What are the health risks associated with high BMI?", "A BMI above 25 is associated with increased risk of type 2 diabetes, cardiovascular disease, high blood pressure, certain cancers, sleep apnea, and osteoarthritis. Risk increases progressively with higher BMI values."),
        ("Can someone with a normal BMI still be unhealthy?", "Yes, BMI does not measure body fat percentage or distribution. A person with normal BMI can still have excess visceral fat (around organs), which carries health risks. This is sometimes called metabolically obese normal weight."),
        ("How has BMI classification changed over time?", "In 1998, the U.S. National Institutes of Health lowered the overweight threshold from 27.8 (men) and 27.3 (women) to 25 for both sexes, aligning with WHO standards. This change reclassified millions of Americans as overweight overnight.")
    ],
    "business-name-generator": [
        ("How do I choose a good business name?", "A good business name should be memorable, easy to spell and pronounce, relevant to your industry, and available as a domain name. It should also be distinct from competitors and not infringe on existing trademarks."),
        ("Should I include my industry in the business name?", "Including your industry can help with clarity and SEO (like 'Smith Plumbing'), but it can limit future expansion. Many successful brands use abstract or invented names (like Google or Spotify) that work across multiple product lines."),
        ("How do I check if a business name is already taken?", "Check the USPTO trademark database (TESS), your state's business name registry, domain name availability, and social media handles. Also search Google to see if any established businesses already use the name."),
        ("What makes a business name legally protectable?", "Business names that are fanciful (invented words), arbitrary (real words used unexpectedly), or suggestive (hinting at qualities without describing them) receive the strongest trademark protection. Descriptive names are harder to protect."),
        ("How long should a business name be?", "Ideally, a business name should be 1-3 words and no more than 15 characters. Shorter names are easier to remember, type, and fit on signage and logos. Most of the world's most recognized brand names are under 10 characters.")
    ],
    "car-depreciation-calculator": [
        ("How much does a new car depreciate in the first year?", "A new car typically loses 20-30% of its value in the first year alone. By the end of the third year, most cars have lost about 40-50% of their original value. This rapid early depreciation is the largest cost of car ownership."),
        ("What is the difference between straight-line and declining balance depreciation?", "Straight-line depreciation spreads the loss evenly across each year of ownership. Declining balance depreciation applies a fixed percentage to the remaining value each year, resulting in larger losses early and smaller losses later, which better reflects actual car value trends."),
        ("What factors affect car depreciation rate?", "Key factors include the make and model (luxury brands depreciate faster), mileage (average is 12,000-15,000 miles/year), condition, maintenance history, fuel efficiency, reliability ratings, and market demand for that vehicle type."),
        ("Which cars hold their value best?", "Trucks, SUVs, and vehicles from brands like Toyota, Lexus, Porsche, and Subaru tend to hold value best. Electric vehicles have historically depreciated faster, though this is changing as demand increases."),
        ("How does mileage affect car value?", "Vehicles lose roughly 20-25 cents per mile in value above the average annual mileage. Cars with significantly below-average mileage retain more value, while high-mileage vehicles can depreciate 10-20% faster than average.")
    ],
    "carpet-calculator": [
        ("How do I calculate how much carpet I need?", "Measure each room's length and width in feet, multiply to get square footage, then add 10% for waste from cuts and seams. Convert to square yards by dividing by 9, as carpet is typically sold by the square yard."),
        ("How much extra carpet should I order for waste?", "Plan for 10-15% extra carpet for standard rectangular rooms. For irregularly shaped rooms, stairs, or patterned carpet that requires matching, add 15-20% to account for additional cutting waste."),
        ("How much does carpet installation typically cost?", "Carpet installation in the U.S. typically costs $3-$6 per square foot for labor, plus $0.50-$1.00 per square foot for padding. The carpet itself ranges from $2-$15+ per square foot depending on material and quality."),
        ("What is the standard carpet roll width?", "Standard carpet rolls are 12 feet wide in the U.S. Some styles are also available in 15-foot widths. Planning your installation around these widths can minimize seams and reduce waste."),
        ("How do I calculate carpet for stairs?", "For each stair, measure the depth of the tread plus the height of the riser, then add 1 inch for the nose. Multiply by the stair width. A standard staircase of 13 steps with 36-inch wide stairs needs approximately 50-60 square feet of carpet.")
    ],
    "code-beautifier": [
        ("What is code beautification and why is it important?", "Code beautification (or formatting) is the process of restructuring code to follow consistent indentation, spacing, and line-breaking conventions. It improves readability, makes code reviews easier, and helps teams maintain a consistent coding style."),
        ("What is the difference between code beautification and minification?", "Beautification adds whitespace, indentation, and line breaks to make code human-readable. Minification does the opposite: it removes all unnecessary whitespace and shortens variable names to reduce file size for faster loading in production."),
        ("Which programming languages can be beautified?", "Most programming languages have beautification tools. Common ones include JavaScript (Prettier, ESLint), Python (Black, autopep8), HTML/CSS (Prettier), JSON (built-in formatters), SQL (sql-formatter), and Java (google-java-format)."),
        ("Should I use tabs or spaces for indentation?", "This is a long-standing debate. Spaces (typically 2 or 4) are more common in most modern style guides and ensure consistent display across editors. Tabs allow each developer to set their preferred visual width. Most teams pick one and enforce it with a formatter."),
        ("Does beautifying code change its functionality?", "No, code beautification only changes whitespace and formatting without altering the logic or behavior. However, in whitespace-sensitive languages like Python, incorrect beautification could potentially change program behavior, so use language-aware formatters.")
    ],
    "color-blindness-simulator": [
        ("What are the main types of color blindness?", "The three main types are protanopia (red-blind, affecting about 1% of males), deuteranopia (green-blind, affecting about 1% of males), and tritanopia (blue-blind, affecting less than 0.01% of the population). Anomalous trichromacy variants (partial deficiency) are more common."),
        ("How common is color blindness?", "Color blindness affects approximately 8% of men and 0.5% of women of Northern European descent. Red-green color blindness is the most common form, with deuteranomaly (reduced green sensitivity) being the single most prevalent type."),
        ("How can I design websites that are accessible to color-blind users?", "Use sufficient contrast ratios (at least 4.5:1 for text), do not rely solely on color to convey information, add patterns or labels to charts and graphs, and test your designs with a color blindness simulator. Avoid problematic color pairs like red/green."),
        ("Is color blindness hereditary?", "Most color blindness is inherited through the X chromosome, which is why it is far more common in men. A mother who is a carrier has a 50% chance of passing it to her sons. Acquired color vision deficiency can also result from eye disease or medication."),
        ("Can color blindness be corrected?", "There is currently no cure for inherited color blindness. Special glasses with color-filtering lenses (like EnChroma) can enhance color perception for some people with red-green deficiency but do not restore normal color vision.")
    ],
    "creatinine-clearance-calculator": [
        ("What is creatinine clearance and why is it important?", "Creatinine clearance (CrCl) estimates how well your kidneys filter waste from the blood by measuring the clearance of creatinine, a waste product from muscle metabolism. It is essential for assessing kidney function and adjusting medication doses."),
        ("What is the Cockcroft-Gault equation?", "The Cockcroft-Gault equation estimates creatinine clearance using the formula: CrCl = [(140 - age) x weight in kg x (0.85 if female)] / (72 x serum creatinine in mg/dL). It was developed in 1976 and remains widely used for drug dosing."),
        ("What are the stages of chronic kidney disease (CKD)?", "CKD is classified into 5 stages based on GFR: Stage 1 (GFR 90+, normal), Stage 2 (GFR 60-89, mild decrease), Stage 3a (GFR 45-59), Stage 3b (GFR 30-44), Stage 4 (GFR 15-29, severe), and Stage 5 (GFR below 15, kidney failure)."),
        ("Why is creatinine clearance used for drug dosing?", "Many medications are eliminated by the kidneys. When kidney function is reduced, drugs can accumulate to toxic levels. Creatinine clearance helps physicians determine safe medication doses, particularly for drugs like antibiotics, anticoagulants, and chemotherapy agents."),
        ("What is the difference between creatinine clearance and GFR?", "Creatinine clearance (CrCl) is an estimate of kidney filtration based on blood creatinine levels and patient characteristics. GFR (glomerular filtration rate) is the actual rate of blood filtered by the kidneys. CrCl slightly overestimates GFR because creatinine is also secreted by kidney tubules.")
    ],
    "debt-payoff-calculator": [
        ("What is the debt avalanche method?", "The debt avalanche method prioritizes paying off debts with the highest interest rates first while making minimum payments on all other debts. This approach minimizes the total interest paid over time and is mathematically the most cost-effective strategy."),
        ("What is the debt snowball method?", "The debt snowball method prioritizes paying off the smallest balance first regardless of interest rate. Once the smallest debt is paid off, you roll that payment into the next smallest. This method provides psychological wins that help maintain motivation."),
        ("How do I calculate my debt payoff timeline?", "Your payoff timeline depends on your total balance, interest rates, and monthly payment amount. Use the formula: months = -log(1 - (balance x rate / payment)) / log(1 + rate), where rate is the monthly interest rate."),
        ("Should I pay off debt or invest?", "Generally, pay off high-interest debt (above 6-7%) before investing, as the guaranteed return from eliminating interest usually exceeds expected investment returns. For low-interest debt, investing may yield better results over time."),
        ("How much faster can extra payments eliminate debt?", "Even small extra payments can dramatically reduce your payoff time. For example, adding $100 per month to a $10,000 balance at 18% APR can reduce the payoff time from over 30 years (with minimums) to under 3 years.")
    ],
    "due-date-calculator": [
        ("How is a pregnancy due date calculated?", "The due date is typically calculated by adding 280 days (40 weeks) to the first day of your last menstrual period (LMP). This is known as Naegele's rule. The actual delivery date can vary by plus or minus two weeks."),
        ("What is gestational age vs fetal age?", "Gestational age is measured from the first day of the last menstrual period and includes about 2 weeks before conception actually occurred. Fetal age (conceptional age) is measured from the actual date of conception and is about 2 weeks less than gestational age."),
        ("How accurate is an ultrasound due date vs LMP?", "First-trimester ultrasounds (before 13 weeks) are accurate to within 5-7 days. LMP-based dates can be less accurate if cycles are irregular. If ultrasound and LMP dates differ by more than 7 days, the ultrasound date is generally preferred."),
        ("What percentage of babies are born on their due date?", "Only about 4-5% of babies are born on their exact due date. Most births occur within two weeks before or after the due date. About 80% of babies arrive between 38 and 42 weeks of gestation."),
        ("What are the trimesters of pregnancy?", "The first trimester spans weeks 1-12 (organ development), the second trimester spans weeks 13-26 (rapid growth and movement), and the third trimester spans weeks 27-40 (weight gain and lung maturation). Each trimester lasts approximately 13 weeks.")
    ],
    "electricity-cost-calculator": [
        ("How do I calculate the electricity cost of an appliance?", "Multiply the appliance wattage by hours of daily use, then divide by 1000 to get daily kilowatt-hours (kWh). Multiply by your electricity rate (cents per kWh) to get the daily cost. For monthly cost, multiply by 30."),
        ("What is a kilowatt-hour (kWh)?", "A kilowatt-hour is a unit of energy equal to using 1,000 watts for one hour. For example, a 100-watt light bulb running for 10 hours uses 1 kWh. Your electric bill charges you per kWh consumed."),
        ("What are the most expensive appliances to run?", "Central air conditioning (3,000-5,000 watts), electric water heaters (4,000-5,500 watts), space heaters (1,500 watts), electric dryers (4,000-5,000 watts), and electric ovens (2,000-5,000 watts) are typically the most expensive household appliances to operate."),
        ("What is the average electricity rate in the US?", "The average U.S. residential electricity rate is approximately 16-17 cents per kWh as of 2024. Rates vary significantly by state, from around 10 cents per kWh in states like Louisiana to over 30 cents in Hawaii and parts of New England."),
        ("How can I reduce my electricity costs?", "Switch to LED bulbs (use 75% less energy), use a programmable thermostat, run appliances during off-peak hours, seal air leaks, upgrade to Energy Star appliances, and unplug devices when not in use. Heating and cooling account for about 50% of home energy use.")
    ],
    "estate-tax-calculator": [
        ("What is the federal estate tax exemption?", "The federal estate tax exemption for 2024 is $13.61 million per individual ($27.22 million per married couple). Estates valued below this threshold owe no federal estate tax. This exemption is scheduled to be reduced by approximately half after 2025 unless Congress acts."),
        ("How are estate taxes calculated?", "Estate taxes are calculated on the taxable estate (total assets minus debts, expenses, and deductions) that exceeds the exemption amount. Federal estate tax rates range from 18% to 40%, with the top rate applying to amounts over $1 million above the exemption."),
        ("What is the difference between estate tax and inheritance tax?", "Estate tax is paid by the estate before assets are distributed to heirs. Inheritance tax is paid by the person receiving the assets. The federal government only imposes an estate tax, while some states impose an inheritance tax, estate tax, or both."),
        ("What assets are included in a taxable estate?", "A taxable estate includes real estate, bank accounts, investments, retirement accounts, life insurance proceeds (if you owned the policy), business interests, personal property, and any assets transferred within 3 years of death."),
        ("How can estate taxes be minimized?", "Common strategies include gifting assets during your lifetime (up to $18,000 per recipient annually without tax), setting up irrevocable trusts, making charitable donations, purchasing life insurance in an irrevocable life insurance trust, and using the marital deduction for spouse transfers.")
    ],
    "ev-charging-calculator": [
        ("How long does it take to charge an electric vehicle?", "Charging time depends on the charger level. Level 1 (120V outlet) adds 3-5 miles of range per hour. Level 2 (240V) adds 25-30 miles per hour, fully charging in 6-10 hours. DC fast charging can add 200+ miles in 30-60 minutes."),
        ("How much does it cost to charge an EV at home?", "The average cost to fully charge an EV at home is $10-$15 for a typical 60 kWh battery at the U.S. average electricity rate. This is equivalent to about $0.03-$0.05 per mile, compared to $0.10-$0.15 per mile for gasoline vehicles."),
        ("What is the difference between Level 1, Level 2, and DC fast charging?", "Level 1 uses a standard 120V household outlet (1.4 kW). Level 2 uses a 240V circuit (7-19 kW) and is the most common home and public charger. DC fast charging (50-350 kW) bypasses the onboard charger for rapid charging at public stations."),
        ("How much money do you save by driving an EV vs gasoline?", "The average EV owner saves $800-$1,500 per year on fuel costs compared to a gasoline car. The exact savings depend on local electricity rates, gas prices, driving distance, and the efficiency of both vehicles."),
        ("Does cold weather affect EV charging?", "Yes, cold weather can reduce charging speed by 20-40% and decrease driving range by 20-40%. Batteries charge more slowly in cold conditions because the chemical reactions inside slow down. Many EVs have battery preconditioning to mitigate this.")
    ],
    "fancy-text-generator": [
        ("How do fancy text generators create different fonts?", "Fancy text generators use Unicode characters that look like styled versions of standard letters. For example, mathematical symbols, enclosed alphanumerics, and special Unicode blocks contain characters that resemble bold, italic, script, and other font styles."),
        ("Can fancy text be used on social media?", "Yes, fancy text generated from Unicode characters works on most social media platforms including Instagram, Twitter/X, Facebook, TikTok, and YouTube. The text is actual Unicode characters, not images, so it can be copied and pasted anywhere."),
        ("What is the difference between fancy text and custom fonts?", "Fancy text uses special Unicode characters that are universally supported across devices and platforms. Custom fonts require CSS or font files and only work on websites where they are installed. Fancy text works anywhere that supports Unicode."),
        ("Are there accessibility concerns with fancy text?", "Yes, screen readers may not correctly read fancy Unicode text, making it inaccessible to visually impaired users. Search engines also cannot properly index fancy text. Use it sparingly and avoid it for important information."),
        ("What Unicode blocks are used for fancy text?", "Common Unicode blocks include Mathematical Alphanumeric Symbols (bold, italic, script), Enclosed Alphanumerics (circled letters), Fullwidth Forms (wide characters), Regional Indicator Symbols, and various other blocks containing decorative letter variants.")
    ],
    "favicon-generator": [
        ("What file format should favicons use?", "Modern favicons should use ICO format (containing multiple sizes) for maximum browser compatibility. Additionally, include PNG versions for modern browsers and Apple Touch Icon (180x180 PNG) for iOS devices. SVG favicons are supported by newer browsers."),
        ("What sizes should a favicon be?", "Include at minimum 16x16 and 32x32 pixels for browser tabs. For comprehensive support, also include 48x48 (Windows), 180x180 (Apple Touch Icon), 192x192 and 512x512 (Android/PWA). An ICO file can contain multiple sizes in one file."),
        ("How do I add a favicon to my website?", "Add a link tag in your HTML head section: <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\">. For Apple devices, add <link rel=\"apple-touch-icon\" href=\"/apple-touch-icon.png\">. Place favicon.ico in your site root for automatic detection."),
        ("Why is my favicon not showing up?", "Common reasons include incorrect file path, browser cache (try clearing it or hard refresh), wrong file format, missing link tag in HTML, or the server not serving the correct MIME type. ICO files should be served as image/x-icon."),
        ("Can I use an SVG as a favicon?", "Yes, SVG favicons are supported by Chrome, Firefox, Edge, and Opera but not Safari or IE. Use the tag <link rel=\"icon\" type=\"image/svg+xml\" href=\"/favicon.svg\">. SVG favicons can adapt to dark mode using CSS media queries within the SVG.")
    ],
    "grade-calculator": [
        ("How do I calculate my weighted grade?", "Multiply each assignment grade by its weight (as a decimal), then sum the results. For example, if homework (30%) = 90 and exams (70%) = 80, your weighted grade is (90 x 0.30) + (80 x 0.70) = 27 + 56 = 83."),
        ("What grade do I need on my final exam to pass?", "Use the formula: Required = (Target - Current x (1 - Final Weight)) / Final Weight. For example, if you have an 75% with a final worth 30% and need 80%: Required = (80 - 75 x 0.70) / 0.30 = (80 - 52.5) / 0.30 = 91.7%."),
        ("What is a GPA and how is it calculated?", "GPA (Grade Point Average) converts letter grades to a 4.0 scale: A=4.0, B=3.0, C=2.0, D=1.0, F=0. Multiply each course's grade points by credit hours, sum them, and divide by total credit hours."),
        ("What is the difference between weighted and unweighted GPA?", "Unweighted GPA uses the standard 4.0 scale for all classes. Weighted GPA adds extra points for honors, AP, or IB courses (typically up to 5.0). Colleges often consider both to evaluate the difficulty of your course load."),
        ("How do I convert a percentage to a letter grade?", "The most common scale is A (90-100%), B (80-89%), C (70-79%), D (60-69%), and F (below 60%). Some schools use plus/minus grades with narrower ranges, such as A (93-100%), A- (90-92%), B+ (87-89%), and so on.")
    ],
    "gravel-calculator": [
        ("How much gravel do I need for my project?", "Calculate the volume by multiplying length x width x depth (all in feet), then divide by 27 to convert cubic feet to cubic yards. For tons, multiply cubic yards by the gravel density factor (typically 1.4 tons per cubic yard for most gravel types)."),
        ("How many tons of gravel are in a cubic yard?", "Most gravel weighs approximately 1.4 tons (2,800 pounds) per cubic yard, though this varies by type. Pea gravel weighs about 1.4 tons/yd3, crushed stone about 1.35 tons/yd3, and river rock about 1.5 tons/yd3."),
        ("How deep should a gravel driveway be?", "A gravel driveway should be 8-12 inches deep total, typically built in three layers: a 4-6 inch base layer of large crushed stone, a 3-4 inch middle layer of medium stone, and a 2-3 inch top layer of fine gravel or crushed stone."),
        ("What type of gravel is best for a driveway?", "Crushed angular gravel (like #57 stone or crushed limestone) is best for driveways because the irregular shapes lock together and resist shifting. Avoid rounded gravel like pea gravel for driveways as it moves underfoot and under tires."),
        ("How do I calculate gravel for a circular area?", "For a circular area, calculate the area using the formula pi x radius^2, then multiply by the desired depth. Convert to cubic yards by dividing by 27. For a 10-foot diameter circle at 3 inches deep, you need about 0.87 cubic yards.")
    ],
    "html-formatter": [
        ("What is HTML formatting and why does it matter?", "HTML formatting involves adding proper indentation, line breaks, and spacing to HTML code to make it readable and maintainable. Well-formatted HTML is easier to debug, review, and collaborate on, especially in team environments."),
        ("What is the difference between HTML beautification and minification?", "Beautification adds whitespace, indentation, and line breaks to make HTML human-readable. Minification removes all unnecessary characters to reduce file size. Beautified HTML is for development, while minified HTML is for production deployment."),
        ("What indentation style should I use for HTML?", "The most common HTML indentation styles are 2 spaces, 4 spaces, or tabs. Most modern style guides and teams prefer 2 spaces for HTML because it keeps deeply nested elements manageable. The key is consistency across your project."),
        ("How do self-closing tags work in HTML5?", "In HTML5, void elements like <br>, <img>, <input>, and <hr> do not require a closing slash. Writing <br> and <br/> are both valid. XHTML required the closing slash, but HTML5 treats it as optional."),
        ("Can HTML formatting affect page performance?", "Whitespace in HTML adds to file size but has minimal impact on modern pages due to gzip compression during transfer. For production, HTML minification can reduce file size by 10-30%, which can improve load times on high-traffic sites.")
    ],
    "ideal-weight-calculator": [
        ("What formulas are used to calculate ideal body weight?", "Four major formulas are used: Devine (1974), Robinson (1983), Miller (1983), and Hamwi (1964). Each uses different calculations based on height and sex. Results vary between formulas, so comparing multiple formulas gives a more realistic range."),
        ("What is the Devine formula for ideal weight?", "The Devine formula calculates ideal body weight as: Men = 50 kg + 2.3 kg per inch over 5 feet. Women = 45.5 kg + 2.3 kg per inch over 5 feet. This is the most widely used formula in clinical medicine for drug dosing."),
        ("Is ideal body weight the same as healthy weight?", "Not exactly. Ideal body weight formulas provide a single target number based primarily on height and sex. A healthy weight range, typically defined by a BMI of 18.5-24.9, is broader and may be more realistic for most people."),
        ("Why do ideal weight calculators give different results?", "Different formulas were developed using different study populations and methods. The Devine formula was originally created for drug dosing, while others aimed to predict optimal health weight. No single formula works perfectly for all body types."),
        ("Should ideal weight be adjusted for frame size?", "Yes, body frame size matters. Large-framed individuals may be healthy at weights 10% above the ideal, while small-framed people may be healthiest at 10% below. Frame size can be estimated by measuring wrist circumference relative to height.")
    ],
    "image-converter": [
        ("What is the difference between JPG and PNG?", "JPG uses lossy compression, producing smaller files but losing some quality each time it is saved. PNG uses lossless compression, preserving all image data with support for transparency. Use JPG for photos and PNG for graphics, logos, and images needing transparency."),
        ("What is WebP and why should I use it?", "WebP is a modern image format developed by Google that provides both lossy and lossless compression. WebP images are typically 25-35% smaller than equivalent JPG files and support transparency like PNG. It is supported by all modern browsers."),
        ("Does converting images reduce quality?", "Converting from a lossless format (PNG, BMP, TIFF) to another lossless format preserves quality. Converting to a lossy format (JPG, WebP lossy) reduces quality based on the compression level. Re-saving a JPG multiple times further degrades quality."),
        ("What image format is best for websites?", "WebP is the best choice for most web images due to its small file size and broad browser support. Use SVG for icons and logos, PNG for images requiring transparency, and JPG as a fallback for older browser support."),
        ("Is it safe to convert images in a browser?", "Yes, browser-based image converters that process files locally using JavaScript and the Canvas API are safe because your images never leave your device. No data is uploaded to a server.")
    ],
    "image-metadata-viewer": [
        ("What is image metadata (EXIF data)?", "EXIF (Exchangeable Image File Format) data is information embedded in image files by cameras and phones. It includes camera settings (aperture, shutter speed, ISO), date and time taken, GPS coordinates, camera model, and lens information."),
        ("What privacy concerns exist with image metadata?", "Image metadata can contain GPS coordinates revealing where a photo was taken, device information, and timestamps. Sharing photos online with metadata intact can inadvertently expose your home location, workplace, or travel patterns."),
        ("How do I remove metadata from photos?", "Most operating systems can strip metadata: on Windows, right-click the file, go to Properties > Details > Remove Properties. On Mac, use Preview > Tools > Show Inspector. Many social media platforms automatically strip EXIF data on upload."),
        ("What metadata do smartphone cameras record?", "Smartphone cameras typically record GPS coordinates, date and time, device model and manufacturer, camera settings, image dimensions, orientation, software version, and sometimes the direction the camera was facing (compass bearing)."),
        ("Can metadata be recovered after it is removed?", "No, once metadata is properly stripped from an image file, it cannot be recovered. The metadata is stored as additional data within the file, and removing it is permanent. Always keep original copies if you need to preserve metadata.")
    ],
    "image-to-base64": [
        ("What is Base64 image encoding?", "Base64 encoding converts binary image data into a text string using 64 ASCII characters (A-Z, a-z, 0-9, +, /). This allows images to be embedded directly in HTML, CSS, or JSON without separate file requests."),
        ("When should I use Base64 images instead of regular image files?", "Use Base64 for small images (under 10 KB) like icons, small logos, or UI elements where eliminating an HTTP request improves performance. For larger images, regular files are better because Base64 increases size by about 33%."),
        ("How much larger is a Base64 encoded image compared to the original?", "Base64 encoding increases file size by approximately 33% (a 3:4 ratio) because every 3 bytes of binary data are encoded as 4 ASCII characters. Gzip compression can partially offset this increase when transmitted over HTTP."),
        ("Can Base64 images be used in CSS?", "Yes, Base64 images can be embedded in CSS using the data URI syntax: background-image: url(data:image/png;base64,iVBORw0KGgo...). This eliminates an HTTP request but increases CSS file size, so it is best for small images only."),
        ("How do I embed a Base64 image in HTML?", "Use the data URI scheme in an img tag: <img src=\"data:image/png;base64,iVBORw0KGgo...\">. Replace image/png with the correct MIME type (image/jpeg, image/gif, image/webp) and follow base64, with the encoded string.")
    ],
    "image-to-text-ocr": [
        ("What is OCR and how does it work?", "OCR (Optical Character Recognition) is technology that converts images of text (scanned documents, photos, screenshots) into machine-readable text. It works by analyzing character shapes and patterns to identify letters, numbers, and symbols."),
        ("What image formats work best for OCR?", "High-resolution images (300 DPI or higher) in PNG or TIFF format produce the best OCR results. The text should have good contrast against the background, be properly oriented, and not be skewed or distorted."),
        ("How accurate is modern OCR technology?", "Modern OCR engines achieve 95-99% accuracy on clean, well-formatted printed text. Accuracy decreases with handwritten text, low resolution images, unusual fonts, poor lighting, and complex layouts with mixed content."),
        ("Can OCR recognize handwritten text?", "Yes, advanced OCR systems can recognize handwritten text, though accuracy is lower than for printed text (typically 70-90%). Neat, consistent handwriting produces better results. Cursive and heavily stylized handwriting remain challenging."),
        ("Is browser-based OCR private and secure?", "Browser-based OCR tools that use JavaScript libraries like Tesseract.js process images entirely on your device without uploading data to any server. This means your documents remain private and are never shared with third parties.")
    ],
    "inches-to-square-feet-calculator": [
        ("How do you convert inches to square feet?", "To convert an area measured in square inches to square feet, divide by 144 (since 1 square foot = 12 x 12 = 144 square inches). For example, 720 square inches equals 720 / 144 = 5 square feet."),
        ("How do I calculate square feet from length and width in inches?", "Multiply the length in inches by the width in inches to get the area in square inches, then divide by 144 to convert to square feet. For example, 36 inches x 48 inches = 1,728 square inches / 144 = 12 square feet."),
        ("Why are there 144 square inches in a square foot?", "There are 144 square inches in a square foot because 1 foot equals 12 inches, and area is calculated by multiplying two linear measurements. So 12 inches x 12 inches = 144 square inches per square foot."),
        ("When would I need to convert inches to square feet?", "This conversion is commonly needed when measuring rooms, flooring, fabric, countertops, or construction materials. Many measurements are taken in inches but materials are sold by the square foot."),
        ("How do I convert square feet back to square inches?", "Multiply the number of square feet by 144 to get square inches. For example, 10 square feet x 144 = 1,440 square inches. This is useful when you need precise measurements for cutting or fitting materials.")
    ],
}

def process_tool(tool_slug):
    """Add FAQPage JSON-LD to a tool's index.html."""
    filepath = f"{tool_slug}/index.html"
    if not os.path.exists(filepath):
        print(f"SKIP: {tool_slug} - file not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if FAQPage already exists
    if '"FAQPage"' in content:
        print(f"SKIP: {tool_slug} - FAQPage already exists")
        return False

    if tool_slug not in TOOL_FAQS:
        print(f"SKIP: {tool_slug} - no FAQ data defined")
        return False

    faqs = TOOL_FAQS[tool_slug]

    # Build the FAQPage JSON-LD
    faq_entities = []
    for q, a in faqs:
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }

    faq_json = json.dumps(faq_schema, indent=2)
    faq_block = f'\n<script type="application/ld+json">\n{faq_json}\n</script>'

    # Find insertion point - after the last existing JSON-LD block
    # Find all JSON-LD script blocks
    jsonld_pattern = r'<script type="application/ld\+json">.*?</script>'
    matches = list(re.finditer(jsonld_pattern, content, re.DOTALL))

    if matches:
        # Insert after the last JSON-LD block
        last_match = matches[-1]
        insert_pos = last_match.end()
        new_content = content[:insert_pos] + faq_block + content[insert_pos:]
    else:
        # Insert before </head>
        head_pos = content.find('</head>')
        if head_pos == -1:
            print(f"ERROR: {tool_slug} - no </head> found")
            return False
        new_content = content[:head_pos] + faq_block + '\n' + content[head_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"DONE: {tool_slug} - added FAQPage with {len(faqs)} questions")
    return True

def add_meta_tags(tool_slug, title, description, short_title, short_description):
    """Add canonical and OG meta tags to a tool."""
    filepath = f"{tool_slug}/index.html"
    if not os.path.exists(filepath):
        print(f"SKIP META: {tool_slug} - file not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if canonical already exists
    if 'rel="canonical"' in content:
        print(f"SKIP META: {tool_slug} - canonical already exists")
        return False

    meta_tags = f'''<link rel="canonical" href="https://zovo.one/free-tools/{tool_slug}/">
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://zovo.one/free-tools/{tool_slug}/"/>
<meta property="og:site_name" content="Zovo"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{short_title}"/>
<meta name="twitter:description" content="{short_description}"/>
'''

    # Find the JSON-LD block to insert before it
    jsonld_match = re.search(r'<script type="application/ld\+json">', content)
    if jsonld_match:
        insert_pos = jsonld_match.start()
        new_content = content[:insert_pos] + meta_tags + ' ' + content[insert_pos:]
    else:
        # Insert before </head>
        head_pos = content.find('</head>')
        if head_pos == -1:
            print(f"ERROR META: {tool_slug} - no </head> found")
            return False
        new_content = content[:head_pos] + meta_tags + content[head_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"DONE META: {tool_slug} - added canonical + OG tags")
    return True


if __name__ == "__main__":
    # First, add meta tags to the two tools that need them
    print("=== Adding Canonical + OG Meta Tags ===")
    add_meta_tags(
        "html-formatter",
        "Free HTML Formatter and Beautifier | Online Tool",
        "Format, beautify, and minify HTML with customizable indentation, attribute wrapping, syntax highlighting, and more. Free online tool.",
        "HTML Formatter and Beautifier",
        "Format, beautify, and minify HTML online. Free tool with customizable indentation and syntax highlighting."
    )
    add_meta_tags(
        "investment-return-calculator",
        "Investment Return Calculator | Free Online Tool",
        "Calculate investment returns, compound interest, and portfolio growth over time. Free online investment return calculator.",
        "Investment Return Calculator",
        "Calculate investment returns and compound interest. Free online calculator."
    )

    print("\n=== Adding FAQPage JSON-LD ===")
    tools = list(TOOL_FAQS.keys())
    done = 0
    for tool in tools:
        if process_tool(tool):
            done += 1

    print(f"\nTotal tools processed: {done}")
