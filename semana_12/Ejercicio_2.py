# Ejercicio 2


from abc import ABC, abstractmethod
import math

#Clase abstracta

class shape(ABC):
    @abstractmethod
    def calculate_perimeter(self):
        pass

    @abstractmethod
    def calculate_area(self):
        pass

# Clases herederas

class Circle(shape):
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_perimeter (self):
        return 2 * math.pi * self.radius
    def calculate_area(self):
        return math.pi * (self.radius ** 2)
    

class Square(shape):
    def __init__(self, side):
        self.side = side

    def calculate_perimeter(self):
        return 4 * self.side
    def calculate_area(self):
        return self.side ** 2
    

class Rectangle (shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_perimeter(self):
        return 2 * (self.width + self.height)
    
    def calculate_area(self):
        return self.width * self.height
    

