from main.run import db
from .estado import Estado

class Tarea(db.Model, Observable):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.relationship('Estado', lazy=True)
    tablero_id = db.Column(db.Integer, db.ForeignKey('tableros.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(150))
    
    def obtener_eventos_posibles(self) -> list:
        return list(Evento_tarea)