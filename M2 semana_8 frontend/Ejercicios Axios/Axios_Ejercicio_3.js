// ==========================================
// AXIOS EJERCICIO 3: GET por ID con manejo de 404
// ==========================================

async function obtenerUsuarioPorId(id) {
    try {
        console.log(`=== OBTENIENDO USUARIO CON AXIOS ===`);
        console.log("ID:", id);
        
        // GET con Axios - sintaxis simple
        const response = await axios.get(`https://api.restful-api.dev/objects/${id}`);
        
        console.log("Response completo:", response);
        console.log("Status:", response.status);
        console.log("Usuario:", response.data);
        
        const usuario = response.data;
        
        console.log("✅ Usuario encontrado:");
        console.log(usuario);
        
        mostrarUsuarioObtenido(usuario);
        
        return usuario;
        
    } catch (error) {
        console.error("❌ Error:", error);
        
        // Axios maneja los errores HTTP de forma especial
        if (error.response) {
            // El servidor respondió con un código de error
            console.error("Status:", error.response.status);
            console.error("Data:", error.response.data);
            
            // Manejo específico del 404
            if (error.response.status === 404) {
                const mensajeError = `Usuario con ID "${id}" no encontrado`;
                console.error("❌ 404:", mensajeError);
                mostrarError(mensajeError, 404);
                return { error: true, mensaje: mensajeError, status: 404 };
            }
            
            // Otros errores HTTP
            mostrarError(`Error ${error.response.status}`, error.response.status);
            return { error: true, mensaje: `Error ${error.response.status}`, status: error.response.status };
            
        } else if (error.request) {
            // No hubo respuesta
            console.error("Request:", error.request);
            mostrarError("No se recibió respuesta del servidor");
            return { error: true, mensaje: "Sin respuesta" };
            
        } else {
            // Error al configurar
            console.error("Error message:", error.message);
            mostrarError(error.message);
            return { error: true, mensaje: error.message };
        }
    }
}

function mostrarUsuarioObtenido(usuario) {
    const resultDiv = document.getElementById('getResult');
    
    if (!resultDiv) {
        console.error("No se encontró #getResult");
        return;
    }
    
    // Formatear los datos adicionales
    let datosHTML = '';
    if (usuario.data && Object.keys(usuario.data).length > 0) {
        datosHTML = `
            <p><strong>Datos adicionales:</strong></p>
            <pre style="background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto;">${JSON.stringify(usuario.data, null, 2)}</pre>
        `;
    } else {
        datosHTML = '<p><em>Sin datos adicionales</em></p>';
    }
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #2196F3; padding: 15px; margin-top: 20px; background-color: #e3f2fd; border-radius: 5px;">
            <h3 style="color: #2196F3; margin-top: 0;">✅ Usuario encontrado con Axios</h3>
            <p><strong>ID:</strong> <code style="background: #ddd; padding: 5px; border-radius: 3px;">${usuario.id}</code></p>
            <p><strong>Nombre:</strong> ${usuario.name}</p>
            ${datosHTML}
            ${usuario.createdAt ? `<p><strong>Creado:</strong> ${new Date(usuario.createdAt).toLocaleString()}</p>` : ''}
            ${usuario.updatedAt ? `<p><strong>Actualizado:</strong> ${new Date(usuario.updatedAt).toLocaleString()}</p>` : ''}
        </div>
    `;
}

function mostrarError(mensaje, status = null) {
    const resultDiv = document.getElementById('getResult');
    
    if (!resultDiv) {
        console.error("No se encontró #getResult");
        return;
    }
    
    const statusBadge = status === 404 ? 
        '<span style="background: #f44336; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px;">404 NOT FOUND</span>' :
        '';
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <h3 style="color: #f44336; margin-top: 0;">❌ Error ${statusBadge}</h3>
            <p style="margin: 0;">${mensaje}</p>
        </div>
    `;
}

// Event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("===========================================");
    console.log("Axios Ejercicio 3 cargado - GET por ID");
    console.log("===========================================");
    
    const getUserForm = document.getElementById('getUserForm');
    
    if (!getUserForm) {
        console.error("❌ Formulario no encontrado");
        return;
    }
    
    console.log("✅ Formulario encontrado");
    
    getUserForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console.log("\n🔍 === BÚSQUEDA DE USUARIO ===");
        
        const id = document.getElementById('userId').value.trim();
        
        if (!id) {
            console.error("❌ ID vacío");
            mostrarError("El ID es obligatorio");
            return;
        }
        
        console.log("ID a buscar:", id);
        obtenerUsuarioPorId(id);
    });
    
    console.log("✅ Event listener configurado");
});