from evento.accion import Accion
from evento.evento import Evento
from evento.interesado import Interesado
from evento.observable import Observable
from evento.subscripcion import Subscripcion
from main.run import db
from tablero.tablero import Tablero
from .rol import Rol
from tarea.estado import Estado

usuarioXtablero = db.Table('asignaciones',
    db.Column('usuario_id',db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('tablero_id',db.Integer, db.ForeignKey('tableros.id'), primary_key=True)
)

class Usuario(db.Model, Interesado):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tableros = db.relationship('Tablero', secondary=usuarioXtablero, lazy='subquery')
    roles = db.relationship('Rol', lazy=True)

    def __str__(self):
        return "Nombre: " + self.nombre + ", Edad: " + self.edad

    def __init__(self, nombre: str):
        self.nombre = nombre

    def agregar_tablero(self, tablero : Tablero):
        self.tableros.append(tablero)

    def subscribirse(self, evento: Evento, observable: Observable, accion: Accion):
        observable.agregar_subscripcion(Subscripcion(self, evento, accion))

    def crear_tarea_en_tablero(self, tablero:Tablero, estado:Estado, titulo:str, descripcion:str):
        pass