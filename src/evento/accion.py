class Accion:
    def correr(self):
        pass

class Accion_mock(Accion):
    contador : int

    def __init__(self):
        self.contador = 0

    def ejecutar(self):
        self.contador += 1
        print("sumo 1")