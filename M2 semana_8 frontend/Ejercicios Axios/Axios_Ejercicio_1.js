// ==========================================
// AXIOS EJERCICIO 1: GET y filtrar datos
// ==========================================

async function listarObjetosConData() {
    try {
        console.log("=== OBTENIENDO OBJETOS CON AXIOS ===");
        
        // Axios hace el GET 
        const response = await axios.get('https://api.restful-api.dev/objects');
        
        console.log("Response completo:", response);
        console.log("Status:", response.status);
        console.log("Datos:", response.data);
        
        // En Axios, los datos están en response.data (no necesitas .json())
        const todosLosObjetos = response.data;
        
        console.log(`Total de objetos: ${todosLosObjetos.length}`);
        
        // Filtrar: solo los que tienen la propiedad "data"
        const objetosConData = todosLosObjetos.filter(objeto => objeto.data !== null && objeto.data !== undefined);
        
        console.log(`Objetos con data: ${objetosConData.length}`);
        console.log("Objetos filtrados:", objetosConData);
        
        // Formatear cada objeto
        const objetosFormateados = objetosConData.map(objeto => formatearObjeto(objeto));
        
        // Mostrar en pantalla
        mostrarEnPantalla(objetosFormateados);
        
        return objetosConData;
        
    } catch (error) {
        console.error("❌ Error:", error);
        
        // Axios proporciona información detallada del error
        if (error.response) {
            // El servidor respondió con un código de error
            console.error("Error response:", error.response.status);
            console.error("Error data:", error.response.data);
            mostrarError(`Error del servidor: ${error.response.status}`);
        } else if (error.request) {
            // La solicitud se hizo pero no hubo respuesta
            console.error("No response:", error.request);
            mostrarError("No se recibió respuesta del servidor");
        } else {
            // Algo pasó al configurar la solicitud
            console.error("Error message:", error.message);
            mostrarError(`Error: ${error.message}`);
        }
    }
}

function formatearObjeto(objeto) {
    const nombre = objeto.name;
    const data = objeto.data;
    
    // Convertir el objeto data en un string legible
    const propiedades = Object.entries(data)
        .map(([key, value]) => `${key}: ${value}`)
        .join(', ');
    
    return `${nombre} (${propiedades})`;
}

function mostrarEnPantalla(objetosFormateados) {
    const resultsDiv = document.getElementById('results');
    
    if (!resultsDiv) {
        console.error("No se encontró #results");
        return;
    }
    
    // Crear una lista HTML
    const lista = objetosFormateados
        .map(texto => `<li>${texto}</li>`)
        .join('');
    
    resultsDiv.innerHTML = `
        <div style="margin-top: 20px;">
            <h3 style="color: #4CAF50;">✅ Objetos con datos (${objetosFormateados.length} encontrados):</h3>
            <ul>${lista}</ul>
        </div>
    `;
    
    // También mostrar en consola
    console.log("=== OBJETOS FORMATEADOS ===");
    objetosFormateados.forEach(texto => console.log(texto));
}

function mostrarError(mensaje) {
    const resultsDiv = document.getElementById('results');
    
    if (!resultsDiv) return;
    
    resultsDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <p style="color: #f44336; margin: 0;"><strong>❌ ${mensaje}</strong></p>
        </div>
    `;
}

// Log inicial
console.log("===========================================");
console.log("Axios Ejercicio 1 cargado");
console.log("===========================================");