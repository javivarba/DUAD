// EJERCICIO 3: Convertir Celsius a Fahrenheit con MAP

// Lista de temperaturas en Celsius
const celsiusTemps = [0, 10, 20, 25, 30, 35, 40, 100];

console.log("Temperaturas en Celsius:", celsiusTemps);
console.log("\n");

console.log("=== CONVERSIÓN CON MAP ===");

// Fórmula: Fahrenheit = (Celsius × 9/5) + 32
const fahrenheitTemps = celsiusTemps.map((celsius) => {
    const fahrenheit = (celsius * 9/5) + 32;
    return fahrenheit;
});

console.log("Temperaturas en Fahrenheit:", fahrenheitTemps);
console.log("\n");