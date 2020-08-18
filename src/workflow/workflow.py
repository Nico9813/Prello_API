from .transicion_posible import Transicion_posible
from tarea.estado import Estado
from evento.accion import Accion
from pommons.list import find
import functools

class Workflow:
    transiciones_posibles: list

    def es_la_transicion(self, estado_inicial: Estado, estado_final: Estado, transicion: Transicion_posible) -> bool:
        return estado_inicial == transicion.estado_inicial and estado_final == transicion.estado_final

    def agregar_accion_entre_estados(self, estado_inicial: Estado, estado_final: Estado, accion: Accion):
            transicion: Transicion_posible = find(self.transiciones_posibles, functools.partial(es_la_transicion, estado_inicial, estado_final))
            if transicion is not None:
                transicion.agregar_accion(accion)
            else:
                transicion_nueva = Transicion_posible(estado_inicial, estado_final)
                transicion_nueva.agregar_accion(accion)
                self.transiciones_posibles.append(transicion_nueva)
            
    #def obtener_funciones_para_transicion(self, estado_inicial: Estado, estado_final: Estado):
    #    for
