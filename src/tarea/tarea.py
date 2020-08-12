from main.run import db

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(150))
    tablero_id = db.Column(db.Integer, db.ForeignKey('tablero.id'), nullable=False)
