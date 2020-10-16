from main.db import db

from .estado import Estado
from evento.subscripcion import Subscripcion
from evento.observable import Observable
from evento.evento import Evento

class Tarea(Observable):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    tablero_id = db.Column(db.Integer, db.ForeignKey('tableros.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    estado = db.relationship('Estado', lazy=True)
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(150))
    estados_posibles = []
    
    def __init__(self, titulo: str, descripcion: str, estado: Estado = None):
        self.estado = estado
        self.titulo = titulo
        self.descripcion = descripcion
        self.subscripciones = []

    def obtener_eventos_posibles(self) -> list:
        return list(Evento)

    def actualizar_estado(self, estado_nuevo : Estado):
        self.estado = estado_nuevo

    def get_estados_posibles(self, workflow):
        self.estados_posibles = workflow.get_estados_posibles(self.estado)
