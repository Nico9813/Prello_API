from main.run import db

class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    tareas = db.relationship('Tarea', lazy=True)
    transiciones = db.relationship('Transicion', lazy=True)

    def __init__(self, nombre : str):
        self.nombre = nombre
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre
