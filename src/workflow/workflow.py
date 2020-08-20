from .transicion_posible import Transicion_posible
from main.run import db
from tarea.estado import Estado
from evento.accion import Accion
from pommons.list import find
from tarea.tarea import Tarea
import functools

class Workflow(db.Model):
    __tablename__ = 'workflows'
    transiciones_posibles: list = db.relationship('Transicion_posible', lazy = True)

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        self.transiciones_posibles = []

    def es_la_transicion(self, estado_inicial: Estado, estado_final: Estado, transicion: Transicion_posible) -> bool:
        return estado_inicial == transicion.estado_inicial and estado_final == transicion.estado_final

    def agregar_transicion(self, estado_inicial: Estado, estado_final: Estado):
        transicion_nueva = Transicion_posible(estado_inicial, estado_final)
        self.transiciones_posibles.append(transicion_nueva)
        return transicion_nueva

    def agregar_accion_entre_estados(self, estado_inicial: Estado, estado_final: Estado, accion: Accion):
            transicion: Transicion_posible = find(self.transiciones_posibles, functools.partial(self.es_la_transicion, estado_inicial, estado_final))
            if transicion is not None:
                transicion.agregar_accion(accion)
            else:
                transicion_nueva = self.agregar_transicion(estado_inicial, estado_final)
                transicion_nueva.agregar_accion(accion)

    def obtener_transicion(self, estado_inicial: Estado, estado_final: Estado) -> list:
        transicion_correcta = find(self.transiciones_posibles, lambda transicion: self.es_la_transicion(estado_inicial, estado_final, transicion))
        return transicion_correcta

    def ejecutar_transicion(self, tarea : Tarea, estado_final : Estado) -> list:
        transicion_a_ejecutar : Transicion_posible = self.obtener_transicion(tarea.estado, estado_final)

        if transicion_a_ejecutar is None:
            raise Excepcion("La transicion no es valida")

        for accion in transicion_a_ejecutar.acciones:
            accion.ejecutar()

        tarea.actualizar_estado(estado_final)

        return transicion_a_ejecutar.acciones
