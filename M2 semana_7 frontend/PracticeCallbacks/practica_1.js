// Función principal que recibe el número y los dos callbacks
function checkNumber(number, callbackEven, callbackOdd) {
    if (number % 2 === 0) {
        callbackEven();  // Ejecuta el callback de número par
    } else {
        callbackOdd();   // Ejecuta el callback de número impar
    }
}

// Definir los callbacks
const showEven = () => {
    console.log("The number is even!");
}

const showOdd = () => {
    console.log("The number is odd!");
}

// Usar la función
checkNumber(6, showEven, showOdd);  // "The number is even!"
checkNumber(7, showEven, showOdd);  // "The number is odd!"