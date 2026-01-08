// ejercicio5_promises_user_error.js

function getUserData(userId) {
    return fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('📋 EJERCICIO 2: MANEJO DE ERRORES');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('🔍 Buscando usuario con ID 999...\n');

getUserData(9)
    .then(userData => {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('👤 DATOS DEL USUARIO');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`ID:           ${userData.id}`);
        console.log(`Nombre:       ${userData.name}`);
        console.log(`Email:        ${userData.email}`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    })
    .catch(error => {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('❌ ERROR EN LA BÚSQUEDA');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('💔 El usuario no fue encontrado');
        console.log(`📝 Detalles: ${error.message}`);
        console.log('💡 Verifica que el ID sea válido (1-10)');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    })
    .finally(() => {
        console.log('✅ Operación completada\n');
    })