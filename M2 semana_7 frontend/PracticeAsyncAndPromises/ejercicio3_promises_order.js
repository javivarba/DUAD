

function createWordPromise(word, delay, order) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log(`Resuelta: "${word}" (orden: ${order})`);
            resolve({ word, order });
        }, delay);
    });
}

const promise1 = createWordPromise("very", 1000, 3);
const promise2 = createWordPromise("dogs", 2000, 1);
const promise3 = createWordPromise("cute", 1500, 4);
const promise4 = createWordPromise("are", 500, 2);

console.log(' Iniciando promesas con diferentes delays...\n');

Promise.all([promise1, promise2, promise3, promise4])
    .then(results => {
        console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log(' Resultados de Promise.all():');
        console.log(results);
        
        const sortedWords = results
            .sort((a, b) => a.order - b.order)
            .map(item => item.word);
        
        const sentence = sortedWords.join(' ');
        
        console.log('\n Frase final:');
        console.log(`"${sentence}"`);
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    })
    .catch(error => {
        console.error(' Error:', error);
    });