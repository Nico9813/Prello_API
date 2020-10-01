from main.db import db, BaseModel

from evento.accion import Accion
from evento.evento import Evento
from evento.interesado import Interesado
from evento.observable import Observable
from evento.subscripcion import Subscripcion
from tablero.tablero import Tablero
from .rol import Rol
from tarea.estado import Estado

usuarioXtablero = db.Table('asignaciones',
    db.Column('usuario_id',db.String(100), db.ForeignKey('usuarios.id', ondelete="CASCADE"), primary_key=True),
    db.Column('tablero_id',db.Integer, db.ForeignKey('tableros.id', ondelete="CASCADE"), primary_key=True)
)

class Usuario(db.Model, BaseModel, Interesado):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(100), primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    tableros = db.relationship(
        'Tablero', 
        secondary=usuarioXtablero, 
        lazy='subquery',
        passive_deletes=True, 
        cascade="all, delete"
    )
    roles = db.relationship('Rol', cascade="all, delete", lazy=True)

    def __str__(self):
        return "Nombre: " + self.nombre
        
    def __init__(self, id: str):
        self.id = id

    def agregar_tablero(self, tablero : Tablero):
        self.tableros.append(tablero)

    def subscribirse(self, evento: Evento, observable: Observable, accion: Accion):
        observable.agregar_subscripcion(Subscripcion(evento, accion))

    def crear_tarea_en_tablero(self, tablero:Tablero, estado:Estado, titulo:str, descripcion:str):
        pass
