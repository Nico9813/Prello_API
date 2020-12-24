from main.db import db, BaseModel
import json
import requests

class AccionFactory():
    acciones_dicc = {
        'Accion_mock': lambda payload: Accion_mock(payload),
        'Accion_mock_2': lambda payload: Accion_mock_2(payload),
        'WebHook': lambda payload: WebHook(payload)
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
    payload = db.Column(db.Text)

    def ejecutar(self, **kwargs):
        pass

    __mapper_args__ = {
        'polymorphic_identity': 'acciones',
        'polymorphic_on': type
    }

class Accion_mock(Accion):
    contador: int = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        self.contador = 0

    def ejecutar(self):
        self.contador += 1

    __mapper_args__ = {
        'polymorphic_identity': 'Accion_mock'
    }


class Accion_mock_2(Accion):
    contador_2: int = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        self.contador_2 = 0

    def ejecutar(self):
        self.contador_2 += 1

    __mapper_args__ = {
        'polymorphic_identity': 'Accion_mock_2'
    }

class WebHook(Accion):
    url : str = db.Column(db.String(50))
    method : str = db.Column(db.String(1024))
    headers : str = db.Column(db.String(1024))
    body : str = db.Column(db.String(1024))
    response : str = db.Column(db.Text)
    status_code_response : int = db.Column(db.Integer)
    
    def __init__(self,kwargs):
        print(kwargs)
        self.url = kwargs['url']
        self.method = kwargs['method']
        self.headers = kwargs['header']
        self.body = kwargs['body']
        self.response = None
        self.status_code_response = None
        self.payload = json.dumps(kwargs)

    def ejecutar(self):
        response = {
            "GET": lambda : requests.get(self.url, headers=self.headers, data=self.body),
            "POST": lambda : requests.post(self.url, headers=self.headers, data=self.body),
        }[self.method]()
        self.response = response.text
        self.status_code_response = response.status_code
        self.save()

    __mapper_args__ = {
        'polymorphic_identity': 'WebHook'
    }