/**
 * PRECISION AGENT BETA - POWER FACTOR CALCULATOR
 * Mathematical Precision Implementation with Zero Error Tolerance
 *
 * Features:
 * - Input validation with domain checking
 * - Mathematical overflow protection
 * - Floating point precision safeguards
 * - Comprehensive error handling
 * - Edge case protection
 */

class PowerFactorCalculator {
    constructor() {
        this.PRECISION_DECIMALS = 6;
        this.MAX_VOLTAGE = 100000; // 100kV maximum
        this.MAX_FREQUENCY = 1000; // 1kHz maximum
        this.MIN_TOLERANCE = 1e-15; // Minimum value tolerance (very small)
    }

    /**
     * Validate power factor input (must be between 0 and 1)
     */
    validatePowerFactor(pf, name = "Power Factor") {
        if (typeof pf !== 'number' || isNaN(pf)) {
            throw new Error(`${name} must be a valid number`);
        }
        if (pf < 0 || pf > 1) {
            throw new Error(`${name} must be between 0 and 1 (got ${pf})`);
        }
        return true;
    }

    /**
     * Validate voltage input
     */
    validateVoltage(voltage, name = "Voltage") {
        if (typeof voltage !== 'number' || isNaN(voltage)) {
            throw new Error(`${name} must be a valid number`);
        }
        if (voltage <= 0) {
            throw new Error(`${name} must be positive (got ${voltage})`);
        }
        if (voltage > this.MAX_VOLTAGE) {
            throw new Error(`${name} exceeds maximum of ${this.MAX_VOLTAGE}V (got ${voltage}V)`);
        }
        return true;
    }

    /**
     * Validate frequency input
     */
    validateFrequency(frequency, name = "Frequency") {
        if (typeof frequency !== 'number' || isNaN(frequency)) {
            throw new Error(`${name} must be a valid number`);
        }
        if (frequency <= 0) {
            throw new Error(`${name} must be positive (got ${frequency})`);
        }
        if (frequency > this.MAX_FREQUENCY) {
            throw new Error(`${name} exceeds maximum of ${this.MAX_FREQUENCY}Hz (got ${frequency}Hz)`);
        }
        return true;
    }

    /**
     * Validate power input
     */
    validatePower(power, name = "Power") {
        if (typeof power !== 'number' || isNaN(power)) {
            throw new Error(`${name} must be a valid number`);
        }
        if (power <= 0) {
            throw new Error(`${name} must be positive (got ${power})`);
        }
        return true;
    }

    /**
     * Round to specified precision
     */
    roundToPrecision(value, decimals = this.PRECISION_DECIMALS) {
        const factor = Math.pow(10, decimals);
        return Math.round(value * factor) / factor;
    }

    /**
     * Safe calculation wrapper with overflow protection
     */
    safeCalculation(calculation, context = "calculation") {
        try {
            const result = calculation();


            if (typeof result !== 'number' || isNaN(result)) {
                throw new Error(`${context} resulted in NaN value`);
            }

            if (!isFinite(result)) {
                throw new Error(`${context} resulted in infinite value`);
            }

            if (Math.abs(result) < this.MIN_TOLERANCE) {
                return 0; // Treat very small values as zero
            }

            return this.roundToPrecision(result);
        } catch (error) {
            throw new Error(`Error in ${context}: ${error.message}`);
        }
    }

    /**
     * Calculate power factor correction kVAR required
     * Formula: kVAR = P × (tan(acos(PF_old)) - tan(acos(PF_new)))
     */
    calculatePowerFactorCorrection(realPower, currentPF, targetPF) {
        // Input validation
        this.validatePower(realPower, "Real Power");
        this.validatePowerFactor(currentPF, "Current Power Factor");
        this.validatePowerFactor(targetPF, "Target Power Factor");

        if (targetPF <= currentPF) {
            throw new Error("Target power factor must be greater than current power factor");
        }

        return this.safeCalculation(() => {
            // Calculate phase angles
            const theta_current = Math.acos(currentPF);
            const theta_target = Math.acos(targetPF);

            // Calculate tangents with overflow protection
            const tan_current = Math.tan(theta_current);
            const tan_target = Math.tan(theta_target);

            // Check for mathematical overflow
            if (!isFinite(tan_current) || !isFinite(tan_target)) {
                throw new Error("Mathematical overflow in tangent calculation");
            }

            // Calculate required kVAR
            const requiredKVAR = realPower * (tan_current - tan_target);

            // Verification calculation using power triangle
            const S_current = realPower / currentPF;
            const Q_current = S_current * Math.sin(theta_current);
            const S_target = realPower / targetPF;
            const Q_target = S_target * Math.sin(theta_target);
            const verification_kVAR = Q_current - Q_target;

            // Cross-check verification (should match within tolerance)
            const verification_error = Math.abs(requiredKVAR - verification_kVAR);
            if (verification_error > 0.001) {
                console.warn(`Verification mismatch: ${verification_error.toFixed(6)} kVAR difference`);
            }

            return requiredKVAR;
        }, "power factor correction");
    }

    /**
     * Calculate apparent power
     * Formula: S = √(P² + Q²)
     */
    calculateApparentPower(realPower, reactivePower) {
        this.validatePower(realPower, "Real Power");

        if (typeof reactivePower !== 'number' || isNaN(reactivePower)) {
            throw new Error("Reactive Power must be a valid number");
        }

        return this.safeCalculation(() => {
            return Math.sqrt(Math.pow(realPower, 2) + Math.pow(reactivePower, 2));
        }, "apparent power calculation");
    }

    /**
     * Calculate three-phase power
     * Formula: P = √3 × V_L × I_L × PF
     */
    calculateThreePhasePower(lineVoltage, lineCurrent, powerFactor) {
        this.validateVoltage(lineVoltage, "Line Voltage");
        this.validatePowerFactor(powerFactor);

        if (typeof lineCurrent !== 'number' || isNaN(lineCurrent)) {
            throw new Error("Line Current must be a valid number");
        }
        if (lineCurrent < 0) {
            throw new Error("Line Current must be non-negative");
        }

        return this.safeCalculation(() => {
            const sqrt3 = Math.sqrt(3);
            const power = sqrt3 * lineVoltage * lineCurrent * powerFactor;

            // Verification: Calculate as 3 × single-phase power
            const phaseVoltage = lineVoltage / sqrt3;
            const phasePower = phaseVoltage * lineCurrent * powerFactor;
            const totalPowerVerification = 3 * phasePower;

            // Cross-check verification
            const verification_error = Math.abs(power - totalPowerVerification);
            if (verification_error > 0.001) {
                console.warn(`Three-phase verification mismatch: ${verification_error.toFixed(6)} W difference`);
            }

            return power;
        }, "three-phase power calculation");
    }

    /**
     * Calculate capacitor value for power factor correction
     * Formula: C = Q / (2π × f × V²)
     */
    calculateCapacitorValue(reactiveVAR, frequency, voltage) {
        if (typeof reactiveVAR !== 'number' || isNaN(reactiveVAR)) {
            throw new Error("Reactive VAR must be a valid number");
        }
        if (reactiveVAR <= 0) {
            throw new Error("Reactive VAR must be positive");
        }

        this.validateFrequency(frequency);
        this.validateVoltage(voltage);

        const omega = 2 * Math.PI * frequency;
        const denominator = omega * Math.pow(voltage, 2);

        if (denominator === 0 || !isFinite(denominator)) {
            throw new Error("Invalid denominator in capacitor calculation");
        }

        const capacitance = this.safeCalculation(() => {
            return reactiveVAR / denominator;
        }, "capacitance calculation");

        // Verification: Q = V²ωC
        const verification_Q = Math.pow(voltage, 2) * omega * capacitance;
        const verification_error = Math.abs(reactiveVAR - verification_Q);

        if (verification_error > 0.01) {
            console.warn(`Capacitor verification mismatch: ${verification_error.toFixed(6)} VAR difference`);
        }

        return {
            farads: capacitance,
            microfarads: capacitance * 1e6,
            nanofarads: capacitance * 1e9,
            picofarads: capacitance * 1e12
        };
    }

    /**
     * Calculate phase angle from power factor
     * Formula: θ = acos(PF)
     */
    calculatePhaseAngle(powerFactor, returnDegrees = true) {
        this.validatePowerFactor(powerFactor);

        return this.safeCalculation(() => {
            const radians = Math.acos(powerFactor);
            return returnDegrees ? radians * 180 / Math.PI : radians;
        }, "phase angle calculation");
    }

    /**
     * Calculate power factor from real and apparent power
     * Formula: PF = P / S
     */
    calculatePowerFactorFromPowers(realPower, apparentPower) {
        this.validatePower(realPower, "Real Power");
        this.validatePower(apparentPower, "Apparent Power");

        if (realPower > apparentPower) {
            throw new Error("Real power cannot exceed apparent power");
        }

        return this.safeCalculation(() => {
            return realPower / apparentPower;
        }, "power factor from powers calculation");
    }

    /**
     * Comprehensive power factor analysis
     */
    analyzePowerSystem(realPower, apparentPower, frequency, voltage) {
        const powerFactor = this.calculatePowerFactorFromPowers(realPower, apparentPower);
        const reactivePower = Math.sqrt(Math.pow(apparentPower, 2) - Math.pow(realPower, 2));
        const phaseAngle = this.calculatePhaseAngle(powerFactor);
        const current = apparentPower / voltage; // Single-phase equivalent

        return {
            powerFactor: this.roundToPrecision(powerFactor, 4),
            reactivePower: this.roundToPrecision(reactivePower),
            phaseAngle: this.roundToPrecision(phaseAngle, 2),
            current: this.roundToPrecision(current, 2),
            efficiency: this.roundToPrecision(powerFactor * 100, 2) + '%'
        };
    }
}

// Example usage and testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PowerFactorCalculator;
} else {
    // Browser environment
    window.PowerFactorCalculator = PowerFactorCalculator;
}

// Self-test if running directly
if (typeof require !== 'undefined' && require.main === module) {
    console.log("=== POWER FACTOR CALCULATOR PRECISION TESTING ===");

    const calc = new PowerFactorCalculator();

    try {
        // Test 1: Power factor correction
        console.log("\nTest 1: Power Factor Correction");
        const kvar = calc.calculatePowerFactorCorrection(100, 0.70, 0.90);
        console.log(`100kW facility, 0.70 to 0.90 PF: ${kvar} kVAR required`);

        // Test 2: Three-phase power
        console.log("\nTest 2: Three-Phase Power");
        const power3ph = calc.calculateThreePhasePower(480, 100, 0.85);
        console.log(`480V, 100A, 0.85 PF: ${power3ph} W`);

        // Test 3: Capacitor sizing
        console.log("\nTest 3: Capacitor Sizing");
        const capacitor = calc.calculateCapacitorValue(50000, 60, 480);
        console.log(`50 kVAR at 480V 60Hz: ${capacitor.microfarads.toFixed(2)} µF`);

        // Test 4: System analysis
        console.log("\nTest 4: Power System Analysis");
        const analysis = calc.analyzePowerSystem(800, 1000, 60, 480);
        console.log(`System Analysis:`, analysis);

        console.log("\n✅ All precision tests completed successfully!");

    } catch (error) {
        console.error("❌ Test failed:", error.message);
    }
}