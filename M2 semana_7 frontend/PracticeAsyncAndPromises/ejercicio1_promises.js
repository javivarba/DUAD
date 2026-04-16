// ejercicio1_promises_fetch.js

function getPokemon(id) {
    return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
}

const pokemon1 = getPokemon(1);
const pokemon2 = getPokemon(25);
const pokemon3 = getPokemon(150);

Promise.all([pokemon1, pokemon2, pokemon3])
    .then(results => {
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🎮 POKÉMON ENCONTRADOS');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        
        results.forEach((pokemon, index) => {
            console.log(`${index + 1}. ${pokemon.name.toUpperCase()} (ID: ${pokemon.id})`);
            console.log(`   Tipo: ${pokemon.types.map(t => t.type.name).join(', ')}`);
            console.log(`   Altura: ${pokemon.height / 10}m`);
            console.log(`   Peso: ${pokemon.weight / 10}kg\n`);
        });
        
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    })
    .catch(error => {
        console.error('❌ Error:', error.message);
    });

console.log('⏳ Buscando pokémon en paralelo...\n');