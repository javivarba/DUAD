// ejercicio2_error_handling_jsonplaceholder.js

const axios = require('axios');

// ============================================
// EJERCICIO 2: MANEJO DE ERRORES
// ============================================

async function getUserData(userId) {
    console.log(`🚀 Intentando obtener usuario con ID: ${userId}...\n`);
    
    try {
        const response = await axios.get(
            `https://jsonplaceholder.typicode.com/users/${userId}`
        );
        
        console.log('✅ Usuario encontrado!');
        console.log(`📊 Status: ${response.status}\n`);
        
        return response.data;
        
    } catch (error) {
        // ============================================
        // MANEJO DETALLADO DE ERRORES
        // ============================================
        
        if (error.response) {
            // El servidor RESPONDIÓ con un código de error
            const statusCode = error.response.status;
            
            console.error(`❌ Error HTTP: ${statusCode}`);
            
            switch (statusCode) {
                case 404:
                    console.error(`💔 Usuario con ID ${userId} no fue encontrado`);
                    console.error('   El usuario no existe en la base de datos\n');
                    break;
                    
                case 500:
                    console.error('💥 Error del servidor');
                    console.error('   Hay un problema en el servidor de la API\n');
                    break;
                    
                default:
                    console.error(`⚠️  Error: ${error.response.statusText}\n`);
            }
            
            return {
                error: true,
                statusCode: statusCode,
                message: error.response.statusText
            };
            
        } else if (error.request) {
            // La solicitud se hizo pero no hubo respuesta
            console.error('❌ No se recibió respuesta del servidor');
            console.error('   Verifica tu conexión a internet\n');
            
            return {
                error: true,
                message: 'Sin respuesta del servidor'
            };
            
        } else {
            // Error al configurar la solicitud
            console.error('❌ Error al configurar la solicitud');
            console.error(`   ${error.message}\n`);
            
            return {
                error: true,
                message: error.message
            };
        }
    }
}

function displayResult(result) {
    if (result.error) {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('⚠️  RESULTADO: ERROR');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`Código: ${result.statusCode || 'N/A'}`);
        console.log(`Mensaje: ${result.message}`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    } else {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('✅ RESULTADO: ÉXITO');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`ID: ${result.id}`);
        console.log(`Nombre: ${result.name}`);
        console.log(`Email: ${result.email}`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    }
}

async function main() {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📋 EJERCICIO 2: MANEJO DE ERRORES');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    // Caso 1: Usuario que existe (ID 2)
    console.log('🧪 TEST 1: Usuario válido (ID 2)');
    console.log('─────────────────────────────────────');
    const result1 = await getUserData(2);
    displayResult(result1);
    
    // Caso 2: Usuario que NO existe (ID 999)
    console.log('🧪 TEST 2: Usuario inválido (ID 999)');
    console.log('─────────────────────────────────────');
    const result2 = await getUserData(999);
    displayResult(result2);
    
    console.log('✅ Programa finalizado');
}

main();