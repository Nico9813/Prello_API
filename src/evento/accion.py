from main.run import db

class Accion(db.Model):

    __tablename__ = 'acciones'
    id = db.Column(db.Integer, primary_key=True)
    transicion_id = db.Column(db.Integer, db.ForeignKey('transiciones_posibles.id'), nullable=True)
    subscripcion_id = db.Column(db.Integer, db.ForeignKey('subscripciones.id'), nullable=True)
    type = db.Column(db.String(50))

    def ejecutar(self):
        pass

    __mapper_args__ = {
        'polymorphic_identity': 'acciones',
        'polymorphic_on': type
    }

class Accion_mock(Accion):
    contador : int = db.Column(db.Integer, nullable=False)

    def __init__(self):
        self.contador = 0

    def ejecutar(self):
        self.contador += 1
        print("sumo 1")

        __mapper_args__ = {
            'polymorphic_identity': 'Accion_mock'
        }
