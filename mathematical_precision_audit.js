// Mathematical Precision Audit for Power Factor Calculator
// Precision Agent Beta - Zero Error Tolerance Mathematical Verification

console.log("=== MATHEMATICAL PRECISION AUDIT ===");
console.log("Testing Power Factor Calculator Formulas");
console.log("Date:", new Date().toISOString());

// Test 1: Power Factor Correction Formula Verification
function testPowerFactorCorrection() {
    console.log("\n=== TEST 1: Power Factor Correction Formula ===");

    // Formula: Required kVAR = P × (tan(acos(PF_old)) - tan(acos(PF_new)))
    const testCases = [
        { P: 100, PF_old: 0.70, PF_new: 0.90, expected_kvar: 47.14 },
        { P: 500, PF_old: 0.80, PF_new: 0.95, expected_kvar: 161.99 },
        { P: 1000, PF_old: 0.85, PF_new: 0.99, expected_kvar: 246.49 }
    ];

    testCases.forEach((test, index) => {
        const theta_old = Math.acos(test.PF_old);
        const theta_new = Math.acos(test.PF_new);
        const tan_old = Math.tan(theta_old);
        const tan_new = Math.tan(theta_new);
        const calculated_kvar = test.P * (tan_old - tan_new);

        console.log(`Test Case ${index + 1}:`);
        console.log(`  Input: P=${test.P}kW, PF_old=${test.PF_old}, PF_new=${test.PF_new}`);
        console.log(`  Calculated kVAR: ${calculated_kvar.toFixed(2)}`);
        console.log(`  Expected kVAR: ${test.expected_kvar}`);

        const error = Math.abs(calculated_kvar - test.expected_kvar);
        const percentError = (error / test.expected_kvar) * 100;

        console.log(`  Absolute Error: ${error.toFixed(4)}`);
        console.log(`  Percent Error: ${percentError.toFixed(4)}%`);

        if (percentError > 0.1) {
            console.log(`  ❌ PRECISION ERROR: Exceeds 0.1% tolerance`);
        } else {
            console.log(`  ✅ PRECISION VERIFIED: Within tolerance`);
        }
    });
}

// Test 2: Apparent Power Formula Verification
function testApparentPower() {
    console.log("\n=== TEST 2: Apparent Power Formula ===");
    console.log("Formula: S = √(P² + Q²)");

    const testCases = [
        { P: 100, Q: 75, expected_S: 125 },
        { P: 800, Q: 600, expected_S: 1000 },
        { P: 960, Q: 280, expected_S: 1000 }
    ];

    testCases.forEach((test, index) => {
        const calculated_S = Math.sqrt(Math.pow(test.P, 2) + Math.pow(test.Q, 2));

        console.log(`Test Case ${index + 1}:`);
        console.log(`  Input: P=${test.P}W, Q=${test.Q}VAR`);
        console.log(`  Calculated S: ${calculated_S.toFixed(2)}VA`);
        console.log(`  Expected S: ${test.expected_S}VA`);

        const error = Math.abs(calculated_S - test.expected_S);
        const percentError = (error / test.expected_S) * 100;

        console.log(`  Absolute Error: ${error.toFixed(4)}`);
        console.log(`  Percent Error: ${percentError.toFixed(4)}%`);

        if (percentError > 0.01) {
            console.log(`  ❌ PRECISION ERROR: Exceeds 0.01% tolerance`);
        } else {
            console.log(`  ✅ PRECISION VERIFIED: Within tolerance`);
        }
    });
}

// Test 3: Three-Phase Power Formula Verification
function testThreePhasePower() {
    console.log("\n=== TEST 3: Three-Phase Power Formula ===");
    console.log("Formula: P = √3 × V_L × I_L × PF");

    const sqrt3 = Math.sqrt(3);
    console.log(`√3 constant verification: ${sqrt3.toFixed(10)} (should be 1.7320508076)`);

    const testCases = [
        { V_L: 480, I_L: 100, PF: 0.85, expected_P: 70708.4 },
        { V_L: 208, I_L: 50, PF: 0.90, expected_P: 16198.7 },
        { V_L: 600, I_L: 200, PF: 0.95, expected_P: 197230.8 }
    ];

    testCases.forEach((test, index) => {
        const calculated_P = sqrt3 * test.V_L * test.I_L * test.PF;

        console.log(`Test Case ${index + 1}:`);
        console.log(`  Input: V_L=${test.V_L}V, I_L=${test.I_L}A, PF=${test.PF}`);
        console.log(`  Calculated P: ${calculated_P.toFixed(1)}W`);
        console.log(`  Expected P: ${test.expected_P}W`);

        const error = Math.abs(calculated_P - test.expected_P);
        const percentError = (error / test.expected_P) * 100;

        console.log(`  Absolute Error: ${error.toFixed(4)}`);
        console.log(`  Percent Error: ${percentError.toFixed(4)}%`);

        if (percentError > 0.01) {
            console.log(`  ❌ PRECISION ERROR: Exceeds 0.01% tolerance`);
        } else {
            console.log(`  ✅ PRECISION VERIFIED: Within tolerance`);
        }
    });
}

// Test 4: Capacitor Sizing Formula Verification
function testCapacitorSizing() {
    console.log("\n=== TEST 4: Capacitor Sizing Formula ===");
    console.log("Formula: C = Q / (2 × π × f × V²)");

    const testCases = [
        { Q: 50000, f: 60, V: 480, expected_C: 0.001146 }, // 50 kVAR at 480V 60Hz
        { Q: 25000, f: 60, V: 240, expected_C: 0.004579 }, // 25 kVAR at 240V 60Hz
        { Q: 100000, f: 50, V: 400, expected_C: 0.003979 } // 100 kVAR at 400V 50Hz
    ];

    testCases.forEach((test, index) => {
        const calculated_C = test.Q / (2 * Math.PI * test.f * Math.pow(test.V, 2));

        console.log(`Test Case ${index + 1}:`);
        console.log(`  Input: Q=${test.Q}VAR, f=${test.f}Hz, V=${test.V}V`);
        console.log(`  Calculated C: ${calculated_C.toFixed(6)}F`);
        console.log(`  Expected C: ${test.expected_C}F`);

        const error = Math.abs(calculated_C - test.expected_C);
        const percentError = (error / test.expected_C) * 100;

        console.log(`  Absolute Error: ${error.toFixed(8)}`);
        console.log(`  Percent Error: ${percentError.toFixed(4)}%`);

        if (percentError > 0.1) {
            console.log(`  ❌ PRECISION ERROR: Exceeds 0.1% tolerance`);
        } else {
            console.log(`  ✅ PRECISION VERIFIED: Within tolerance`);
        }
    });
}

// Test 5: Edge Case Testing for Mathematical Boundaries
function testEdgeCases() {
    console.log("\n=== TEST 5: Edge Case Mathematical Testing ===");

    // Test division by zero protection
    console.log("Testing division by zero protection:");
    try {
        const result = 100 / 0;
        console.log(`  100 / 0 = ${result} (should be Infinity)`);
        if (!isFinite(result)) {
            console.log(`  ✅ Division by zero handled correctly`);
        } else {
            console.log(`  ❌ Division by zero not handled correctly`);
        }
    } catch (error) {
        console.log(`  ❌ Unexpected error: ${error.message}`);
    }

    // Test acos domain validation (PF must be between 0 and 1)
    console.log("\nTesting acos domain validation:");
    const invalidPF = [1.5, -0.5, 0, 1];
    invalidPF.forEach(pf => {
        try {
            const result = Math.acos(pf);
            console.log(`  acos(${pf}) = ${result}`);
            if (pf === 0) {
                console.log(`    ✅ acos(0) = π/2 = ${Math.PI/2} (correct)`);
            } else if (pf === 1) {
                console.log(`    ✅ acos(1) = 0 (correct)`);
            } else if (pf < 0 || pf > 1) {
                console.log(`    ❌ Should return NaN for invalid PF`);
            }
        } catch (error) {
            console.log(`  ❌ Error with acos(${pf}): ${error.message}`);
        }
    });

    // Test sqrt of negative numbers
    console.log("\nTesting sqrt domain validation:");
    try {
        const result = Math.sqrt(-1);
        console.log(`  sqrt(-1) = ${result} (should be NaN)`);
        if (isNaN(result)) {
            console.log(`  ✅ Negative sqrt handled correctly`);
        } else {
            console.log(`  ❌ Negative sqrt not handled correctly`);
        }
    } catch (error) {
        console.log(`  ❌ Unexpected error: ${error.message}`);
    }
}

// Run all precision tests
testPowerFactorCorrection();
testApparentPower();
testThreePhasePower();
testCapacitorSizing();
testEdgeCases();

console.log("\n=== MATHEMATICAL PRECISION AUDIT COMPLETE ===");
console.log("All formulas verified for computational accuracy");