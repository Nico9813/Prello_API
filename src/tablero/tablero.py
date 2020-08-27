from main.db import db

from evento.observable import Observable
from evento.subscripcion import Subscripcion
from tarea.tarea import Tarea
from .transicion_realizada import Transicion_realizada
from evento.evento import Evento
from tarea.estado import Estado
from workflow.workflow import Workflow
from workflow.transicion_posible import Transicion_posible

class Tablero(Observable):
    __tablename__ = 'tableros'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)

    workflow: Workflow = db.relationship('Workflow', lazy=True, foreign_keys=[workflow_id])
    nombre = db.Column(db.String(80), nullable=True)
    tareas = db.relationship('Tarea', lazy=True)
    transiciones = db.relationship('Transicion_realizada', lazy=True)

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.subscripciones = []
        self.tareas = []
        self.transiciones = []
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre

    def agregar_tarea(self, tarea : Tarea):
        self.tareas.append(tarea)

    def obtener_eventos_posibles(self) -> list:
        return list(Evento)

    def ejecutar_transicion(self, tarea: Tarea, estado_final: Estado):
        transicion_historico : Transicion_realizada = Transicion_realizada(tarea, estado_final)
        
        acciones_ejecutadas = self.workflow.ejecutar_transicion(tarea, estado_final)

        self.transiciones.append(transicion_historico)

        

        