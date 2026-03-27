#!/bin/bash

# Quality Enforcement Script - URL Standardization
# Perfection Agent Gamma - Fix tools.zovo.one violations

echo "=== PERFECTION AGENT GAMMA - URL STANDARDIZATION ==="
echo "Fixing tools.zovo.one → zovo.one/free-tools/"
echo ""

tools_with_violations=(
./reverse-mortgage-calculator/index.html
./puppy-years-to-human-years/index.html
./regex-visualizer/index.html
./sleep-cycle-calculator/index.html
./retirement-calculator/index.html
./number-generator/index.html
./qr-wifi-generator/index.html
./paycheck-estimator/index.html
./scientific-calculator-online/index.html
./pomodoro-timer/index.html
./svg-optimizer/index.html
./speech-to-text/index.html
./payroll-tax-calculator/index.html
./normal-distribution-table/index.html
./noise-reduction-calculator/index.html
./salary-calculator-massachusetts/index.html
./qr-code-maker/index.html
./salary-calculator-pennsylvania/index.html
./sitemap-generator/index.html
./paystub-generator/index.html
./qr-code-generator/index.html
./salary-to-hourly-calculator/index.html
./pdf-to-word-converter/index.html
./periodic-table/index.html
./projectile-motion-calculator/index.html
./square-footage-calculator/index.html
./qr-code-designer/index.html
./spring-constant-calculator/index.html
./significant-figures-calculator/index.html
./stock-profit-calculator/index.html
./nginx-config-generator/index.html
./readability-checker/index.html
./salary-calculator-georgia/index.html
./recycling-guide/index.html
./salary-calculator-maryland/index.html
./paint-coverage-calculator/index.html
./self-employment-tax-calculator/index.html
./pressure-converter/index.html
./quadratic-equation-grapher/index.html
./resume-generator/index.html
./scientific-notation-converter/index.html
./pregnancy-weight-tracker/index.html
./savings-goal-calculator/index.html
./radical-simplifier/index.html
./number-base-converter/index.html
./photo-to-sketch/index.html
./pay-stub-generator/index.html
./og-preview/index.html
./pixel-art-editor/index.html
./salary-calculator-california/index.html
./ohms-law-calculator/index.html
./pay-stub-creator/index.html
./pdf-splitter/index.html
./social-security-calculator/index.html
./pipe-flow-calculator/index.html
./svg-editor/index.html
./rental-yield-calculator/index.html
./salary-calculator-north-carolina/index.html
./sba-loan-calculator/index.html
./payroll-calculator/index.html
./protein-calculator/index.html
./qr-reader/index.html
./pdf-merger/index.html
./number-system-converter/index.html
./svg-path-editor/index.html
./screenshot-mockup/index.html
./ping-test/index.html
./salary-calculator/index.html
./physics-formula-calculator/index.html
./pdf-compressor/index.html
./sleep-calculator/index.html
./regex-tester/index.html
./paint-calculator/index.html
./sip-calculator/index.html
./shoe-size-converter/index.html
./noise-generator/index.html
./plagiarism-checker/index.html
./student-loan-calculator/index.html
./pendulum-calculator/index.html
./sales-tax-calculator/index.html
./percentage-calculator/index.html
./photo-filter/index.html
./sleep-quality-calculator/index.html
./percent-yield-calculator/index.html
./scientific-calculator/index.html
./salary-calculator-virginia/index.html
./placeholder-image/index.html
./online-calculator/index.html
./savings-calculator/index.html
./pixel-to-rem-converter/index.html
./salary-calculator-illinois/index.html
./stair-calculator/index.html
./receipt-generator/index.html
./rv-loan-calculator/index.html
./retirement-savings-calculator/index.html
./simple-interest-calculator/index.html
./screen-recorder/index.html
./overtime-calculator/index.html
./regex-generator/index.html
./overtime-tax-calculator/index.html
./rhyme-finder/index.html
./resume-builder/index.html
./rent-vs-buy-calculator/index.html
./paycheck-calculator/index.html
./period-calculator/index.html
./robots-txt-generator/index.html
./privacy-policy-generator/index.html
./roman-numeral-converter/index.html
./ssl-checker/index.html
./percentage-finder/index.html
./naira-to-usd-converter/index.html
./salary-calculator-ohio/index.html
./sorting-visualizer/index.html
./photo-editor/index.html
./recipe-scaler/index.html
./stopwatch/index.html
./soil-calculator/index.html
./scientific-notation-calculator/index.html
./readme-generator/index.html
./statistics-calculator/index.html
./paraphrase-tool/index.html
./paper-size-guide/index.html
./sitemap-validator/index.html
./online-translator/index.html
./roof-pitch-calculator/index.html
./pace-calculator/index.html
./present-value-calculator/index.html
./subnet-calculator/index.html
./paycheck-tax-calculator/index.html
./salary-calculator-colorado/index.html
./slug-generator/index.html
./running-pace-calculator/index.html
./salary-raise-calculator/index.html
./quadratic-solver/index.html
./svg-animator/index.html
./rc-circuit-calculator/index.html
./power-factor-calculator/index.html
./resistor-calculator/index.html
./percentage-change-calculator/index.html
./speed-distance-time-calculator/index.html
./random-picker/index.html
./speed-test/index.html
./pst-to-est/index.html
./screenshot-to-code/index.html
./salary-increase-calculator/index.html
./sql-playground/index.html
./percent-off-calculator/index.html
./salary-calculator-texas/index.html
./sek-to-usd-converter/index.html
./pay-stub-calculator/index.html
./speed-converter/index.html
./property-tax-calculator/index.html
./px-to-rem/index.html
./random-counter/index.html
./statistics-probability-calculator/index.html
./sudoku-solver/index.html
./ovulation-calculator/index.html
./salary-calculator-new-york/index.html
./quarterly-tax-calculator/index.html
./password-generator/index.html
./schema-generator/index.html
./resistor-color-code-calculator/index.html
./story-title-generator/index.html
./salary-calculator-michigan/index.html
./student-loan-repayment-calculator/index.html
./svg-to-png-converter/index.html
./random-number-generator/index.html
./ring-size-chart/index.html
./piano-keyboard/index.html
./poem-generator/index.html
)

fixed_count=0
error_count=0

for file in "${tools_with_violations[@]}"; do
    if [[ -f "$file" ]]; then
        echo "Processing: $file"

        # Fix tools.zovo.one URLs to zovo.one/free-tools/
        sed -i '' 's|https://tools\.zovo\.one/|https://zovo.one/free-tools/|g' "$file"

        if [[ $? -eq 0 ]]; then
            ((fixed_count++))
            echo "  ✓ Fixed URL violations"
        else
            ((error_count++))
            echo "  ✗ Error fixing $file"
        fi
    else
        echo "  ✗ File not found: $file"
        ((error_count++))
    fi
done

echo ""
echo "=== URL STANDARDIZATION COMPLETE ==="
echo "✓ Fixed: $fixed_count tools"
echo "✗ Errors: $error_count tools"
echo "Total processed: $((fixed_count + error_count))"