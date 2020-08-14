from evento.observable import Observable
from evento.subscripcion import Subscripcion
from main.run import db
from tarea.tarea import Tarea
from transicion.transicion import Transicion

class Tablero(db.Model, Observable):
    __tablename__ = 'tableros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    tareas = db.relationship('Tarea', lazy=True)
    transiciones = db.relationship('Transicion', lazy=True)

    def __init__(self, nombre: str):
        self.nombre = nombre
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre

    def agregar_subscripcion(self, subscripcion: Subscripcion):
        self.subscripciones.append(subscripcion)
