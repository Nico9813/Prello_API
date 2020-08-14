from evento.accion import Accion
from evento.evento import Evento
from evento.interesado import Interesado


class Subscripcion:
    interesado: Interesado
    evento: Evento
    accion: Accion

    def __init__(self, interesado: Interesado, evento: Evento, accion: Accion):
        self.interesado = interesado
        self.evento = evento
        self.accion = accion
