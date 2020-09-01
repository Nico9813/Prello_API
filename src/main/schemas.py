from marshmallow  import fields
from main.ext import ma

class UsuarioSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()
    tableros    = fields.Nested('TableroSchema', many=True)
    roles       = fields.Nested('RolSchema', many=True)

class RolSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()

class TableroSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    nombre      = fields.String()
    workflow    = fields.Nested('WorkflowSchema', many=False)
    tareas      = fields.Nested('TareaSchema', many=True)
    transiciones= fields.Nested('TransicionRealizadaSchema', many=True)

class WorkflowSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    transiciones= fields.Nested('TransicionPosibleSchema', many=True)

class TransicionRealizadaSchema(ma.Schema):
    id          = fields.Integer(dump_only=True)
    tarea       = fields.Nested('TareaSchema', many=False)
    estado_inicial = fields.Nested('EstadoSchema', many=False)
    estado_final = fields.Nested('EstadoSchema', many=False)

class TransicionPosible(ma.Schema):
    id          = fields.Integer(dump_only=True)
    acciones    = fields.Nested('AccionSchema', many=True)
    estado_inicial = fields.Nested('EstadoSchema', many=False)
    estado_final = fields.Nested('EstadoSchema', many=False)

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

class AccionMockSchema(AccionSchema):
    contador    = fields.Integer()
