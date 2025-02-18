from main.db import db, BaseModel

from main.excepciones import TransicionNoValidaError
from .transicion_posible import TransicionPosible
from tablero.transicion_realizada import Transicion_realizada
from tarea.estado import Estado
from evento.accion import Accion
from pommons.list import find
from tarea.tarea import Tarea

class Workflow(db.Model, BaseModel):
    __tablename__ = 'workflows'
    id = db.Column(db.Integer, primary_key=True)
    
    transiciones_posibles = db.relationship('TransicionPosible', cascade="all, delete", lazy='joined')

    def __init__(self):
        self.transiciones_posibles = []

    def get_estados_posibles(self, estado : Estado):
        return map(lambda transicion: transicion.estado_final, filter(lambda transicion: transicion.estado_inicial_id == estado.id, self.transiciones_posibles))

    def es_la_transicion(self, estado_inicial: Estado, estado_final: Estado, transicion: TransicionPosible) -> bool:
        return estado_inicial == transicion.estado_inicial and estado_final == transicion.estado_final

    def agregar_transicion(self, estado_inicial: Estado, estado_final: Estado):
        transicion_nueva = self.obtener_transicion(estado_inicial, estado_final)
        if transicion_nueva is None:
            transicion_nueva = TransicionPosible(estado_inicial, estado_final)
            self.transiciones_posibles.append(transicion_nueva)
        return transicion_nueva

    def agregar_accion_entre_estados(self, estado_inicial: Estado, estado_final: Estado, accion: Accion):
        transicion: TransicionPosible = self.obtener_transicion(estado_inicial, estado_final)
        if transicion is not None:
            transicion.agregar_accion(accion)
        else:
            transicion_nueva = self.agregar_transicion(estado_inicial, estado_final)
            transicion_nueva.agregar_accion(accion)
        return transicion

    def obtener_transicion(self, estado_inicial: Estado, estado_final: Estado) -> list:
        transicion_correcta = find(self.transiciones_posibles, lambda transicion: self.es_la_transicion(estado_inicial, estado_final, transicion))
        return transicion_correcta

    def ejecutar_transicion(self, tarea : Tarea, estado_final : Estado) -> Transicion_realizada:
        transicion_a_ejecutar : TransicionPosible = self.obtener_transicion(tarea.estado, estado_final)

        #if transicion_a_ejecutar is None:
            #raise TransicionNoValidaError("La transicion no es valida")

        respuestas = []

        if transicion_a_ejecutar is not None:
            for accion in transicion_a_ejecutar.acciones:
                respuestas.append(accion.ejecutar())

        tarea.actualizar_estado(estado_final)

        transicion_ejecutada = Transicion_realizada(tarea, estado_final, respuestas)

        return transicion_ejecutada
