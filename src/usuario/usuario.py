from tablero import Tablero

class Usuario:
    nombre : str
    edad : int
    tableros : list(Tablero)

    def __init__(self, nombre : str, edad : int):
        self.nombre = nombre
        self.edad = edad
        self.tableros = []
    
    def __str__(self):
        return "Nombre: " + self.nombre + ", Edad: " + self.edad + ", Tableros: " + len(self.tableros)

    def agregarTablero(nombre : str):
        self.tableros.append(Tablero(nombre))

