from main.db import db, BaseModel

from tarea.estado import Estado
from evento.accion import Accion

class TransicionPosible(db.Model, BaseModel):
    __tablename__ = 'transiciones_posibles'
    id = db.Column(db.Integer, primary_key=True)

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable = False)
    estado_inicial_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable = False)
    estado_final_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable = False)

    estado_inicial: Estado = db.relationship('Estado', lazy = True, foreign_keys = [estado_inicial_id])
    estado_final: Estado = db.relationship('Estado', lazy = True, foreign_keys = [estado_final_id])
    acciones: list = db.relationship('Accion', lazy = True)

    def __init__(self, estado_inicial: Estado, estado_final: Estado):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.acciones = []

    def agregar_accion(self, accion: Accion):
        self.acciones.append(accion)
