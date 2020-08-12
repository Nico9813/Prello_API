from main.run import db
from tablero.tablero import Tablero

usuarioXtablero = db.Table('asignaciones',
    db.Column('usuario_id',db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('tablero_id',db.Integer, db.ForeignKey('tablero.id'), primary_key=True)
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    tableros = db.relationship('Tablero', secondary=usuarioXtablero, lazy='subquery')
    roles = db.relationship('Rol', lazy=True)
    
    def __str__(self):
        return "Nombre: " + self.nombre + ", Edad: " + self.edad

    def agregar_tablero(self, tablero : Tablero):
        self.tableros.append(tablero)