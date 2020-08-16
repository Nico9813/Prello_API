from main.run import db
from evento.subscripcion import Subscripcion
from sqlalchemy.ext.declarative import declared_attr

class Observable(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def subscripciones(cls):
        return db.relationship('Subscripcion', lazy=True)

    def agregar_subscripcion(self, subscripcion: Subscripcion):
        self.subscripciones.append(subscripcion)

    def obtener_eventos_posibles(self) -> list:
        pass

    def procesar_evento(self, evento):
        for subscripcion in self.subscripciones:
            if subscripcion.evento == evento:
                subscripcion.ejecutar_accion()