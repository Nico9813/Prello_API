from marshmallow  import fields
from main.ext import ma

class UsuarioSchema(ma.Schema):
    nombre      = fields.String()
    tableros    = fields.Nested('TableroSchema', many=True)
    roles       = fields.Nested('RolSchema', many=True)

class RolSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()

class TableroSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()
    workflow    = fields.Nested('WorkflowSchema', many=False, dump_only=True)
    tareas      = fields.Nested('TareaSchema', many=True, dump_only=True)
    transiciones= fields.Nested('TransicionRealizadaSchema', many=True, dump_only=True)
    estados     = fields.Nested('EstadoSchema', many=True, dump_only=True)

class WorkflowSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    transiciones= fields.Nested('TransicionPosibleSchema', many=True)

class TransicionRealizadaSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    tarea       = fields.Nested('TareaSchema', many=False, dump_only=True)
    estado_inicial = fields.Nested('EstadoSchema', many=False, dump_only=True)
    estado_final = fields.Nested('EstadoSchema', many=False, dump_only=True)
    id_estado_final = fields.Integer(load_only=True)
    id_tarea        = fields.Integer(load_only=True)

class TransicionPosibleSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    acciones    = fields.Nested('AccionSchema', many=True, dump_only=True)
    estado_inicial = fields.Nested('EstadoSchema', many=False, dump_only=True)
    estado_final = fields.Nested('EstadoSchema', many=False, dump_only=True)
    id_estado_inicial = fields.Integer(load_only=True)
    id_estado_final = fields.Integer(load_only=True)

class EstadoSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()

class TareaSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    titulo      = fields.String()
    descripcion = fields.String()
    estado      = fields.Nested('EstadoSchema', many=False,dump_only=True)
    tablero_id  = fields.Integer()
    estado_id   = fields.Integer(load_only=True)

class AccionSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    tipo_accion = fields.String(load_only=True)
    payload     = fields.Raw(required=True)

class AccionMockSchema(AccionSchema):
    contador    = fields.Integer()

class SubscripcionSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    tipo_objeto = fields.String() #Validar observables
    id_objeto   = fields.Integer()
    accion      = fields.Nested('AccionSchema', many=False)
    evento      = fields.String() #Validar evento segun observable
