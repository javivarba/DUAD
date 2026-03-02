// ==========================================
// EJERCICIO 2: Crear usuario con POST (FETCH)
// ==========================================

async function crearUsuario(nombre, correo, password, direccion) {
    try {
        console.log("=== CREANDO USUARIO ===");
        console.log("Datos a enviar:", { nombre, correo, password, direccion });
        
        const nuevoUsuario = {
            name: nombre,
            data: {
                correo: correo,
                password: password,
                direccion: direccion
            }
        };
        
        console.log("Objeto a enviar:", JSON.stringify(nuevoUsuario, null, 2));
        
        // FETCH con POST
        const response = await fetch('https://api.restful-api.dev/objects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nuevoUsuario)
        });
        
        console.log("Status:", response.status);
        console.log("OK:", response.ok);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error("Error response:", errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const usuarioCreado = await response.json();
        
        console.log("✅ ÉXITO - Usuario creado");
        console.log("Respuesta:", usuarioCreado);
        console.log("🔑 ID:", usuarioCreado.id);
        
        guardarIDUsuario(usuarioCreado.id, nombre);
        mostrarUsuarioCreado(usuarioCreado);
        
        return usuarioCreado;
        
    } catch (error) {
        console.error("❌ Error:", error.message);
        mostrarError(error.message);
        throw error;
    }
}

function guardarIDUsuario(id, nombre) {
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    usuarios.push({ id, nombre, fecha: new Date().toISOString() });
    localStorage.setItem('usuarios', JSON.stringify(usuarios));
    console.log("💾 Guardado en localStorage");
}

function mostrarUsuarioCreado(usuario) {
    const div = document.getElementById('userResult');
    div.innerHTML = `
        <div style="border: 2px solid green; padding: 15px; margin-top: 10px; background: #e8f5e9; border-radius: 5px;">
            <h3 style="color: green; margin: 0 0 10px 0;">✅ Usuario creado</h3>
            <p><strong>ID:</strong> <code>${usuario.id}</code></p>
            <p><strong>Nombre:</strong> ${usuario.name}</p>
            <p><strong>Correo:</strong> ${usuario.data.correo}</p>
            <p><strong>Dirección:</strong> ${usuario.data.direccion}</p>
            <p><strong>Creado:</strong> ${usuario.createdAt}</p>
        </div>
    `;
}

function mostrarError(mensaje) {
    const div = document.getElementById('userResult');
    div.innerHTML = `
        <div style="border: 2px solid red; padding: 15px; margin-top: 10px; background: #ffebee; border-radius: 5px;">
            <p style="color: red; margin: 0;"><strong>❌ ${mensaje}</strong></p>
        </div>
    `;
}

// Event Listener
document.addEventListener('DOMContentLoaded', function() {
    console.log("Script cargado - Ejercicio fetch POST");
    
    const form = document.getElementById('userForm');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nombre = document.getElementById('nombre').value.trim();
        const correo = document.getElementById('correo').value.trim();
        const password = document.getElementById('password').value;
        const direccion = document.getElementById('direccion').value.trim();
        
        if (!nombre || !correo || !password || !direccion) {
            mostrarError("Todos los campos son obligatorios");
            return;
        }
        
        crearUsuario(nombre, correo, password, direccion);
        this.reset();
    });
});