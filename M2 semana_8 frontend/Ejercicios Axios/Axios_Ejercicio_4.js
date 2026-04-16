// ==========================================
// AXIOS EJERCICIO 4: PUT - Actualizar dirección
// ==========================================

async function actualizarDireccion(id, nuevaDireccion) {
    try {
        console.log("=== ACTUALIZANDO DIRECCIÓN CON AXIOS ===");
        console.log("ID:", id);
        console.log("Nueva dirección:", nuevaDireccion);
        
        // Paso 1: Obtener el usuario actual
        console.log("\nPaso 1: Obteniendo usuario actual...");
        const responseGet = await axios.get(`https://api.restful-api.dev/objects/${id}`);
        
        console.log("GET Status:", responseGet.status);
        console.log("Usuario actual:", responseGet.data);
        
        const usuarioActual = responseGet.data;
        
        // Paso 2: Preparar datos actualizados
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
        
        // Paso 3: Enviar PUT con Axios
        console.log("\nPaso 3: Enviando PUT...");
        
        // Con Axios: axios.put(url, data, config)
        const responsePut = await axios.put(
            `https://api.restful-api.dev/objects/${id}`,
            datosActualizados
        );
        
        console.log("PUT Status:", responsePut.status);
        console.log("Usuario actualizado:", responsePut.data);
        
        const usuarioActualizado = responsePut.data;
        
        console.log("\n✅ ÉXITO - Dirección actualizada");
        
        mostrarUsuarioActualizado(usuarioActual, usuarioActualizado);
        
        return usuarioActualizado;
        
    } catch (error) {
        console.error("❌ Error:", error);
        
        // Manejo de errores con Axios
        if (error.response) {
            console.error("Status:", error.response.status);
            console.error("Data:", error.response.data);
            
            // Manejo específico de 404
            if (error.response.status === 404) {
                mostrarError(`Usuario con ID "${id}" no encontrado`, 404);
                return { error: true, mensaje: "Usuario no encontrado", status: 404 };
            }
            
            // Otros errores HTTP
            mostrarError(`Error ${error.response.status}: ${JSON.stringify(error.response.data)}`, error.response.status);
            return { error: true, mensaje: error.response.data, status: error.response.status };
            
        } else if (error.request) {
            console.error("Request:", error.request);
            mostrarError("No se recibió respuesta. Problema de CORS o red.");
            return { error: true, mensaje: "Sin respuesta" };
            
        } else {
            console.error("Error message:", error.message);
            mostrarError(error.message);
            return { error: true, mensaje: error.message };
        }
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
            <h3 style="color: #FF9800; margin-top: 0;">✅ Dirección actualizada con Axios</h3>
            
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

function mostrarError(mensaje, status = null) {
    const resultDiv = document.getElementById('updateResult');
    
    if (!resultDiv) return;
    
    const statusBadge = status ? 
        `<span style="background: #f44336; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px;">ERROR ${status}</span>` :
        '';
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <h3 style="color: #f44336; margin-top: 0;">❌ Error ${statusBadge}</h3>
            <p>${mensaje}</p>
            <hr style="border: 1px solid #f44336; margin: 15px 0;">
            <p style="font-size: 14px;">
                <strong>Solución:</strong> Prueba en <strong>Postman</strong><br>
                <strong>URL:</strong> https://api.restful-api.dev/objects/ff8081819c5368bb019c8d591fee5a4f<br>
                <strong>Method:</strong> PUT<br>
                <strong>Body:</strong> Objeto completo con dirección actualizada
            </p>
        </div>
    `;
}

// Event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("===========================================");
    console.log("Axios Ejercicio 4 cargado - PUT dirección");
    console.log("===========================================");
    
    const updateForm = document.getElementById('updateForm');
    
    if (!updateForm) {
        console.error("❌ Formulario no encontrado");
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
        
        actualizarDireccion(id, nuevaDireccion);
    });
    
    console.log("✅ Event listener configurado");
});