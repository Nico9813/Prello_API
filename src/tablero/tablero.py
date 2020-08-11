class Tablero:
    nombre : str

    def __init__(self, nombre : str):
        self.nombre = nombre
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre