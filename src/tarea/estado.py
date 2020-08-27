from main.db import db

from evento.evento import Evento
from evento.observable import Observable
from evento.subscripcion import Subscripcion

class Estado(Observable):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    def __init__(self, nombre : str):
        self.nombre = nombre
        self.subscripciones = []

    def obtener_eventos_posibles(self) -> list:
        return list(Evento)
