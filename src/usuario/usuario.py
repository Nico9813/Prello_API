

class Usuario:
    nombre : str
    edad : int

    def __init__(self, nombre : str, edad : int):
        self.nombre = nombre
        self.edad = edad
    
    def __str__(self):
        return "Nombre: " + self.nombre + ", Edad: " + self.edad