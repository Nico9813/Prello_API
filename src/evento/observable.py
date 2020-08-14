from evento.subscripcion import Subscripcion

class Observable:
    subscripciones: list

    def agregar_subscripcion(self, subscripcion: Subscripcion):
        self.subscripciones.append(subscripcion)

    
        pass

    def procesar_evento(self, evento):
        for subscripcion in self.subscripciones:
            if subscripcion.evento == evento:
                subscripcion.ejecutar_accion()