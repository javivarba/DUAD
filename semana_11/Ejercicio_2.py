# Cree una clase de Bus con atributo de max_passengers y metodo para agregar pasajeros 1x1.

class Person:
    def __init__(self, name):
        self.name = name
p1 = Person("Alice")
p2 = Person("Bob")
p3 = Person("Carlos")
p4 = Person ("Ben")

class Bus:

    def __init__(self, max_passengers):
        self.max_passengers = max_passengers    
        self.passengers = []     
                   

    def add_passenger(self, person):
        if len(self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} has boarded the bus.")
        else:
            print("The bus is full. Cannot add more passengers.")

    def remove_passenger(self, person):
        if person in self.passengers:
            self.passengers.remove(person)
            print(f"{person.name} has left the bus.")
        else:
            print(f"{person.name} is not on the bus.")

my_bus = Bus (3)
my_bus.add_passenger(p1) 
my_bus.remove_passenger(p2)
my_bus.add_passenger(p2)
my_bus.add_passenger(p3)
my_bus.add_passenger(p4)