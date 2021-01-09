from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from main.autentificacion import requires_auth, get_usuario_actual
from main.db import db

from main.excepciones import ResourceNotFoundError, PermissionError, TransicionNoValidaError

from .tablero import Tablero
from tarea.tarea import Tarea
from tarea.estado import Estado
from evento.accion import AccionFactory, Accion
from workflow.transicion_posible import TransicionPosible
from usuario.usuario import Usuario
from main.schemas import TableroSchema, TransicionRealizadaSchema, TransicionPosibleSchema, AccionSchema

tablero_router = Blueprint('tablero', __name__)

tablero_schema = TableroSchema()

api = Api(tablero_router)

class TableroListResource(Resource):

    @requires_auth
    def get(self):
        usuario_actual = get_usuario_actual()
        result = tablero_schema.dump(usuario_actual.tableros, many=True)
        return result, 200
    
    @requires_auth
    def post(self):
        data = request.get_json()
        tablero_nuevo_dicc = tablero_schema.load(data)
        usuario_actual = get_usuario_actual()

        tablero_nuevo = Tablero(tablero_nuevo_dicc['nombre'])

        usuario_actual.agregar_tablero(tablero_nuevo)
        tablero_nuevo.save()

        result = tablero_schema.dump(tablero_nuevo)
        return result, 201

class TableroResource(Resource):

    @requires_auth
    def get(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = tablero_schema.dump(tablero_actual)
        return result, 200
    
    def delete(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = tablero_schema.dump(tablero_actual)

        #Borrar todas las tareas asociadas a este tablero
        tareas_a_borrar = Tarea.simple_filter(tablero_id=tablero_id)

        for tarea in tareas_a_borrar:
            tarea.delete()

        tablero_actual.delete()
        return result, 200

class TableroSharedResource(Resource):

    @requires_auth
    def get(self, tablero_id : int):
        tablero = Tablero.get_by_id(tablero_id)

        if tablero is None:
            raise ResourceNotFoundError(
                "El tablero " + str(tablero_id) + " no existe")

        usuario_actual = get_usuario_actual()
        if not tablero.id in map(lambda tablero : tablero.id ,usuario_actual.tableros):
            raise PermissionError(
                "El tablero " + str(tablero_id) + " no pertenece al usuario actual"
            )

        return jsonify({"id": tablero_id})
             

    @requires_auth
    def post(self,tablero_id : int):
        tablero_compartido = Tablero.get_by_id(tablero_id)

        if tablero_compartido is None:
            raise ResourceNotFoundError(
                "El tablero " + str(tablero_id) + " no existe")

        usuario_actual = get_usuario_actual()
        usuario_actual.agregar_tablero(tablero_compartido)
        usuario_actual.save()
        
        result = tablero_schema.dump(tablero_compartido)
        return result, 200

transicion_realizada_schema = TransicionRealizadaSchema()

class TransicionesRealizadasListResource(Resource):

    def get(self, tablero_id : int):
        tablero_actual = Tablero.get_by_id(tablero_id)
        result = transicion_realizada_schema.dump(tablero_actual.transiciones, many=True)
        return result, 200

    def post(self, tablero_id : int):
        data = request.get_json()
        tablero_actual = Tablero.get_by_id(tablero_id)
        transicion_a_realizar_dicc = transicion_realizada_schema.load(data)
        id_tarea = transicion_a_realizar_dicc['id_tarea']
        id_estado_final = transicion_a_realizar_dicc['id_estado_final']
        tarea_actual = Tarea.get_by_id(id_tarea)
        estado_final = Estado.get_by_id(id_estado_final)

        if estado_final is None:
            raise ResourceNotFoundError(
                "El estado " + str(id_estado_final) + " no existe en el tablero")
        if tarea_actual is None:
            raise ResourceNotFoundError(
                "La tarea " + str(id_tarea) + " no existe en el tablero")
        if tarea_actual.tablero_id != tablero_id:
            raise PermissionError(
                "error: La tarea " + str(id_tarea) + " no pertenece al tablero " + str(tablero_id))

        try:
            transicion_realizada = tablero_actual.ejecutar_transicion(tarea_actual, estado_final)
            transicion_realizada.save()
            tarea_actual.save()
            result = transicion_realizada_schema.dump(transicion_realizada)
            status_code = 201
        except TransicionNoValidaError as ex:
            result = jsonify("transicion no valida")
            status_code = 401

        return result

transicion_posible_schema = TransicionPosibleSchema()

class TransicionesPosiblesResource(Resource):
    def delete(self,tablero_id : int, transicion_id : int):
        transicion_actual = TransicionPosible.get_by_id(transicion_id)
        result = transicion_posible_schema.dump(transicion_actual)
        transicion_actual.delete()
        return result, 200
        

class TransicionesPosiblesListResource(Resource):

    def post(self, tablero_id : int):
        data = request.get_json()
        transicion_posible_nueva_dicc = transicion_posible_schema.load(data)
        id_estado_inicial = transicion_posible_nueva_dicc['id_estado_inicial']
        id_estado_final = transicion_posible_nueva_dicc['id_estado_final']
        estado_inicial = Estado.get_by_id(id_estado_inicial)
        estado_final = Estado.get_by_id(id_estado_final)
        tablero_actual = Tablero.get_by_id(tablero_id)

        if estado_inicial is None:
            raise ResourceNotFoundError("El estado " + str(id_estado_inicial) + " no existe en el tablero")
        if estado_final is None:
            raise ResourceNotFoundError("El estado " + str(id_estado_final) + " no existe en el tablero")

        transicion_posible_nueva = tablero_actual.agregar_transicion(estado_inicial, estado_final)
        tablero_actual.save()
        result = transicion_posible_schema.dump(transicion_posible_nueva)
        return result, 201

accion_schema = AccionSchema()

class AccionesTransicionResource(Resource):

    def post(self, tablero_id : int, transicion_id : int):
        data = request.get_json()
        transicion = TransicionPosible.get_by_id(transicion_id)
        accion_a_agregar = AccionFactory.crear_instancia(data['type'], data['payload'])
        estado_inicial = transicion.estado_inicial
        estado_final = transicion.estado_final
        tablero_actual = Tablero.get_by_id(tablero_id)

        if estado_inicial is None:
            raise ResourceNotFoundError("El estado " + str(id_estado_inicial) + " no existe en el tablero")
        if estado_final is None:
            raise ResourceNotFoundError("El estado " + str(id_estado_final) + " no existe en el tablero")

        transicion_modificada = tablero_actual.workflow.agregar_accion_entre_estados(estado_inicial, estado_final, accion_a_agregar)
        transicion_modificada.save()
        result = accion_schema.dump(accion_a_agregar)
        return result, 200

class AccionTransicionResource(Resource):
    def delete(self,tablero_id : int, transicion_id : int, accion_id :int):
        accion_actual = Accion.get_by_id(accion_id)
        result = accion_schema.dump(accion_actual)
        accion_actual.delete()
        return result, 200




api.add_resource(TableroResource, '/tableros/<int:tablero_id>', endpoint='tableros_resource')
api.add_resource(TableroSharedResource, '/tableros/shared/<int:tablero_id>', endpoint='tableros_shared_resource')
api.add_resource(TransicionesRealizadasListResource, '/tableros/<int:tablero_id>/transiciones', endpoint='transiciones_realizadas_list_resource')
api.add_resource(TransicionesPosiblesListResource, '/tableros/<int:tablero_id>/transiciones_posibles', endpoint='transiciones_posibles_list_resource')
api.add_resource(TransicionesPosiblesResource, '/tableros/<int:tablero_id>/transiciones_posibles/<int:transicion_id>', endpoint='transiciones_posibles_resource')
api.add_resource(AccionesTransicionResource, '/tableros/<int:tablero_id>/transiciones_posibles/<int:transicion_id>/acciones', endpoint='acciones_transiciones_posibles_resource')
api.add_resource(AccionTransicionResource, '/tableros/<int:tablero_id>/transiciones_posibles/<int:transicion_id>/acciones/<int:accion_id>', endpoint='accion_transiciones_posibles_resource')
api.add_resource(TableroListResource, '/tableros', endpoint='tableros_list_resource')
