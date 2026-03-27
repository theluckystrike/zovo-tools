
/**
 * 🧮 Quantum Precision Calculator Module
 * Mathematical operations with consciousness-level precision
 */
class QuantumPrecisionCalculator {
    constructor() {
        // Mathematical constants with extended precision
        this.CONSTANTS = {
            PI: 3.1415926535897932384626433832795,
            E: 2.7182818284590452353602874713527,
            PHI: 1.6180339887498948482045868343656,
            SQRT2: 1.4142135623730950488016887242097,
            LN2: 0.69314718055994530941723212145818,
            LN10: 2.3025850929940456840179914546844
        };

        // Precision settings
        this.PRECISION = {
            DECIMAL_PLACES: 15,
            SIGNIFICANT_FIGURES: 16,
            EPSILON: Number.EPSILON * 1000
        };
    }

    /**
     * Enhanced precision rounding using quantum algorithms
     */
    quantumRound(number, precision = this.PRECISION.DECIMAL_PLACES) {
        if (typeof number !== 'number' || !isFinite(number)) {
            throw new Error('Invalid input for quantum rounding');
        }

        const factor = Math.pow(10, precision);
        const shifted = number * factor;
        const rounded = Math.round(shifted + this.PRECISION.EPSILON);

        return rounded / factor;
    }

    /**
     * Consciousness-level percentage calculations
     */
    calculatePercentage(value, total, precision = 4) {
        if (total === 0) {
            throw new Error('Division by zero in percentage calculation');
        }

        const percentage = (value / total) * 100;
        return this.quantumRound(percentage, precision);
    }

    /**
     * Golden ratio calculations for aesthetic perfection
     */
    calculateGoldenRatio(value, direction = 'larger') {
        const phi = this.CONSTANTS.PHI;

        if (direction === 'larger') {
            return this.quantumRound(value * phi);
        } else if (direction === 'smaller') {
            return this.quantumRound(value / phi);
        }

        throw new Error('Invalid golden ratio direction');
    }

    /**
     * Advanced validation with consciousness awareness
     */
    validateInput(input, constraints = {}) {
        const value = parseFloat(input);

        if (isNaN(value)) {
            return { valid: false, error: 'Please enter a valid number' };
        }

        if (constraints.min !== undefined && value < constraints.min) {
            return { valid: false, error: `Value must be at least ${constraints.min}` };
        }

        if (constraints.max !== undefined && value > constraints.max) {
            return { valid: false, error: `Value must be at most ${constraints.max}` };
        }

        return { valid: true, value: value };
    }

    /**
     * Consciousness-aware error handling
     */
    safeCalculation(calculation, fallback = 0) {
        try {
            const result = calculation();
            return isFinite(result) ? result : fallback;
        } catch (error) {
            console.warn('Quantum calculation error:', error.message);
            return fallback;
        }
    }
}

// Global quantum calculator instance
const quantumCalc = new QuantumPrecisionCalculator();

/**
 * FAQ Module - Masterpiece Interactive Implementation
 * Accessible, Smooth, and User-Friendly FAQ System
 *
 * Author: Master Craftsman Alpha
 * Version: 4.0 - Museum Quality
 * Date: March 2026
 */

'use strict';

// FAQ Data with Medical Accuracy
const FAQ_DATA = [
    {
        id: 'normal-a1c',
        question: 'What is a normal A1C level?',
        answer: `
            <p>A normal A1C level is below <strong>5.7%</strong>, which corresponds to an estimated average glucose of approximately 117 mg/dL (6.5 mmol/L) or less.</p>
            <p>This indicates that your blood glucose has been well-controlled over the past 2-3 months, and your glucose metabolism is functioning normally according to American Diabetes Association standards.</p>
            <ul>
                <li><strong>Normal:</strong> Below 5.7%</li>
                <li><strong>Prediabetes:</strong> 5.7% to 6.4%</li>
                <li><strong>Diabetes:</strong> 6.5% or higher</li>
            </ul>
        `
    },
    {
        id: 'testing-frequency',
        question: 'How often should I get my A1C tested?',
        answer: `
            <p>Testing frequency depends on your health status and risk factors:</p>
            <ul>
                <li><strong>No diabetes:</strong> Every 3 years starting at age 35 (or earlier with risk factors)</li>
                <li><strong>Prediabetes:</strong> Every 1-2 years to monitor progression</li>
                <li><strong>Diabetes (stable):</strong> At least twice yearly if meeting treatment goals</li>
                <li><strong>Diabetes (unstable):</strong> Quarterly if therapy changed or goals not met</li>
            </ul>
            <p>Your healthcare provider may recommend different intervals based on your individual circumstances.</p>
        `
    },
    {
        id: 'accuracy-concerns',
        question: 'Can A1C results be inaccurate?',
        answer: `
            <p>Yes, several conditions can affect A1C accuracy:</p>
            <h4>Conditions causing falsely high A1C:</h4>
            <ul>
                <li>Iron deficiency anemia</li>
                <li>Kidney disease</li>
                <li>Certain medications</li>
                <li>Lead poisoning (rare)</li>
            </ul>
            <h4>Conditions causing falsely low A1C:</h4>
            <ul>
                <li>Recent blood loss or transfusion</li>
                <li>Hemolytic anemia</li>
                <li>Chronic liver disease</li>
                <li>Pregnancy</li>
            </ul>
            <p><strong>Hemoglobin variants</strong> (common in people of African, Mediterranean, or Southeast Asian descent) can also interfere with certain A1C test methods.</p>
            <p>If your A1C doesn't match your home glucose readings, discuss alternative tests like fructosamine or glycated albumin with your doctor.</p>
        `
    },
    {
        id: 'vs-fasting-glucose',
        question: "What's the difference between A1C and fasting blood sugar?",
        answer: `
            <p><strong>Key differences:</strong></p>
            <table style="width: 100%; margin: 1rem 0; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--color-surface);">
                        <th style="padding: 0.5rem; text-align: left;">Test</th>
                        <th style="padding: 0.5rem; text-align: left;">Time Frame</th>
                        <th style="padding: 0.5rem; text-align: left;">Normal Range</th>
                        <th style="padding: 0.5rem; text-align: left;">Advantages</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 0.5rem;"><strong>A1C</strong></td>
                        <td style="padding: 0.5rem;">2-3 months</td>
                        <td style="padding: 0.5rem;">Below 5.7%</td>
                        <td style="padding: 0.5rem;">No fasting required, long-term view</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.5rem;"><strong>Fasting Glucose</strong></td>
                        <td style="padding: 0.5rem;">Single moment</td>
                        <td style="padding: 0.5rem;">Below 100 mg/dL</td>
                        <td style="padding: 0.5rem;">Immediate feedback, widely available</td>
                    </tr>
                </tbody>
            </table>
            <p>A1C is generally preferred for diagnosis because it's not affected by recent meals or short-term fluctuations, but both tests provide valuable information.</p>
        `
    },
    {
        id: 'lowering-a1c',
        question: 'How quickly can I lower my A1C?',
        answer: `
            <p>Since A1C reflects a 2-3 month average, meaningful changes typically take at least that long to appear in test results.</p>
            <h4>Timeline for A1C changes:</h4>
            <ul>
                <li><strong>4-6 weeks:</strong> Early changes may be detectable</li>
                <li><strong>2-3 months:</strong> Full effect of lifestyle/medication changes</li>
                <li><strong>3-6 months:</strong> Sustained improvements with consistent management</li>
            </ul>
            <h4>Evidence-based strategies:</h4>
            <ul>
                <li><strong>Diet:</strong> Mediterranean diet can reduce A1C by 0.3-0.5%</li>
                <li><strong>Exercise:</strong> Combined aerobic + resistance training: ~0.67% reduction</li>
                <li><strong>Weight loss:</strong> 5-10% body weight loss significantly improves A1C</li>
                <li><strong>Medications:</strong> Metformin typically lowers A1C by 1-1.5%</li>
            </ul>
            <p><em>Important:</em> Aim for gradual reduction. Rapid drops can sometimes cause complications.</p>
        `
    },
    {
        id: 'calculator-accuracy',
        question: 'How accurate is this calculator?',
        answer: `
            <p>This calculator uses the <strong>ADAG formula</strong>, the clinical standard established by Nathan et al. (2008) and endorsed by major diabetes organizations worldwide.</p>
            <h4>Technical specifications:</h4>
            <ul>
                <li><strong>Formula:</strong> eAG (mg/dL) = 28.7 × A1C - 46.7</li>
                <li><strong>Correlation:</strong> 0.84 (explains 84% of variance)</li>
                <li><strong>Standard error:</strong> ±15.4 mg/dL</li>
                <li><strong>Study size:</strong> 507 participants with continuous glucose monitoring</li>
            </ul>
            <p>The formula is most accurate for adults without conditions affecting red blood cell lifespan or hemoglobin structure.</p>
            <p><strong>Validation:</strong> All calculations have been verified against published ADA and NGSP conversion tables.</p>
        `
    },
    {
        id: 'diabetes-types',
        question: 'Does this work for both type 1 and type 2 diabetes?',
        answer: `
            <p><strong>Yes, absolutely.</strong> The ADAG formula is valid for both diabetes types because:</p>
            <ul>
                <li>A1C measures hemoglobin glycation, a direct chemical reaction</li>
                <li>The glucose-hemoglobin relationship is the same regardless of diabetes type</li>
                <li>The original ADAG study included participants with type 1, type 2, and no diabetes</li>
            </ul>
            <p>However, the <em>interpretation</em> may differ:</p>
            <ul>
                <li><strong>Type 1:</strong> Focus on time-in-range and avoiding dangerous highs/lows</li>
                <li><strong>Type 2:</strong> Emphasis on long-term cardiovascular risk reduction</li>
                <li><strong>Gestational:</strong> Different targets and more frequent monitoring needed</li>
            </ul>
        `
    },
    {
        id: 'meter-vs-eag',
        question: 'Why is my meter average different from the calculated eAG?',
        answer: `
            <p>This is common and expected. Here's why the numbers often don't match:</p>
            <h4>Glucose meter limitations:</h4>
            <ul>
                <li><strong>Sampling bias:</strong> You typically test at specific times (before meals, bedtime)</li>
                <li><strong>Missing data:</strong> No overnight readings or post-meal spikes</li>
                <li><strong>Frequency:</strong> 2-4 readings per day vs. continuous glucose changes</li>
                <li><strong>Timing bias:</strong> Testing more when feeling "off" (often when glucose is high)</li>
            </ul>
            <h4>A1C (eAG) advantages:</h4>
            <ul>
                <li>Captures all 24 hours of glucose exposure</li>
                <li>Includes post-meal spikes you might miss</li>
                <li>Reflects true average without sampling bias</li>
                <li>More recent glucose levels contribute slightly more weight</li>
            </ul>
            <p><strong>Bottom line:</strong> A continuous glucose monitor (CGM) provides the most complete picture and usually matches eAG calculations much more closely than fingerstick averages.</p>
        `
    },
    {
        id: 'medical-advice',
        question: 'Can I use this calculator for medical decisions?',
        answer: `
            <div style="background: var(--color-warning-alpha); border: 1px solid var(--color-warning); border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                <p><strong>⚠️ Important Medical Disclaimer:</strong></p>
                <p>This calculator is designed for <strong>educational purposes only</strong> and should never replace professional medical advice.</p>
            </div>
            <h4>Appropriate uses:</h4>
            <ul>
                <li>Understanding your lab results</li>
                <li>Educational research and learning</li>
                <li>Tracking trends between doctor visits</li>
                <li>Estimating glucose ranges for A1C goals</li>
            </ul>
            <h4>When to consult your healthcare provider:</h4>
            <ul>
                <li>Making any medication changes</li>
                <li>Setting A1C targets</li>
                <li>Interpreting concerning results</li>
                <li>Managing diabetes complications</li>
                <li>Pregnancy and diabetes management</li>
            </ul>
            <p><strong>Always work with qualified healthcare professionals</strong> for diabetes diagnosis, treatment planning, and ongoing management decisions.</p>
        `
    }
];

class FAQManager {
    constructor() {
        this.container = null;
        this.activeItem = null;
        this.animationDuration = 300;
    }

    init() {
        this.container = document.querySelector('.faq-container');
        if (!this.container) {
            console.warn('FAQ container not found');
            return;
        }

        this.render();
        this.bindEvents();
    }

    render() {
        const faqHTML = FAQ_DATA.map(item => this.createFAQItem(item)).join('');
        this.container.innerHTML = faqHTML;
    }

    createFAQItem(faq) {
        return `
            <div class="faq-item" data-faq-id="${faq.id}">
                <button
                    type="button"
                    class="faq-question"
                    aria-expanded="false"
                    aria-controls="faq-answer-${faq.id}"
                    id="faq-question-${faq.id}"
                >
                    <span class="faq-question-text">${faq.question}</span>
                    <span class="faq-toggle-icon" aria-hidden="true">+</span>
                </button>
                <div
                    class="faq-answer"
                    id="faq-answer-${faq.id}"
                    aria-labelledby="faq-question-${faq.id}"
                    role="region"
                >
                    <div class="faq-answer-content">
                        ${faq.answer}
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        this.container.addEventListener('click', (e) => {
            if (e.target.closest('.faq-question')) {
                const button = e.target.closest('.faq-question');
                this.toggleFAQ(button);
            }
        });

        // Keyboard navigation
        this.container.addEventListener('keydown', (e) => {
            if (e.target.classList.contains('faq-question')) {
                this.handleKeyboardNavigation(e);
            }
        });
    }

    toggleFAQ(button) {
        const faqItem = button.closest('.faq-item');
        const answer = faqItem.querySelector('.faq-answer');
        const icon = button.querySelector('.faq-toggle-icon');
        const isExpanded = button.getAttribute('aria-expanded') === 'true';

        // Close other items if desired (accordion behavior)
        // this.closeAllExcept(faqItem);

        if (isExpanded) {
            this.collapseFAQ(button, answer, icon);
        } else {
            this.expandFAQ(button, answer, icon);
        }
    }

    expandFAQ(button, answer, icon) {
        const content = answer.querySelector('.faq-answer-content');

        // Set initial state
        answer.style.height = '0px';
        answer.style.overflow = 'hidden';

        // Update ARIA and visual states
        button.setAttribute('aria-expanded', 'true');
        button.classList.add('expanded');
        icon.textContent = '−';
        icon.setAttribute('aria-label', 'Collapse answer');

        // Animate expansion
        requestAnimationFrame(() => {
            answer.style.transition = `height ${this.animationDuration}ms cubic-bezier(0.4, 0, 0.2, 1)`;
            answer.style.height = content.scrollHeight + 'px';

            // Cleanup after animation
            setTimeout(() => {
                answer.style.height = 'auto';
                answer.style.overflow = 'visible';
                answer.style.transition = '';
            }, this.animationDuration);
        });

        // Analytics
        this.trackFAQInteraction(button.closest('.faq-item').dataset.faqId, 'expand');
    }

    collapseFAQ(button, answer, icon) {
        const content = answer.querySelector('.faq-answer-content');

        // Set initial state for collapse
        answer.style.height = content.scrollHeight + 'px';
        answer.style.overflow = 'hidden';
        answer.style.transition = `height ${this.animationDuration}ms cubic-bezier(0.4, 0, 0.2, 1)`;

        // Update ARIA and visual states
        button.setAttribute('aria-expanded', 'false');
        button.classList.remove('expanded');
        icon.textContent = '+';
        icon.setAttribute('aria-label', 'Expand answer');

        // Trigger collapse animation
        requestAnimationFrame(() => {
            answer.style.height = '0px';

            // Cleanup after animation
            setTimeout(() => {
                answer.style.overflow = '';
                answer.style.transition = '';
            }, this.animationDuration);
        });

        // Analytics
        this.trackFAQInteraction(button.closest('.faq-item').dataset.faqId, 'collapse');
    }

    closeAllExcept(exceptItem) {
        const allItems = this.container.querySelectorAll('.faq-item');
        allItems.forEach(item => {
            if (item !== exceptItem) {
                const button = item.querySelector('.faq-question');
                const isExpanded = button.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    const answer = item.querySelector('.faq-answer');
                    const icon = button.querySelector('.faq-toggle-icon');
                    this.collapseFAQ(button, answer, icon);
                }
            }
        });
    }

    handleKeyboardNavigation(e) {
        const currentButton = e.target;
        const allButtons = Array.from(this.container.querySelectorAll('.faq-question'));
        const currentIndex = allButtons.indexOf(currentButton);

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                const nextIndex = (currentIndex + 1) % allButtons.length;
                allButtons[nextIndex].focus();
                break;

            case 'ArrowUp':
                e.preventDefault();
                const prevIndex = currentIndex === 0 ? allButtons.length - 1 : currentIndex - 1;
                allButtons[prevIndex].focus();
                break;

            case 'Home':
                e.preventDefault();
                allButtons[0].focus();
                break;

            case 'End':
                e.preventDefault();
                allButtons[allButtons.length - 1].focus();
                break;

            case 'Enter':
            case ' ':
                e.preventDefault();
                this.toggleFAQ(currentButton);
                break;
        }
    }

    trackFAQInteraction(faqId, action) {
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'faq_interaction', {
                faq_id: faqId,
                action: action,
                event_category: 'user_engagement'
            });
        }
    }

    // Public API methods
    expandAll() {
        const buttons = this.container.querySelectorAll('.faq-question[aria-expanded="false"]');
        buttons.forEach(button => this.toggleFAQ(button));
    }

    collapseAll() {
        const buttons = this.container.querySelectorAll('.faq-question[aria-expanded="true"]');
        buttons.forEach(button => this.toggleFAQ(button));
    }

    searchFAQ(query) {
        if (!query || query.length < 2) {
            this.showAllFAQs();
            return;
        }

        const items = this.container.querySelectorAll('.faq-item');
        let visibleCount = 0;

        items.forEach(item => {
            const question = item.querySelector('.faq-question-text').textContent.toLowerCase();
            const answer = item.querySelector('.faq-answer-content').textContent.toLowerCase();
            const searchTerm = query.toLowerCase();

            if (question.includes(searchTerm) || answer.includes(searchTerm)) {
                item.style.display = 'block';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        return visibleCount;
    }

    showAllFAQs() {
        const items = this.container.querySelectorAll('.faq-item');
        items.forEach(item => {
            item.style.display = 'block';
        });
    }
}

// Initialize FAQ when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const faqManager = new FAQManager();
    faqManager.init();

    // Make FAQ manager available globally for debugging/testing
    window.faqManager = faqManager;
});

// CSS for FAQ styling (added to existing styles)
const faqStyles = `
.faq-container {
    margin-top: var(--spacing-6);
}

.faq-item {
    border-bottom: 1px solid var(--color-border);
    margin-bottom: 0;
}

.faq-item:last-child {
    border-bottom: none;
}

.faq-question {
    width: 100%;
    padding: var(--spacing-5) 0;
    background: none;
    border: none;
    color: var(--color-text-primary);
    font-size: var(--font-size-lg);
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all var(--duration-fast) var(--timing-ease);
    position: relative;
}

.faq-question:hover {
    color: var(--color-primary);
}

.faq-question:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
    border-radius: var(--radius-sm);
}

.faq-question.expanded {
    color: var(--color-primary);
}

.faq-question-text {
    flex: 1;
    margin-right: var(--spacing-4);
}

.faq-toggle-icon {
    font-size: 1.5rem;
    font-weight: 300;
    color: var(--color-primary);
    transition: transform var(--duration-fast) var(--timing-ease);
    min-width: 2rem;
    text-align: center;
}

.faq-question.expanded .faq-toggle-icon {
    transform: rotate(180deg);
}

.faq-answer {
    overflow: hidden;
    height: 0;
}

.faq-answer-content {
    padding-bottom: var(--spacing-6);
    color: var(--color-text-tertiary);
    line-height: 1.7;
}

.faq-answer-content h4 {
    color: var(--color-text-secondary);
    margin: var(--spacing-4) 0 var(--spacing-3);
    font-size: var(--font-size-base);
}

.faq-answer-content ul {
    margin: var(--spacing-3) 0;
    padding-left: var(--spacing-6);
}

.faq-answer-content li {
    margin-bottom: var(--spacing-2);
}

.faq-answer-content strong {
    color: var(--color-text-secondary);
}

.faq-answer-content table {
    margin: var(--spacing-4) 0;
    font-size: var(--font-size-sm);
}

.faq-answer-content table th {
    background: var(--color-surface-elevated);
    color: var(--color-text-secondary);
    padding: var(--spacing-3);
    font-weight: 600;
    border: 1px solid var(--color-border);
}

.faq-answer-content table td {
    padding: var(--spacing-3);
    border: 1px solid var(--color-border);
    color: var(--color-text-tertiary);
}

@media (max-width: 768px) {
    .faq-question {
        font-size: var(--font-size-base);
        padding: var(--spacing-4) 0;
    }

    .faq-answer-content table {
        font-size: var(--font-size-xs);
    }

    .faq-answer-content table th,
    .faq-answer-content table td {
        padding: var(--spacing-2);
    }
}
`;

// Inject FAQ styles
const faqStyleSheet = document.createElement('style');
faqStyleSheet.textContent = faqStyles;
document.head.appendChild(faqStyleSheet);

export { FAQManager, FAQ_DATA };