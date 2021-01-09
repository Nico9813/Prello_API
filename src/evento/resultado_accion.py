from main.db import db, BaseModel

class ResultadoAccion(db.Model, BaseModel):
    __tablename__ = 'resultados_acciones'
    id = db.Column(db.Integer, primary_key=True)
    transicion_realizada_id = db.Column(db.Integer, db.ForeignKey('transiciones_realizadas.id'), nullable=True)

    respuesta = db.Column(db.String(200))

    def __init__(self, respuesta: str):
        self.respuesta = respuesta

        