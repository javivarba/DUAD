// EJERCICIO 5: Procesar Objeto de Estudiante
// Entrada
const student = {
    name: "John Doe",
    grades: [
        { name: "math", grade: 80 },
        { name: "science", grade: 100 },
        { name: "history", grade: 60 },
        { name: "PE", grade: 90 },
        { name: "music", grade: 98 }
    ]
};

console.log("=== ESTUDIANTE ORIGINAL ===");
console.log(student);
console.log("\n");

function processStudent(student) {
    // 1. Nombre (fácil, ya lo tenemos)
    const name = student.name;
    
    // 2. Calcular promedio de notas
    let totalGrades = 0;
    for (const gradeObj of student.grades) {
        totalGrades += gradeObj.grade;
    }
    const gradeAvg = totalGrades / student.grades.length;
    
    // 3. Encontrar materia con nota más alta
    let highestGrade = student.grades[0]; // Empezamos con la primera
    for (const gradeObj of student.grades) {
        if (gradeObj.grade > highestGrade.grade) {
            highestGrade = gradeObj;
        }
    }
    
    // 4. Encontrar materia con nota más baja
    let lowestGrade = student.grades[0]; // Empezamos con la primera
    for (const gradeObj of student.grades) {
        if (gradeObj.grade < lowestGrade.grade) {
            lowestGrade = gradeObj;
        }
    }
    
    // Construir objeto resultado
    return {
        name: name,
        gradeAvg: gradeAvg,
        highestGrade: highestGrade.name,
        lowestGrade: lowestGrade.name
    };
}

const result = processStudent(student);
console.log("=== RESULTADO ===");
console.log(result);
console.log("\n");
