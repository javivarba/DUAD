// callback_exercise.js
const fs = require('fs');

// ============================================
// PASO 1: Crear los archivos de texto
// ============================================
console.log('📝 Creando archivos...\n');

const file1Content = `One
Red
I
Test
Blue
Three
Like
Dog
Sea
Green
Luigi
Drawing
Books
Pizza`;

const file2Content = `Hello
Tea
Light
I
Game
Pillow
Otter
Like
Yellow
Paper
Music
Pizza
Sun
Night`;

// Crear los archivos de forma síncrona
fs.writeFileSync('archivo1.txt', file1Content);
fs.writeFileSync('archivo2.txt', file2Content);
console.log('✅ Archivos creados: archivo1.txt y archivo2.txt\n');

// ============================================
// PASO 2: Leer archivos con CALLBACKS
// ============================================
console.log('Leyendo archivos con callbacks...\n');

// Leer el primer archivo
fs.readFile('archivo1.txt', 'utf8', (err1, data1) => {
    if (err1) {
        console.error('Error leyendo archivo 1:', err1);
        return;
    }
    
    console.log('✅ Archivo 1 leído correctamente');
    const words1 = data1.split('\n').map(word => word.trim());
    console.log('Palabras en archivo 1:', words1.length);
    
    // Leer el segundo archivo (CALLBACK ANIDADO - esto es Callback Hell)
    fs.readFile('archivo2.txt', 'utf8', (err2, data2) => {
        if (err2) {
            console.error('❌ Error leyendo archivo 2:', err2);
            return;
        }
        
        console.log('✅ Archivo 2 leído correctamente');
        const words2 = data2.split('\n').map(word => word.trim());
        console.log('Palabras en archivo 2:', words2.length);
        
        // ============================================
        // PASO 3: Comparar y encontrar palabras repetidas
        // ============================================
        console.log('\n🔍 Comparando archivos...\n');
        
        // Usar Set para búsqueda eficiente
        const set1 = new Set(words1);
        const repeated = words2.filter(word => set1.has(word));
        
        // ============================================
        // PASO 4: Mostrar resultados
        // ============================================
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📋 PALABRAS REPETIDAS:');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        repeated.forEach(word => console.log(`  • ${word}`));
        
        console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🔐 MENSAJE ESCONDIDO:');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`  ➜ ${repeated.join(' ')} 🍕`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    });
});

console.log('⏳ Esperando a que terminen de leer los archivos...');
console.log('💡 Nota: Este es un ejemplo de CALLBACK HELL (callbacks anidados)\n');