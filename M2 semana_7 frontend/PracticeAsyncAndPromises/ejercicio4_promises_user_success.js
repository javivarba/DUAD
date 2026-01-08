// ejercicio4_promises_user_success.js

function getUserData(userId) {
    return fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            console.log(`✅ Respuesta recibida: ${response.status}`);
            return response.json();
        });
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('📋 EJERCICIO 1: BÚSQUEDA EXITOSA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('🔍 Buscando usuario con ID 2...\n');

getUserData(2)
    .then(userData => {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('👤 DATOS DEL USUARIO');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`ID:           ${userData.id}`);
        console.log(`Nombre:       ${userData.name}`);
        console.log(`Username:     ${userData.username}`);
        console.log(`Email:        ${userData.email}`);
        console.log(`Teléfono:     ${userData.phone}`);
        console.log(`Website:      ${userData.website}`);
        console.log(`Ciudad:       ${userData.address.city}`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    })
    .catch(error => {
        console.error('❌ Error al obtener usuario:', error.message);
    })
    .finally(() => {
        console.log('✅ Operación completada\n');
    });