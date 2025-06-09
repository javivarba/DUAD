# Ejercicio 3

# La herencia múltiple permite que una clase hija herede atributos y métodos de más de una clase padre.

#Vamos a crear una clase Employee y una clase Logger. Luego una clase Manager que hereda de ambas.

class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def work(self):
        print (f"{self.name} is working as {self.position}")


class Logger:
    def log(self, message):
        print (f"[LOG]: {message}")


class Manager (Employee, Logger):
    def __init__(self, name):
        super().__init__(name, "Manager")

    def approve_budget(self):
        self.log(f"{self.name} approved the budget.")





