from main.run import db
from tarea.estado import Estado
from tarea.tarea import Tarea

class Transicion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    tablero_id = db.Column(db.Integer, db.ForeignKey('tablero.id'), nullable=False)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tarea.id'), nullable=False)
    estado_inicial_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    estado_final_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)

    tarea = db.relationship('Tarea', lazy=True)
    estado_inicial = db.relationship('Estado', foreign_keys=[estado_inicial_id],lazy=True)
    estado_final = db.relationship('Estado', foreign_keys=[estado_final_id] ,lazy=True)