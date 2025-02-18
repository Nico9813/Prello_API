from main.db import db, BaseModel

class Rol(db.Model, BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tablero_id = db.Column(db.Integer, db.ForeignKey('tableros.id'), nullable=False)

    def __init__(self, nombre : str):
        self.nombre = nombre
