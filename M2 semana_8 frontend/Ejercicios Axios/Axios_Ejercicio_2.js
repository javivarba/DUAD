// ==========================================
// AXIOS EJERCICIO 2: POST - Crear usuario
// ==========================================

async function crearUsuario(nombre, correo, password, direccion) {
    try {
        console.log("=== CREANDO USUARIO CON AXIOS ===");
        console.log("Datos a enviar:", { nombre, correo, password, direccion });
        
        // Preparar el objeto
        const nuevoUsuario = {
            name: nombre,
            data: {
                correo: correo,
                password: password,
                direccion: direccion
            }
        };
        
        console.log("Objeto completo:", nuevoUsuario);
        
        // Con Axios, el POST es más simple:
        // axios.post(url, data, config)
        const response = await axios.post('https://api.restful-api.dev/objects', nuevoUsuario);
        
        // Nota: Axios automáticamente:
        // - Agrega Content-Type: application/json
        // - Convierte el objeto a JSON string
        // - Parsea la respuesta JSON a objeto
        
        console.log("Response completo:", response);
        console.log("Status:", response.status);
        console.log("Usuario creado:", response.data);
        
        const usuarioCreado = response.data;
        
        console.log("✅ Usuario creado exitosamente");
        console.log("🔑 ID:", usuarioCreado.id);
        console.log("⚠️ Guarda este ID:", usuarioCreado.id);
        
        // Guardar en localStorage
        guardarIDUsuario(usuarioCreado.id, nombre);
        
        // Mostrar en pantalla
        mostrarUsuarioCreado(usuarioCreado);
        
        return usuarioCreado;
        
    } catch (error) {
        console.error("❌ Error:", error);
        
        // Manejo de errores detallado con Axios
        if (error.response) {
            // El servidor respondió con error
            console.error("Status:", error.response.status);
            console.error("Data:", error.response.data);
            console.error("Headers:", error.response.headers);
            mostrarError(`Error ${error.response.status}: ${JSON.stringify(error.response.data)}`);
        } else if (error.request) {
            // La solicitud se hizo pero no hubo respuesta (CORS, network, etc)
            console.error("Request:", error.request);
            mostrarError("No se recibió respuesta. Problema de CORS o red.");
        } else {
            // Error al configurar la solicitud
            console.error("Error message:", error.message);
            mostrarError(error.message);
        }
        
        throw error;
    }
}

function guardarIDUsuario(id, nombre) {
    try {
        let usuarios = JSON.parse(localStorage.getItem('usuarios_axios')) || [];
        
        usuarios.push({
            id: id,
            nombre: nombre,
            fecha: new Date().toISOString()
        });
        
        localStorage.setItem('usuarios_axios', JSON.stringify(usuarios));
        console.log("💾 ID guardado en localStorage");
        console.log("Total usuarios:", usuarios.length);
        
    } catch (error) {
        console.error("Error en localStorage:", error);
    }
}

function mostrarUsuarioCreado(usuario) {
    const resultDiv = document.getElementById('userResult');
    
    if (!resultDiv) {
        console.error("No se encontró #userResult");
        return;
    }
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #4CAF50; padding: 15px; margin-top: 20px; background-color: #e8f5e9; border-radius: 5px;">
            <h3 style="color: #4CAF50; margin-top: 0;">✅ Usuario creado con Axios</h3>
            <p><strong>ID:</strong> <code style="background: #ddd; padding: 5px; border-radius: 3px;">${usuario.id}</code></p>
            <p><strong>Nombre:</strong> ${usuario.name}</p>
            <p><strong>Correo:</strong> ${usuario.data.correo}</p>
            <p><strong>Dirección:</strong> ${usuario.data.direccion}</p>
            ${usuario.createdAt ? `<p><strong>Creado:</strong> ${new Date(usuario.createdAt).toLocaleString()}</p>` : ''}
            <p style="background: #fff3cd; padding: 10px; border-radius: 4px; margin-top: 10px;">
                <strong>⚠️ Guarda este ID para el ejercicio 4:</strong><br>
                <code>${usuario.id}</code>
            </p>
        </div>
    `;
}

function mostrarError(mensaje) {
    const resultDiv = document.getElementById('userResult');
    
    if (!resultDiv) return;
    
    resultDiv.innerHTML = `
        <div style="border: 2px solid #f44336; padding: 15px; margin-top: 20px; background-color: #ffebee; border-radius: 5px;">
            <h3 style="color: #f44336; margin-top: 0;">❌ Error</h3>
            <p>${mensaje}</p>
            <hr style="border: 1px solid #f44336; margin: 15px 0;">
            <p style="font-size: 14px;">
                <strong>Solución:</strong> Prueba en Postman con estos datos:<br>
                <strong>URL:</strong> https://api.restful-api.dev/objects<br>
                <strong>Method:</strong> POST<br>
                <strong>Body (JSON):</strong> Usa los datos del formulario
            </p>
        </div>
    `;
}

// Ver usuarios guardados en localStorage
function verUsuariosGuardados() {
    const usuarios = JSON.parse(localStorage.getItem('usuarios_axios')) || [];
    console.log("=== USUARIOS GUARDADOS (AXIOS) ===");
    console.table(usuarios);
    return usuarios;
}

// Event listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("===========================================");
    console.log("Axios Ejercicio 2 cargado - POST");
    console.log("===========================================");
    
    const userForm = document.getElementById('userForm');
    
    if (!userForm) {
        console.error("❌ Formulario no encontrado");
        return;
    }
    
    console.log("✅ Formulario encontrado");
    
    userForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console.log("\n📝 === NUEVO USUARIO ===");
        
        const nombre = document.getElementById('nombre').value.trim();
        const correo = document.getElementById('correo').value.trim();
        const password = document.getElementById('password').value;
        const direccion = document.getElementById('direccion').value.trim();
        
        if (!nombre || !correo || !password || !direccion) {
            console.error("❌ Campos incompletos");
            mostrarError("Todos los campos son obligatorios");
            return;
        }
        
        crearUsuario(nombre, correo, password, direccion);
        
        this.reset();
    });
    
    console.log("✅ Event listener configurado");
});