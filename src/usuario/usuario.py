class Usuario:
    nombre
    edad
    tableros

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def __str__(self):
        return "Nombre: " + self.nombre + ", Edad: " + self.edad