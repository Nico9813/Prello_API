from .workflow import Workflow
from tarea.estado import Estado
from pommons.list import isEmpty
from tarea.tarea import Tarea
from evento.accion import Accion_mock

def test_agregar_transicion():
	workflow = Workflow()
	workflow.agregar_transicion(Estado("TODO"), Estado("DOING"))
	assert not isEmpty(workflow.transiciones_posibles)

def test_ejecutar_transicion():
	workflow = Workflow()
	to_do = Estado("TODO")
	doing = Estado("DOING")
	tarea = Tarea(to_do, "Titulo", "Descripcion")
	accion_contador = Accion_mock()
	workflow.agregar_transicion(to_do, doing)
	workflow.agregar_accion_entre_estados(to_do, doing, accion_contador)
	acciones_realizadas = workflow.ejecutar_transicion(tarea, doing)
	assert accion_contador.contador == 1
	assert accion_contador in acciones_realizadas
	assert tarea.estado == doing

def ejecutar_transicion_no_valida():
	with pytest.raises(Exception):
		workflow = Workflow()
		to_do = Estado("TODO")
		doing = Estado("DOING")
		tarea = Tarea(to_do, "Titulo", "Descripcion")
		acciones_realizadas = workflow.ejecutar_transicion(tarea, doing)

	