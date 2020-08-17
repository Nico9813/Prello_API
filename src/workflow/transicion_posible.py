from tarea.estado import Estado
from evento.accion import Accion

class Transicion_posible:
    estado_inicial: Estado
    estado_final: Estado
    acciones: list

    def __init__(self, estado_inicial: Estado, estado_final: Estado):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.acciones = []

    def agregar_accion(self, accion: Accion):
        self.acciones.append(accion)
