// ejercicio1_async_await.js

const axios = require('axios');

// ============================================
// EJERCICIO 1: ASYNC/AWAIT CON API
// ============================================

/**
 * Función asíncrona para obtener datos de un usuario
 * @param {number} userId - ID del usuario a buscar
 * @returns {Promise<Object>} - Datos del usuario
 */
async function getUserData(userId) {
    console.log(`🚀 Iniciando solicitud para usuario ${userId}...\n`);
    
    try {
        // ============================================
        // AWAIT: Espera a que la Promise se resuelva
        // ============================================
        // axios.get() retorna una Promise
        // await pausa la ejecución hasta que la Promise se resuelva
        
        const response = await axios.get(
            `https://jsonplaceholder.typicode.com/users/${userId}`
        );
        
        console.log('✅ Respuesta recibida del servidor');
        console.log(`📊 Status: ${response.status} ${response.statusText}`);
        console.log('✅ Datos parseados correctamente\n');
        
        // Retornar los datos del usuario
        return response.data;
        
    } catch (error) {
        // ============================================
        // MANEJO DE ERRORES CON TRY/CATCH
        // ============================================
        
        if (error.response) {
            // El servidor respondió con un código de error
            console.error(`❌ Error ${error.response.status}:`, error.response.statusText);
        } else if (error.request) {
            // La solicitud se hizo pero no hubo respuesta
            console.error('❌ No se recibió respuesta del servidor');
            console.error('   Verifica tu conexión a internet');
        } else {
            // Error al configurar la solicitud
            console.error('❌ Error:', error.message);
        }
        
        // Re-lanzar el error para que el llamador lo maneje
        throw error;
    }
}

// ============================================
// FUNCIÓN PARA MOSTRAR LOS DATOS DEL USUARIO
// ============================================
function displayUserData(userData) {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('👤 DATOS DEL USUARIO');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`ID:           ${userData.id}`);
    console.log(`Nombre:       ${userData.name}`);
    console.log(`Username:     ${userData.username}`);
    console.log(`Email:        ${userData.email}`);
    console.log(`Teléfono:     ${userData.phone}`);
    console.log(`Website:      ${userData.website}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    console.log(`\n📍 Dirección:`);
    console.log(`   Calle:     ${userData.address.street}`);
    console.log(`   Suite:     ${userData.address.suite}`);
    console.log(`   Ciudad:    ${userData.address.city}`);
    console.log(`   Zipcode:   ${userData.address.zipcode}`);
    console.log(`   Geo:       lat ${userData.address.geo.lat}, lng ${userData.address.geo.lng}`);
    
    console.log(`\n🏢 Compañía:`);
    console.log(`   Nombre:    ${userData.company.name}`);
    console.log(`   Slogan:    ${userData.company.catchPhrase}`);
    console.log(`   BS:        ${userData.company.bs}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    console.log('📦 Objeto completo (JSON):');
    console.log(JSON.stringify(userData, null, 2));
}

// ============================================
// FUNCIÓN PRINCIPAL - TAMBIÉN DEBE SER ASYNC
// ============================================
async function main() {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📋 EJERCICIO 1: ASYNC/AWAIT CON API');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    try {
        // ============================================
        // AWAIT: Espera a que getUserData termine
        // ============================================
        // El código se detiene aquí hasta que la función termine
        // Es como si fuera código sincrónico
        
        const userData = await getUserData(2);
        
        // Esta línea NO se ejecuta hasta que getUserData termine
        displayUserData(userData);
        
        console.log('\n✅ Programa finalizado exitosamente');
        
    } catch (error) {
        console.error('\n💥 Error en la ejecución del programa');
        console.error('💡 Verifica tu conexión a internet\n');
    }
}

// ============================================
// EJECUTAR EL PROGRAMA
// ============================================
main();

// ============================================
// 📚 CONCEPTOS CLAVE DE ASYNC/AWAIT
// ============================================
/*
1. ASYNC:
   - Palabra clave que convierte una función en asíncrona
   - Toda función async retorna automáticamente una Promise
   - Permite usar await dentro de ella
   
   Ejemplo:
   async function getUserData() {
       return "data";  // Retorna una Promise
   }

2. AWAIT:
   - Solo funciona dentro de funciones async
   - Pausa la ejecución hasta que la Promise se resuelva
   - Hace que el código asíncrono se vea sincrónico
   - Retorna el valor resuelto de la Promise
   
   Ejemplo:
   const data = await axios.get(url);  // Espera aquí
   console.log(data);  // Se ejecuta después

3. TRY/CATCH:
   - Maneja errores de forma limpia
   - Si una Promise es rechazada, el catch atrapa el error
   - Más legible que .catch() de Promises
   
   Ejemplo:
   try {
       const data = await getData();
   } catch (error) {
       console.error(error);
   }

4. FLUJO DE EJECUCIÓN:
   
   main() inicia
      ↓
   await getUserData(2) → Se PAUSA aquí ⏸️
      ↓
   axios.get() hace la solicitud HTTP
      ↓
   Espera la respuesta del servidor... ⏳
      ↓
   Respuesta recibida ✅
      ↓
   getUserData() retorna los datos
      ↓
   main() CONTINÚA con displayUserData()
      ↓
   Programa termina

5. VENTAJAS VS CALLBACKS:
   
   Callbacks (Ejercicio 2 de callbacks):
   fs.readFile('file1', (err1, data1) => {
       if (err1) return console.error(err1);
       fs.readFile('file2', (err2, data2) => {
           if (err2) return console.error(err2);
           // Callback hell 😱
       });
   });
   
   Async/Await:
   try {
       const data1 = await readFile('file1');
       const data2 = await readFile('file2');
       // Código limpio y legible ✨
   } catch (error) {
       console.error(error);
   }

6. COMPARACIÓN CON PYTHON:
   
   Python:
   async def get_user_data(user_id):
       response = await fetch(url)
       return response.json()
   
   JavaScript:
   async function getUserData(userId) {
       const response = await axios.get(url);
       return response.data;
   }
   
   ¡Es casi idéntico! 🎯
*/