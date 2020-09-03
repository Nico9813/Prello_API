from main.db import db

from evento.observable import Observable
from evento.subscripcion import Subscripcion
from tarea.tarea import Tarea
from .transicion_realizada import Transicion_realizada
from evento.evento import Evento
from tarea.estado import Estado
from workflow.workflow import Workflow
from workflow.transicion_posible import TransicionPosible

class Tablero(Observable):
    __tablename__ = 'tableros'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=True)

    workflow: Workflow = db.relationship('Workflow', lazy=True, foreign_keys=[workflow_id])
    nombre = db.Column(db.String(80), nullable=True)
    tareas = db.relationship('Tarea', lazy=True)
    transiciones = db.relationship('Transicion_realizada', lazy=True)
    estados = db.relationship('Estado', lazy=True)

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.subscripciones = []
        self.tareas = []
        self.transiciones = []
        self.estados = []
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre

    def agregar_estado(self, estado : Estado):
        self.estados.append(estado)

    def agregar_tarea(self, tarea : Tarea):
        self.tareas.append(tarea)

    def get_estados_posibles(self, estado : Estado):
        return self.workflow.get_estados_posibles(estado)

    def obtener_eventos_posibles(self) -> list:
        return list(Evento)

    def agregar_transicion(self, estado_inicial : Estado, estado_final : Estado):
        return self.workflow.agregar_transicion(estado_inicial, estado_final)

    def ejecutar_transicion(self, tarea: Tarea, estado_final: Estado):
        transicion_historico : Transicion_realizada = Transicion_realizada(tarea, estado_final)
        
        transicion_realizada = self.workflow.ejecutar_transicion(tarea, estado_final)

        self.transiciones.append(transicion_historico)
        
        return transicion_historico
        

        
