// ==========================================
// EJERCICIO 3: Obtener usuario por ID (GET)
// ==========================================

async function obtenerUsuarioPorId(id) {
    try {
        console.log(`=== OBTENIENDO USUARIO ID: ${id} ===`);
        
        // Realizar GET request
        const response = await fetch(`https://api.restful-api.dev/objects/${id}`);
        
        console.log("Status:", response.status);
        console.log("OK:", response.ok);
        
        // Manejo específico del error 404
        if (response.status === 404) {
            const mensajeError = `Usuario con ID "${id}" no encontrado`;
            console.error("❌", mensajeError);
            mostrarError(mensajeError);
            return { error: true, mensaje: mensajeError, status: 404 };
        }
        
        // Manejo de otros errores HTTP
        if (!response.ok) {
            const mensajeError = `Error HTTP: ${response.status}`;
            console.error("❌", mensajeError);
            mostrarError(mensajeError);
            return { error: true, mensaje: mensajeError, status: response.status };
        }
        
        // Si todo OK, obtener los datos
        const usuario = await response.json();
        
        console.log("✅ Usuario encontrado:");
        console.log(usuario);
        
        mostrarUsuarioObtenido(usuario);
        
        return usuario;
        
    } catch (error) {
        // Manejo de errores de red o parsing
        console.error("❌ Error de conexión:", error.message);
        mostrarError("Error de conexión: " + error.message);
        return { error: true, mensaje: error.message };
    }
}

function mostrarUsuarioObtenido(usuario) {
    const resultDiv = document.getElementById('getResult');
    
    if (!resultDiv) {
        console.error("No se encontró el div #getResult");
        return;
    }
    
    // Construir HTML con los datos del usuario
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
            <h3 style="color: #2196F3; margin-top: 0;">✅ Usuario encontrado</h3>
            <p><strong>ID:</strong> <code style="background: #ddd; padding: 5px; border-radius: 3px;">${usuario.id}</code></p>
            <p><strong>Nombre:</strong> ${usuario.name}</p>
            ${datosHTML}
            ${usuario.createdAt ? `<p><strong>Creado:</strong> ${usuario.createdAt}</p>` : ''}
            ${usuario.updatedAt ? `<p><strong>Actualizado:</strong> ${usuario.updatedAt}</p>` : ''}
        </div>
    `;
}

function mostrarError(mensaje) {
    const resultDiv = document.getElementById('getResult');
    
    if (!resultDiv) {
        console.error("No se encontró el div #getResult");
        return;
    }
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <p style="color: #f44336; margin: 0;"><strong>❌ ${mensaje}</strong></p>
        </div>
    `;
}

// Event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("===========================================");
    console.log("Script Ejercicio 3 cargado - GET por ID");
    console.log("===========================================");
    
    const getUserForm = document.getElementById('getUserForm');
    
    if (!getUserForm) {
        console.error("❌ Formulario 'getUserForm' no encontrado");
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
