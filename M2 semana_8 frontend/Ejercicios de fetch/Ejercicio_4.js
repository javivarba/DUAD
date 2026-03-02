// ==========================================
// EJERCICIO 4: Actualizar dirección (PUT)
// ==========================================

async function actualizarDireccion(id, nuevaDireccion) {
    try {
        console.log("=== ACTUALIZANDO DIRECCIÓN ===");
        console.log("ID:", id);
        console.log("Nueva dirección:", nuevaDireccion);
        
        // Paso 1: Primero obtenemos el usuario actual para tener todos sus datos
        console.log("\nPaso 1: Obteniendo usuario actual...");
        const responseGet = await fetch(`https://api.restful-api.dev/objects/${id}`);
        
        console.log("GET Status:", responseGet.status);
        
        if (responseGet.status === 404) {
            const mensajeError = `Usuario con ID "${id}" no encontrado`;
            console.error("❌", mensajeError);
            mostrarError(mensajeError);
            return { error: true, mensaje: mensajeError };
        }
        
        if (!responseGet.ok) {
            throw new Error(`Error al obtener usuario: ${responseGet.status}`);
        }
        
        const usuarioActual = await responseGet.json();
        console.log("Usuario actual obtenido:");
        console.log(usuarioActual);
        
        // Paso 2: Actualizamos la dirección en los datos
        console.log("\nPaso 2: Preparando datos actualizados...");
        
        const datosActualizados = {
            name: usuarioActual.name,
            data: {
                ...usuarioActual.data,
                direccion: nuevaDireccion
            }
        };
        
        console.log("Datos a enviar:");
        console.log(JSON.stringify(datosActualizados, null, 2));
        
        // Paso 3: Enviamos PUT con los datos actualizados
        console.log("\nPaso 3: Enviando PUT request...");
        const responsePut = await fetch(`https://api.restful-api.dev/objects/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosActualizados)
        });
        
        console.log("PUT Status:", responsePut.status);
        console.log("PUT OK:", responsePut.ok);
        
        if (!responsePut.ok) {
            const errorText = await responsePut.text();
            console.error("Error response:", errorText);
            throw new Error(`HTTP error! status: ${responsePut.status}`);
        }
        
        const usuarioActualizado = await responsePut.json();
        
        console.log("\n✅ ÉXITO - Usuario actualizado:");
        console.log(usuarioActualizado);
        
        mostrarUsuarioActualizado(usuarioActual, usuarioActualizado);
        
        return usuarioActualizado;
        
    } catch (error) {
        console.error("❌ Error completo:", error);
        mostrarError("Error: " + error.message);
        return { error: true, mensaje: error.message };
    }
}

function mostrarUsuarioActualizado(usuarioAntes, usuarioDespues) {
    const resultDiv = document.getElementById('updateResult');
    
    if (!resultDiv) {
        console.error("No se encontró #updateResult");
        return;
    }
    
    const direccionAntes = usuarioAntes.data?.direccion || 'Sin dirección';
    const direccionDespues = usuarioDespues.data?.direccion || 'Sin dirección';
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #FF9800; padding: 15px; margin-top: 20px; background-color: #fff3e0; border-radius: 5px;">
            <h3 style="color: #FF9800; margin-top: 0;">✅ Dirección actualizada exitosamente</h3>
            
            <p><strong>ID:</strong> <code style="background: #ddd; padding: 5px; border-radius: 3px;">${usuarioDespues.id}</code></p>
            <p><strong>Nombre:</strong> ${usuarioDespues.name}</p>
            
            <hr style="border: 1px solid #ddd; margin: 15px 0;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div style="background: #ffebee; padding: 10px; border-radius: 4px;">
                    <strong>❌ Dirección anterior:</strong>
                    <p style="margin: 5px 0;">${direccionAntes}</p>
                </div>
                <div style="background: #e8f5e9; padding: 10px; border-radius: 4px;">
                    <strong>✅ Dirección nueva:</strong>
                    <p style="margin: 5px 0;">${direccionDespues}</p>
                </div>
            </div>
            
            ${usuarioDespues.data ? `
                <details style="margin-top: 15px;">
                    <summary style="cursor: pointer; font-weight: bold;">Ver todos los datos</summary>
                    <pre style="background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; margin-top: 10px;">${JSON.stringify(usuarioDespues.data, null, 2)}</pre>
                </details>
            ` : ''}
            
            ${usuarioDespues.updatedAt ? `<p style="margin-top: 10px;"><strong>Actualizado:</strong> ${new Date(usuarioDespues.updatedAt).toLocaleString()}</p>` : ''}
        </div>
    `;
}

function mostrarError(mensaje) {
    const resultDiv = document.getElementById('updateResult');
    
    if (!resultDiv) return;
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <h3 style="color: #f44336; margin-top: 0;">❌ Error</h3>
            <p style="margin: 0;">${mensaje}</p>
            <hr style="border: 1px solid #f44336; margin: 15px 0;">
            <p style="margin: 0; font-size: 14px;">
                <strong>Solución:</strong> Si es un error de CORS, prueba esta actualización en <strong>Postman</strong>.
            </p>
        </div>
    `;
}

// Event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("===========================================");
    console.log("Script Ejercicio 4 - PUT dirección");
    console.log("===========================================");
    
    const updateForm = document.getElementById('updateForm');
    
    if (!updateForm) {
        console.error("❌ Formulario 'updateForm' no encontrado");
        return;
    }
    
    console.log("✅ Formulario encontrado");
    
    updateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console.log("\n🔄 === ACTUALIZACIÓN DE DIRECCIÓN ===");
        
        const id = document.getElementById('updateUserId').value.trim();
        const nuevaDireccion = document.getElementById('newDireccion').value.trim();
        
        if (!id || !nuevaDireccion) {
            console.error("❌ Campos incompletos");
            mostrarError("Todos los campos son obligatorios");
            return;
        }
        
        console.log("Datos del formulario:");
        console.log("- ID:", id);
        console.log("- Nueva dirección:", nuevaDireccion);
        
        actualizarDireccion(id, nuevaDireccion);
    });
    
    console.log("✅ Event listener configurado");
});