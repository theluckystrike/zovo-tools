/**
 * A1C Calculator Masterpiece Engine
 * Precision Medical Mathematics with Artisan-Level Craftsmanship
 *
 * Author: Master Craftsman Alpha
 * Version: 4.0 - Museum Quality Implementation
 * Date: March 2026
 *
 * Mathematical Foundation:
 * Based on the ADAG (A1C-Derived Average Glucose) Study
 * Published by Nathan et al., Diabetes Care 2008
 * DOI: 10.2337/dc08-0545
 */

'use strict';

// ============================================================================
// CONSTANTS: Medical Grade Precision Values
// ============================================================================

const MEDICAL_CONSTANTS = {
    // ADAG Study Formula Coefficients (Validated with 507 participants)
    ADAG: {
        SLOPE: 28.7,              // Linear relationship coefficient
        INTERCEPT: 46.7,          // Y-intercept correction factor
        MMOL_DIVISOR: 18.015,     // Glucose conversion factor mg/dL → mmol/L
        CORRELATION: 0.84,        // Original study correlation coefficient
        STANDARD_ERROR: 15.4      // Standard error in mg/dL
    },

    // Medical Risk Thresholds (ADA 2026 Standards)
    RISK_LEVELS: {
        NORMAL: { max: 5.7, label: 'Normal', class: 'risk-normal' },
        PREDIABETES: { min: 5.7, max: 6.4, label: 'Prediabetes', class: 'risk-prediabetes' },
        DIABETES_CONTROLLED: { min: 6.5, max: 6.9, label: 'Diabetes (Well Controlled)', class: 'risk-diabetes' },
        DIABETES_MODERATE: { min: 7.0, max: 7.9, label: 'Diabetes (Moderate)', class: 'risk-diabetes' },
        DIABETES_POOR: { min: 8.0, max: 8.9, label: 'Diabetes (Poor Control)', class: 'risk-diabetes' },
        DIABETES_DANGEROUS: { min: 9.0, label: 'Diabetes (Dangerous)', class: 'risk-diabetes' }
    },

    // Input Validation Bounds
    VALIDATION: {
        A1C_MIN: 3.0,             // Minimum physiologically possible A1C
        A1C_MAX: 20.0,            // Maximum safe calculation range
        GLUCOSE_MIN_MGDL: 40,     // Minimum glucose (severe hypoglycemia)
        GLUCOSE_MAX_MGDL: 600,    // Maximum glucose (severe hyperglycemia)
        GLUCOSE_MIN_MMOL: 2.2,    // Minimum glucose in mmol/L
        GLUCOSE_MAX_MMOL: 33.3,   // Maximum glucose in mmol/L
        PRECISION_DIGITS: 1       // Decimal places for A1C results
    },

    // Animation & UI Constants
    ANIMATION: {
        GAUGE_DURATION: 800,      // Gauge animation duration (ms)
        RESULT_FADE_DURATION: 300, // Result fade animation (ms)
        CALCULATION_DELAY: 150,   // Debounce delay for calculations (ms)
        GAUGE_EASING: 'cubic-bezier(0.4, 0, 0.2, 1)' // Material Design easing
    }
};

// ============================================================================
// CORE CALCULATOR ENGINE: Mathematical Precision
// ============================================================================

class A1CCalculatorEngine {
    constructor() {
        this.history = this.loadHistory();
        this.calculationCount = this.loadCalculationCount();
        this.currentUnit = 'mgdl';
        this.reverseUnit = 'mgdl';

        // Bind methods to preserve context
        this.calculateA1CtoGlucose = this.calculateA1CtoGlucose.bind(this);
        this.calculateGlucoseToA1C = this.calculateGlucoseToA1C.bind(this);
        this.setUnit = this.setUnit.bind(this);
        this.setReverseUnit = this.setReverseUnit.bind(this);
    }

    // ========================================================================
    // MATHEMATICAL CORE: ADAG Formula Implementation
    // ========================================================================

    /**
     * Convert A1C percentage to estimated average glucose (eAG)
     * Formula: eAG (mg/dL) = 28.7 × A1C - 46.7
     * @param {number} a1c - A1C percentage (3.0 - 20.0)
     * @param {string} unit - Output unit ('mgdl' or 'mmol')
     * @returns {object} Calculation result with value and metadata
     */
    convertA1CToGlucose(a1c, unit = 'mgdl') {
        if (!this.validateA1CInput(a1c)) {
            throw new Error(`A1C value ${a1c} is outside valid range (${MEDICAL_CONSTANTS.VALIDATION.A1C_MIN} - ${MEDICAL_CONSTANTS.VALIDATION.A1C_MAX}%)`);
        }

        // Apply ADAG formula with mathematical precision
        const glucoseMgDl = MEDICAL_CONSTANTS.ADAG.SLOPE * a1c - MEDICAL_CONSTANTS.ADAG.INTERCEPT;

        // Convert to requested unit with proper rounding
        const glucose = unit === 'mmol'
            ? this.precisionRound(glucoseMgDl / MEDICAL_CONSTANTS.ADAG.MMOL_DIVISOR, 1)
            : this.precisionRound(glucoseMgDl, 0);

        // Calculate confidence interval
        const standardError = unit === 'mmol'
            ? MEDICAL_CONSTANTS.ADAG.STANDARD_ERROR / MEDICAL_CONSTANTS.ADAG.MMOL_DIVISOR
            : MEDICAL_CONSTANTS.ADAG.STANDARD_ERROR;

        return {
            value: glucose,
            unit: unit,
            a1c: a1c,
            riskLevel: this.determineRiskLevel(a1c),
            confidenceInterval: {
                lower: this.precisionRound(glucose - 1.96 * standardError, unit === 'mmol' ? 1 : 0),
                upper: this.precisionRound(glucose + 1.96 * standardError, unit === 'mmol' ? 1 : 0)
            },
            timestamp: new Date().toISOString(),
            formula: 'ADAG'
        };
    }

    /**
     * Convert average glucose to estimated A1C
     * Formula: A1C (%) = (eAG mg/dL + 46.7) / 28.7
     * @param {number} glucose - Average glucose value
     * @param {string} unit - Input unit ('mgdl' or 'mmol')
     * @returns {object} Calculation result with A1C and metadata
     */
    convertGlucoseToA1C(glucose, unit = 'mgdl') {
        if (!this.validateGlucoseInput(glucose, unit)) {
            const bounds = unit === 'mmol'
                ? `${MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MIN_MMOL} - ${MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MAX_MMOL} mmol/L`
                : `${MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MIN_MGDL} - ${MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MAX_MGDL} mg/dL`;
            throw new Error(`Glucose value ${glucose} ${unit === 'mmol' ? 'mmol/L' : 'mg/dL'} is outside valid range (${bounds})`);
        }

        // Convert to mg/dL if necessary
        const glucoseMgDl = unit === 'mmol'
            ? glucose * MEDICAL_CONSTANTS.ADAG.MMOL_DIVISOR
            : glucose;

        // Apply inverse ADAG formula
        const a1c = this.precisionRound(
            (glucoseMgDl + MEDICAL_CONSTANTS.ADAG.INTERCEPT) / MEDICAL_CONSTANTS.ADAG.SLOPE,
            MEDICAL_CONSTANTS.VALIDATION.PRECISION_DIGITS
        );

        return {
            value: a1c,
            unit: '%',
            glucose: glucose,
            glucoseUnit: unit,
            riskLevel: this.determineRiskLevel(a1c),
            timestamp: new Date().toISOString(),
            formula: 'ADAG-Inverse'
        };
    }

    // ========================================================================
    // RISK ASSESSMENT: Medical Classification
    // ========================================================================

    /**
     * Determine medical risk level based on A1C value
     * @param {number} a1c - A1C percentage
     * @returns {object} Risk level information
     */
    determineRiskLevel(a1c) {
        const levels = MEDICAL_CONSTANTS.RISK_LEVELS;

        if (a1c < levels.NORMAL.max) {
            return levels.NORMAL;
        } else if (a1c >= levels.PREDIABETES.min && a1c < levels.PREDIABETES.max) {
            return levels.PREDIABETES;
        } else if (a1c >= levels.DIABETES_CONTROLLED.min && a1c < levels.DIABETES_CONTROLLED.max) {
            return levels.DIABETES_CONTROLLED;
        } else if (a1c >= levels.DIABETES_MODERATE.min && a1c < levels.DIABETES_MODERATE.max) {
            return levels.DIABETES_MODERATE;
        } else if (a1c >= levels.DIABETES_POOR.min && a1c < levels.DIABETES_POOR.max) {
            return levels.DIABETES_POOR;
        } else {
            return levels.DIABETES_DANGEROUS;
        }
    }

    // ========================================================================
    // VALIDATION: Input Sanitization & Bounds Checking
    // ========================================================================

    validateA1CInput(a1c) {
        return (
            typeof a1c === 'number' &&
            !isNaN(a1c) &&
            isFinite(a1c) &&
            a1c >= MEDICAL_CONSTANTS.VALIDATION.A1C_MIN &&
            a1c <= MEDICAL_CONSTANTS.VALIDATION.A1C_MAX
        );
    }

    validateGlucoseInput(glucose, unit) {
        if (typeof glucose !== 'number' || isNaN(glucose) || !isFinite(glucose)) {
            return false;
        }

        if (unit === 'mmol') {
            return glucose >= MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MIN_MMOL &&
                   glucose <= MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MAX_MMOL;
        } else {
            return glucose >= MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MIN_MGDL &&
                   glucose <= MEDICAL_CONSTANTS.VALIDATION.GLUCOSE_MAX_MGDL;
        }
    }

    // ========================================================================
    // UTILITIES: Mathematical & Data Operations
    // ========================================================================

    /**
     * Precision rounding to avoid floating point errors
     * @param {number} number - Number to round
     * @param {number} digits - Decimal places
     * @returns {number} Precisely rounded number
     */
    precisionRound(number, digits) {
        const multiplier = Math.pow(10, digits);
        return Math.round(number * multiplier) / multiplier;
    }

    /**
     * Format number for display with appropriate precision
     * @param {number} number - Number to format
     * @param {number} decimals - Decimal places
     * @returns {string} Formatted number string
     */
    formatNumber(number, decimals = 1) {
        if (!isFinite(number)) return '--';
        return number.toFixed(decimals);
    }

    // ========================================================================
    // HISTORY MANAGEMENT: Local Storage Operations
    // ========================================================================

    saveCalculation(calculation) {
        this.history.unshift({
            ...calculation,
            id: Date.now(),
            timestamp: new Date().toISOString()
        });

        // Keep only last 10 calculations
        this.history = this.history.slice(0, 10);

        this.calculationCount++;
        this.saveHistory();
        this.saveCalculationCount();
    }

    loadHistory() {
        try {
            const stored = localStorage.getItem('a1c_calc_history');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.warn('Failed to load calculation history:', error);
            return [];
        }
    }

    saveHistory() {
        try {
            localStorage.setItem('a1c_calc_history', JSON.stringify(this.history));
        } catch (error) {
            console.warn('Failed to save calculation history:', error);
        }
    }

    loadCalculationCount() {
        try {
            const count = localStorage.getItem('a1c_calc_count');
            return count ? parseInt(count, 10) : 0;
        } catch (error) {
            console.warn('Failed to load calculation count:', error);
            return 0;
        }
    }

    saveCalculationCount() {
        try {
            localStorage.setItem('a1c_calc_count', this.calculationCount.toString());
        } catch (error) {
            console.warn('Failed to save calculation count:', error);
        }
    }

    clearHistory() {
        this.history = [];
        this.saveHistory();
    }

    // ========================================================================
    // UNIT MANAGEMENT: mg/dL ↔ mmol/L Conversion
    // ========================================================================

    setUnit(unit) {
        this.currentUnit = unit;
        this.updateUnitButtons('unit-toggle-1', unit);
    }

    setReverseUnit(unit) {
        this.reverseUnit = unit;
        this.updateUnitButtons('unit-toggle-2', unit);
    }

    updateUnitButtons(containerId, activeUnit) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const buttons = container.querySelectorAll('button');
        buttons.forEach(button => {
            const isActive = button.dataset.unit === activeUnit;
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-checked', isActive);
        });
    }

    // ========================================================================
    // UI INTERFACE: DOM Interaction Methods
    // ========================================================================

    calculateA1CtoGlucose() {
        try {
            const a1cInput = document.getElementById('a1cInput');
            const a1c = parseFloat(a1cInput.value);

            if (!a1cInput.value.trim() || isNaN(a1c)) {
                this.clearResult('a1cResult');
                return;
            }

            const result = this.convertA1CToGlucose(a1c, this.currentUnit);
            this.displayA1CResult(result);
            this.saveCalculation({
                type: 'a1c_to_glucose',
                input: { a1c, unit: this.currentUnit },
                output: result
            });
            this.updateGauge(a1c);
            this.incrementCalculationCount();
            this.updateHistoryDisplay();

        } catch (error) {
            this.displayError('a1cResult', error.message);
            console.error('A1C calculation error:', error);
        }
    }

    calculateGlucoseToA1C() {
        try {
            const glucoseInput = document.getElementById('glucoseInput');
            const glucose = parseFloat(glucoseInput.value);

            if (!glucoseInput.value.trim() || isNaN(glucose)) {
                this.clearResult('glucoseResult');
                return;
            }

            const result = this.convertGlucoseToA1C(glucose, this.reverseUnit);
            this.displayGlucoseResult(result);
            this.saveCalculation({
                type: 'glucose_to_a1c',
                input: { glucose, unit: this.reverseUnit },
                output: result
            });
            this.incrementCalculationCount();
            this.updateHistoryDisplay();

        } catch (error) {
            this.displayError('glucoseResult', error.message);
            console.error('Glucose calculation error:', error);
        }
    }

    // ========================================================================
    // DISPLAY METHODS: Result Visualization
    // ========================================================================

    displayA1CResult(result) {
        const container = document.getElementById('a1cResult');
        if (!container) return;

        // Update value display
        const valueElement = container.querySelector('#eagValue');
        const unitElement = container.querySelector('#eagUnit');
        const riskElement = container.querySelector('#riskBadge');

        if (valueElement) {
            valueElement.textContent = this.formatNumber(result.value, result.unit === 'mmol' ? 1 : 0);
            this.animateValueChange(valueElement);
        }

        if (unitElement) {
            unitElement.textContent = result.unit === 'mmol' ? 'mmol/L' : 'mg/dL';
        }

        if (riskElement) {
            this.displayRiskBadge(riskElement, result.riskLevel);
        }

        // Update container styling
        container.style.borderColor = this.getRiskColor(result.riskLevel);
    }

    displayGlucoseResult(result) {
        const container = document.getElementById('glucoseResult');
        if (!container) return;

        const valueElement = container.querySelector('#a1cValue');
        const riskElement = container.querySelector('#revRiskBadge');

        if (valueElement) {
            valueElement.textContent = this.formatNumber(result.value, 1) + '%';
            this.animateValueChange(valueElement);
        }

        if (riskElement) {
            this.displayRiskBadge(riskElement, result.riskLevel);
        }

        container.style.borderColor = this.getRiskColor(result.riskLevel);
    }

    displayRiskBadge(element, riskLevel) {
        if (!element || !riskLevel) return;

        element.className = `risk-badge ${riskLevel.class}`;
        element.textContent = riskLevel.label;
        element.setAttribute('aria-label', `Risk level: ${riskLevel.label}`);
    }

    getRiskColor(riskLevel) {
        if (!riskLevel) return 'var(--color-border)';

        switch (riskLevel.class) {
            case 'risk-normal': return 'var(--color-success)';
            case 'risk-prediabetes': return 'var(--color-warning)';
            case 'risk-diabetes': return 'var(--color-danger)';
            default: return 'var(--color-border)';
        }
    }

    animateValueChange(element) {
        if (!element) return;

        element.style.animation = 'none';
        element.offsetHeight; // Trigger reflow
        element.style.animation = `fadeInScale ${MEDICAL_CONSTANTS.ANIMATION.RESULT_FADE_DURATION}ms ${MEDICAL_CONSTANTS.ANIMATION.GAUGE_EASING}`;
    }

    clearResult(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const valueElement = container.querySelector('.result-value');
        const riskElement = container.querySelector('.risk-badge');

        if (valueElement) valueElement.textContent = '--';
        if (riskElement) {
            riskElement.textContent = '';
            riskElement.className = 'risk-badge';
        }

        container.style.borderColor = 'var(--color-border)';
    }

    displayError(containerId, message) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const valueElement = container.querySelector('.result-value');
        if (valueElement) {
            valueElement.textContent = 'Error';
            valueElement.style.color = 'var(--color-danger)';
        }

        console.error(`Calculator Error (${containerId}):`, message);
    }

    incrementCalculationCount() {
        const countElement = document.getElementById('calc-count');
        if (countElement) {
            countElement.textContent = this.calculationCount.toString();
        }
    }

    updateHistoryDisplay() {
        const historyContainer = document.getElementById('historyList');
        if (!historyContainer) return;

        if (this.history.length === 0) {
            historyContainer.innerHTML = '<p style="color:#666;font-size:0.88rem;">No conversions yet. Try the calculator above.</p>';
            return;
        }

        const historyHTML = this.history.map(item => {
            const date = new Date(item.timestamp).toLocaleDateString();
            const time = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            if (item.type === 'a1c_to_glucose') {
                return `
                    <div class="history-item">
                        <span>A1C ${item.input.a1c}% → ${item.output.value} ${item.output.unit === 'mmol' ? 'mmol/L' : 'mg/dL'}</span>
                        <span class="date">${date} ${time}</span>
                    </div>
                `;
            } else {
                return `
                    <div class="history-item">
                        <span>${item.input.glucose} ${item.input.unit === 'mmol' ? 'mmol/L' : 'mg/dL'} → A1C ${item.output.value}%</span>
                        <span class="date">${date} ${time}</span>
                    </div>
                `;
            }
        }).join('');

        historyContainer.innerHTML = historyHTML;
    }

    // ========================================================================
    // GAUGE VISUALIZATION: Precision Medical Instrument
    // ========================================================================

    updateGauge(a1c) {
        const gaugeContainer = document.getElementById('gaugeContainer');
        const gaugeSvg = document.getElementById('gaugeSvg');

        if (!gaugeContainer || !gaugeSvg) return;

        // Clear existing gauge
        gaugeSvg.innerHTML = '';

        // Gauge parameters
        const centerX = 150;
        const centerY = 150;
        const radius = 100;
        const startAngle = -135;
        const endAngle = 45;
        const angleRange = endAngle - startAngle;

        // Create gauge background
        this.createGaugeBackground(gaugeSvg, centerX, centerY, radius, startAngle, endAngle);

        // Create gauge segments (risk zones)
        this.createGaugeSegments(gaugeSvg, centerX, centerY, radius, startAngle, angleRange);

        // Create gauge needle
        this.createGaugeNeedle(gaugeSvg, centerX, centerY, radius, a1c, startAngle, angleRange);

        // Create gauge labels
        this.createGaugeLabels(gaugeSvg, centerX, centerY, radius, startAngle, angleRange);
    }

    createGaugeBackground(svg, centerX, centerY, radius, startAngle, endAngle) {
        const startRad = (startAngle * Math.PI) / 180;
        const endRad = (endAngle * Math.PI) / 180;

        const x1 = centerX + radius * Math.cos(startRad);
        const y1 = centerY + radius * Math.sin(startRad);
        const x2 = centerX + radius * Math.cos(endRad);
        const y2 = centerY + radius * Math.sin(endRad);

        const largeArcFlag = endAngle - startAngle > 180 ? 1 : 0;

        const pathData = [
            `M ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`
        ].join(' ');

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathData);
        path.setAttribute('stroke', 'var(--color-border)');
        path.setAttribute('stroke-width', '8');
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke-linecap', 'round');

        svg.appendChild(path);
    }

    createGaugeSegments(svg, centerX, centerY, radius, startAngle, angleRange) {
        const segments = [
            { range: [0, 5.7], color: '#00ff88' },      // Normal
            { range: [5.7, 6.4], color: '#ffaa00' },    // Prediabetes
            { range: [6.4, 14], color: '#ff4444' }      // Diabetes
        ];

        segments.forEach(segment => {
            const startA1C = Math.max(segment.range[0], 4);
            const endA1C = Math.min(segment.range[1], 14);

            const startAngleSegment = startAngle + ((startA1C - 4) / 10) * angleRange;
            const endAngleSegment = startAngle + ((endA1C - 4) / 10) * angleRange;

            const startRad = (startAngleSegment * Math.PI) / 180;
            const endRad = (endAngleSegment * Math.PI) / 180;

            const x1 = centerX + radius * Math.cos(startRad);
            const y1 = centerY + radius * Math.sin(startRad);
            const x2 = centerX + radius * Math.cos(endRad);
            const y2 = centerY + radius * Math.sin(endRad);

            const pathData = [
                `M ${x1} ${y1}`,
                `A ${radius} ${radius} 0 0 1 ${x2} ${y2}`
            ].join(' ');

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', pathData);
            path.setAttribute('stroke', segment.color);
            path.setAttribute('stroke-width', '6');
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke-linecap', 'round');
            path.setAttribute('opacity', '0.8');

            svg.appendChild(path);
        });
    }

    createGaugeNeedle(svg, centerX, centerY, radius, a1c, startAngle, angleRange) {
        // Clamp A1C value to gauge range
        const clampedA1C = Math.max(4, Math.min(14, a1c));

        // Calculate needle angle
        const needleAngle = startAngle + ((clampedA1C - 4) / 10) * angleRange;
        const needleRad = (needleAngle * Math.PI) / 180;

        // Needle end point
        const needleLength = radius * 0.8;
        const needleX = centerX + needleLength * Math.cos(needleRad);
        const needleY = centerY + needleLength * Math.sin(needleRad);

        // Create needle
        const needle = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        needle.setAttribute('x1', centerX);
        needle.setAttribute('y1', centerY);
        needle.setAttribute('x2', needleX);
        needle.setAttribute('y2', needleY);
        needle.setAttribute('stroke', 'var(--color-primary)');
        needle.setAttribute('stroke-width', '3');
        needle.setAttribute('stroke-linecap', 'round');
        needle.classList.add('gauge-needle');

        // Center dot
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', centerX);
        dot.setAttribute('cy', centerY);
        dot.setAttribute('r', '6');
        dot.setAttribute('fill', 'var(--color-primary)');

        // Value text
        const valueText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        valueText.setAttribute('x', centerX);
        valueText.setAttribute('y', centerY + 40);
        valueText.setAttribute('class', 'gauge-value-text');
        valueText.textContent = `${a1c.toFixed(1)}%`;

        svg.appendChild(needle);
        svg.appendChild(dot);
        svg.appendChild(valueText);
    }

    createGaugeLabels(svg, centerX, centerY, radius, startAngle, angleRange) {
        const labels = [
            { value: 4, label: '4' },
            { value: 5.7, label: '5.7' },
            { value: 6.4, label: '6.4' },
            { value: 8, label: '8' },
            { value: 10, label: '10' },
            { value: 14, label: '14' }
        ];

        labels.forEach(labelData => {
            const angle = startAngle + ((labelData.value - 4) / 10) * angleRange;
            const angleRad = (angle * Math.PI) / 180;
            const labelRadius = radius + 20;

            const x = centerX + labelRadius * Math.cos(angleRad);
            const y = centerY + labelRadius * Math.sin(angleRad) + 5;

            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', x);
            text.setAttribute('y', y);
            text.setAttribute('class', 'gauge-label');
            text.textContent = labelData.label;

            svg.appendChild(text);
        });
    }
}

// ============================================================================
// INITIALIZATION & EVENT BINDING
// ============================================================================

// Global calculator instance
let calculator;

// Initialize calculator when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    calculator = new A1CCalculatorEngine();

    // Bind event listeners
    bindCalculatorEvents();

    // Initialize unit toggles
    calculator.setUnit('mgdl');
    calculator.setReverseUnit('mgdl');

    // Update calculation count display
    calculator.incrementCalculationCount();

    console.log('A1C Calculator Masterpiece Engine initialized successfully');
});

function bindCalculatorEvents() {
    // A1C input events
    const a1cInput = document.getElementById('a1cInput');
    if (a1cInput) {
        let a1cTimeout;
        a1cInput.addEventListener('input', function() {
            clearTimeout(a1cTimeout);
            a1cTimeout = setTimeout(calculator.calculateA1CtoGlucose, MEDICAL_CONSTANTS.ANIMATION.CALCULATION_DELAY);
        });
        a1cInput.addEventListener('blur', calculator.calculateA1CtoGlucose);
    }

    // Glucose input events
    const glucoseInput = document.getElementById('glucoseInput');
    if (glucoseInput) {
        let glucoseTimeout;
        glucoseInput.addEventListener('input', function() {
            clearTimeout(glucoseTimeout);
            glucoseTimeout = setTimeout(calculator.calculateGlucoseToA1C, MEDICAL_CONSTANTS.ANIMATION.CALCULATION_DELAY);
        });
        glucoseInput.addEventListener('blur', calculator.calculateGlucoseToA1C);
    }

    // Unit toggle events
    bindUnitToggleEvents('unit-toggle-1', calculator.setUnit);
    bindUnitToggleEvents('unit-toggle-2', calculator.setReverseUnit);

    // Button events
    bindButtonEvents();
}

function bindUnitToggleEvents(containerId, setterFunction) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const buttons = container.querySelectorAll('button[data-unit]');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const unit = this.dataset.unit;
            setterFunction.call(calculator, unit);

            // Re-calculate if inputs have values
            if (containerId === 'unit-toggle-1') {
                const input = document.getElementById('a1cInput');
                if (input && input.value.trim()) {
                    calculator.calculateA1CtoGlucose();
                }
            } else {
                const input = document.getElementById('glucoseInput');
                if (input && input.value.trim()) {
                    calculator.calculateGlucoseToA1C();
                }
            }
        });
    });
}

function bindButtonEvents() {
    // Calculate buttons
    const a1cButton = document.getElementById('calc-a1c-btn');
    if (a1cButton) {
        a1cButton.addEventListener('click', calculator.calculateA1CtoGlucose);
    }

    const glucoseButton = document.getElementById('calc-glucose-btn');
    if (glucoseButton) {
        glucoseButton.addEventListener('click', calculator.calculateGlucoseToA1C);
    }

    // Clear history button
    const clearButton = document.getElementById('clear-history-btn');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            if (confirm('Clear all calculation history? This cannot be undone.')) {
                calculator.clearHistory();
                calculator.updateHistoryDisplay();
            }
        });
    }
}

// Add CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);

// Export for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { A1CCalculatorEngine, MEDICAL_CONSTANTS };
}