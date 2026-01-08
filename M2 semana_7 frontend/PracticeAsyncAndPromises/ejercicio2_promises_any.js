

function getPokemon(id) {
    console.log(`🔍 Solicitando pokémon ID: ${id}`);
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

Promise.any([pokemon1, pokemon2, pokemon3])
    .then(pokemon => {
        console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('🏆 PRIMER POKÉMON EN RESPONDER');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(`Nombre: ${pokemon.name.toUpperCase()}`);
        console.log(`ID: ${pokemon.id}`);
        console.log(`Tipo: ${pokemon.types.map(t => t.type.name).join(', ')}`);
        console.log(`Altura: ${pokemon.height / 10}m`);
        console.log(`Peso: ${pokemon.weight / 10}kg`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    })
    .catch(error => {
        console.error('❌ Todas las promesas fallaron:', error);
    });

console.log('⏳ Iniciando búsqueda en paralelo (modo carrera)...\n');