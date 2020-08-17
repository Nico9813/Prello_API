from .transicion_posible import Transicion_posible
from tarea.estado import Estado
from evento.accion import Accion

class Workflow:
    transiciones_posibles: list

    def aniadir_accion_entre_estados(self, estado_inicial: Estado, estado_final: Estado, accion: Accion):

        for transicion in self.transiciones_posibles:
            if(estado_inicial == transicion.estado_inicial and estado_final == transicion.estado_final):
                transicion.agregar_accion(accion)
                break
        else:
            transicion_nueva = Transicion_posible(estado_inicial, estado_final)
            transicion_nueva.agregar_accion(accion)
            self.transiciones_posibles.append(transicion_nueva)