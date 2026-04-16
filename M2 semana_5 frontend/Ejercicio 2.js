// EJERCICIO 2: Filtrar números pares de una lista

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 23, 28, 30];

console.log("Lista original:", numbers);
console.log("\n");

// SOLUCIÓN 1: Usando FOR tradicional

console.log("SOLUCIÓN 1: Usando FOR tradicional");

const evenNumbersWithFor = [];

for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        evenNumbersWithFor.push(numbers[i]);
    }
}

console.log("Números pares (con for):", evenNumbersWithFor);
console.log("\n");

// SOLUCIÓN 2: Usando método FILTER

console.log("SOLUCIÓN 2: Usando método FILTER");

const evenNumbersWithFilter = numbers.filter((number) => {
    return number % 2 === 0;
});

console.log("Números pares (con filter):", evenNumbersWithFilter);
console.log("\n");