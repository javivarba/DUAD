
// EJERCICIO 4: Convertir String a Array de Palabras (SIN SPLIT)

const sentence = "Javascript es el lenguaje del futuro";

console.log("String original:", sentence);
console.log("\n");

console.log("=== SOLUCIÓN MANUAL (sin split) ===");

function stringToWords(text) {
    const words = [];      // Array para almacenar las palabras
    let currentWord = "";  // Palabra que estamos construyendo
    
    // Recorremos cada carácter del string
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        
        // Si encontramos un espacio
        if (char === " ") {
            // Y si tenemos una palabra construida, la agregamos al array
            if (currentWord !== "") {
                words.push(currentWord);
                currentWord = ""; // Reiniciamos la palabra actual
            }
        } else {
            // Si no es espacio, agregamos el carácter a la palabra actual
            currentWord += char;
        }
    }
    
    // No olvidar agregar la última palabra (si existe)
    if (currentWord !== "") {
        words.push(currentWord);
    }
    
    return words;
}

const wordsArray = stringToWords(sentence);
console.log("Array de palabras:", wordsArray);
console.log("Número de palabras:", wordsArray.length);
console.log("\n");