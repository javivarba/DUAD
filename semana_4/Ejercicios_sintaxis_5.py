

contador_de_nota = 1
total_de_notas= 0
cantidad_de_notas_aprobadas = 0
cantidad_de_notas_desaprobadas = 0
suma_notas_aprobadas = 0
suma_notas_desaprobadas = 0
promedio_de_notas_total = 0
nota_actual= 0


total_de_notas = int(input( "Enter the amount of grades  "))

while contador_de_nota <= total_de_notas:
    nota_actual = float(input (f"Enter your grade {contador_de_nota}:"))
    contador_de_nota += 1
    


    if nota_actual < 70:
        cantidad_de_notas_desaprobadas +=1
        suma_notas_desaprobadas += nota_actual

    else: 
        cantidad_de_notas_aprobadas +=1
        suma_notas_aprobadas+= nota_actual
    
promedio_de_notas_total += nota_actual / total_de_notas 

contador_de_nota += 1


promedio_de_notas_aprobadas = suma_notas_aprobadas / cantidad_de_notas_aprobadas if cantidad_de_notas_aprobadas > 0 else 0

promedio_de_notas_desaprobadas = suma_notas_desaprobadas / cantidad_de_notas_desaprobadas if cantidad_de_notas_desaprobadas > 0 else 0

print (f"the student passed {cantidad_de_notas_aprobadas} grades")

print( f' The grade average of the pass courses is {promedio_de_notas_aprobadas}')

print(f"the student has {cantidad_de_notas_desaprobadas} grades not approve.")

print(f"the average of the not approve courses is: {promedio_de_notas_desaprobadas}")

print(f"Grade average: {promedio_de_notas_total}")
    


