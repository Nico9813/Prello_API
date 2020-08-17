from evento.observable import Observable
from evento.subscripcion import Subscripcion
from main.run import db
from tarea.tarea import Tarea
from .transicion_realizada import Transicion_realizada
from evento.evento import Evento
from tarea.estado import Estado

class Tablero(Observable):
    __tablename__ = 'tableros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    tareas = db.relationship('Tarea', lazy=True)
    transiciones = db.relationship('Transicion_realizada', lazy=True)

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.subscripciones = []
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre

    def agregar_tarea(self, tarea : Tarea):
        self.tareas.append(tarea)

    def obtener_eventos_posibles(self) -> list:
        return list(Evento)

    def ejecutar_transicion(self, tarea: Tarea, estado_final: Estado):
        acciones_a_ejecutar = self.workflow.obtener_funciones_para_transicion(tarea.estado, estado_final)
        if length(acciones_a_ejecutar) == 0:
            raise
        transicion_a_realizar = Transicion_realizada(tarea, estado_final, acciones_a_ejecutar)
        for accion in acciones_a_ejecutar:
            accion.ejecutar()

        