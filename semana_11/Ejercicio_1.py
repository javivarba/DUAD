# Cree una Clase de circle con el atributo radio y un metodo de get_area para calcular el area

import math

class Circle:

 def __init__(self, radius):
        self.radius = radius  

 def get_area(self):
        return math.pi * (self.radius ** 2)
 
my_circle = Circle(5)  
print("Radius:", my_circle.radius)       
print("Area:", my_circle.get_area())     

