// Función asíncrona para obtener y mostrar objetos
async function listarObjetos() {
    try {
        // 1. Hacemos el request GET
        console.log("Haciendo request...");
        const response = await fetch('https://api.restful-api.dev/objects');
        
        // 2. Convertimos la respuesta a JSON (segunda promesa)
        const objetos = await response.json();
        console.log("Datos recibidos:", objetos);
        
        // 3. Filtramos: solo los que TIENEN la propiedad 'data'
        const objetosConData = objetos.filter(objeto => objeto.data);
        console.log("Objetos con data:", objetosConData);
        
        // 4. Formateamos cada objeto para mostrarlo legible
        const objetosFormateados = objetosConData.map(objeto => {
            return formatearObjeto(objeto);
        });
        
        // 5. Mostramos en pantalla
        mostrarEnPantalla(objetosFormateados);
        
    } catch (error) {
        console.error("Error al obtener datos:", error);
    }
}

// Función helper para formatear un objeto individual
function formatearObjeto(objeto) {
    const nombre = objeto.name;
    const data = objeto.data;
    
    // Construimos el string con las propiedades de data
    const propiedades = Object.entries(data)
        .map(([key, value]) => `${key}: ${value}`)
        .join(', ');
    
    return `${nombre} (${propiedades})`;
}

// Función para mostrar en el DOM
function mostrarEnPantalla(objetosFormateados) {
    const resultsDiv = document.getElementById('results');
    
    // Creamos una lista HTML
    const lista = objetosFormateados.map(texto => `<li>${texto}</li>`).join('');
    resultsDiv.innerHTML = `<ul>${lista}</ul>`;
    
    // También mostramos en consola
    console.log("=== OBJETOS FORMATEADOS ===");
    objetosFormateados.forEach(texto => console.log(texto));
}

// Ejecutamos la función cuando cargue la página
listarObjetos();