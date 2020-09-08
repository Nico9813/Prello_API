from main.db import db, BaseModel

class AccionFactory():
    acciones_dicc = {
        'Accion_mock': lambda payload: Accion_mock(payload),
        'Accion_mock_2': lambda payload: Accion_mock_2(payload),
    }

    @classmethod
    def get_acciones_posibles(self):
        acciones_posibles = []
        for key in self.acciones_dicc.keys():
            acciones_posibles.append(key)
        return acciones_posibles

    @classmethod
    def crear_instancia(self, accion_type : str, payload):
        return self.acciones_dicc[accion_type](payload)

class Accion(db.Model, BaseModel):

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
    contador: int = db.Column(db.Integer, default=0)

    def __init__(self, payload = {}):
        self.contador = 0

    def ejecutar(self):
        self.contador += 1

    __mapper_args__ = {
        'polymorphic_identity': 'Accion_mock'
    }


class Accion_mock_2(Accion):
    contador_2: int = db.Column(db.Integer, default=0)

    def __init__(self, payload={}):
        self.contador_2 = 0

    def ejecutar(self):
        self.contador_2 += 1

    __mapper_args__ = {
        'polymorphic_identity': 'Accion_mock_2'
    }
