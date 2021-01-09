from .usuario import Usuario

def test_crear_usuario():
	  user = Usuario("asda")
	  assert user.nombre == "asda"





























 #  Y
    #       estado_prueba = Estado()
  #. .#     estado_prueba.nombre = 'TO DO'
 #     #
   #  #     estado_prueba_2 = Estado()
    #       estado_prueba_2.nombre = 'DOING'
   #
 #          tarea_prueba = Tarea()
#           tarea_prueba.estado = estado_prueba
 #          tarea_prueba.titulo = 'primera tarea'
  #         tarea_prueba.descripcion = 'una muy muy larga descripcion'
   #
  #         transicion_prueba = Transicion()
 #          transicion_prueba.tarea = tarea_prueba
#           transicion_prueba.estado_inicial = estado_prueba
 #          transicion_prueba.estado_final = estado_prueba_2
  #
 #          tablero_prueba = Tablero('tablerito')
#           tablero_prueba.tareas = [tarea_prueba]
  #         tablero_prueba.transiciones = [transicion_prueba]
  #
 #          rol_prueba = Rol()
#           rol_prueba.nombre = 'QA'
# 
  #         usuario_prueba = Usuario()
   #        usuario_prueba.nombre = 'nicolas'
    #       usuario_prueba.edad = 17
   #        usuario_prueba.roles = [rol_prueba]
  #         usuario_prueba.tableros = [tablero_prueba]
  #
   #  db.session.add(usuario_prueba)
  #   db.session.commit()
