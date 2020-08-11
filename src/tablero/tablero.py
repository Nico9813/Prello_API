from main.run import db

class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    #usuario_id = db.Column(db.Integer, db.ForeignKey(''))

    def __init__(self, nombre : str):
        self.nombre = nombre
    
    def __str__(self):
        return "Nombre tablero: " + self.nombre
