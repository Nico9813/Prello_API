from main.db import db, BaseModel
from evento.accion import Accion
from evento.evento import Evento

class Subscripcion(db.Model, BaseModel):
    __tablename__ = 'subscripciones'
    id = db.Column(db.Integer, primary_key=True)
    evento: Evento = db.Column(db.Enum(Evento))
    accion: Accion = db.relationship('Accion', uselist=False, lazy=True)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'))
    tablero_id = db.Column(db.Integer, db.ForeignKey('tableros.id'))
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'))


    def __init__(self, evento: Evento, accion: Accion):
        self.evento = evento
        self.accion = accion

    def ejecutar_accion(self):
        self.accion.ejecutar()
