from main.db import db, BaseModel

from tarea.estado import Estado
from tarea.tarea import Tarea
from workflow.workflow import Workflow

class Transicion_realizada(db.Model, BaseModel):
    __tablename__ = 'transiciones_realizadas'
    id = db.Column(db.Integer, primary_key=True)
    
    tablero_id = db.Column(db.Integer, db.ForeignKey('tableros.id'), nullable=False)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    estado_inicial_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    estado_final_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)

    tarea = db.relationship('Tarea', lazy=True)
    estado_inicial = db.relationship('Estado', foreign_keys=[estado_inicial_id],lazy=True)
    estado_final = db.relationship('Estado', foreign_keys=[estado_final_id] ,lazy=True)

    def __init__(self, tarea: Tarea, estado_final: Estado):
        self.tarea = tarea
        self.estado_inicial = tarea.estado
        self.estado_final = estado_final