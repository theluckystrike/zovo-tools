// Debug capacitor calculation issue

function debugCapacitorCalculation(reactiveVAR, frequency, voltage) {
    console.log("=== CAPACITOR CALCULATION DEBUG ===");
    console.log(`Input: Q=${reactiveVAR}VAR, f=${frequency}Hz, V=${voltage}V`);

    const omega = 2 * Math.PI * frequency;
    console.log(`ω = 2πf = ${omega.toFixed(6)} rad/s`);

    const voltage_squared = Math.pow(voltage, 2);
    console.log(`V² = ${voltage_squared}`);

    const denominator = omega * voltage_squared;
    console.log(`Denominator = ω × V² = ${denominator.toExponential(6)}`);

    const capacitance = reactiveVAR / denominator;
    console.log(`Capacitance = Q / (ω × V²) = ${capacitance.toExponential(6)} F`);
    console.log(`Capacitance = ${(capacitance * 1e6).toFixed(2)} µF`);

    // Check for NaN or Infinity
    console.log(`isFinite(capacitance): ${isFinite(capacitance)}`);
    console.log(`isNaN(capacitance): ${isNaN(capacitance)}`);

    return capacitance;
}

// Test the problematic calculation
debugCapacitorCalculation(50000, 60, 480);