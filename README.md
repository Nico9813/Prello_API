# Prello

# CASOS DE USO

# - CREAR UN USUARIO
# - CREAR UN TABLERO ( ASIGNACION EN MODO ADMIN )
# - INVITAR A UN TABLERO ( ASIGNACION EN MODO INVITADO ) HACE FALTA LA DIFERENCIACION????
# - CRUD LISTA
# - CRUD TAREA
# - CREAR WORKFLOW
# - AGREGAR INTERACCION WORKFLOW { ID_ESTADO_INICIAL, ID_ESTADO_FINAL , ID_ACCION }
# - LISTAR ACCIONES DISPONIBLES
# - MOSTRAR ACCION ESPECIFICA
# - MOVER TAREA

# SESSION
# - algun dato para obtener el usuario logueado de la base de datos

# END POINTS API

# USUARIO
# - POST    users/                                                      --> NUEVO USUARIO
# - GET     users/                                                      --> OBTENER USUARIO
# - GET     users                                                       --> OBTENER USUARIO PROPIO
# - PUT     users                                                       --> MODIFICAR USUARIO PROPIO
# - DELETE  users                                                       --> BORRAR USUARIO PROPIO

# TABLEROS USUARIO
# - GET     tableros                                                    --> OBTENER TODOS LOS TABLEROS DE USUARIO ID
# - POST    tableros                                                    --> CREAR TABLERO COMO ADMINISTRADOR EN EL USUARIO LOGUEADO
# - POST    tableros/<id_tablero>/shared                                --> ASIGNA COMO INVITADO UN TABLERO AL USUARIO LOGUEADO
# - GET     tableros/<id_tablero>                                       --> OBTENER TABLERO ID_TABLERO
# - PUT     tableros/<id_tablero>                                       --> MODIFICAR TABLERO ID_TABLERO
# - DELETE  tableros/<id_tablero>                                       --> BORRAR TABLERO ID_TABLERO

# LISTAS TABLERO USUARIO
# - GET     tablero/<id_tablero>/estados                                --> OBTENER TODAS LAS estados DE UN TABLERO ????
# - POST    tablero/<id_tablero>/estados                                --> CREAR LISTA ID
# - GET     tablero/<id_tablero>/estados/<id>                           --> OBTENER LISTA ID ????
# - PUT     tablero/<id_tablero>/estados/<id>                           --> MODIFICAR LISTA ID
# - DELETE  tablero/<id_tablero>/estados/<id>                           --> BORRAR LISTA ID

# TAREAS
# - GET     tablero/<id_tablero>/estados/<id>/tareas                    --> OBTENER TODAS LAS TAREAS DE UNA LISTA
# - POST    tablero/<id_tablero>/estados/<id>/tareas                    --> CREAR UNA TAREA ID
# - POST    tablero/<id_tablero>/estados/<id>/tareas/<id>               --> CAMBIAR DE ESTADO UNA TAREA (QUERY PARAMS NUEVO ESTADO)
# - GET     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> OBTENER POSIBLES ESTADOS DESTINO DE UNA TAREA
# - GET     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> OBTENER UNA TAREA ID ????
# - PUT     tablero/<id_tablero>/estados/<id>/tareas/<id>               --> MODIFICAR TAREA ID
# - DELETE  tablero/<id_tablero>/estados/<id>/tareas/<id>               --> BORRAR TAREA ID

# ACCIONES
# - GET     acciones/                                                   --> OBTENER ACCIONES DISPONIBLES
# - GET     acciones/<id>                                               --> OBTENER ACCION ID

# WORKFLOW
# - GET     tableros/<id_tablero>/workflows                             --> OBTENER TODOS LOS WORKFLOWS DE UN TABLERO
# - POST    tableros/<id_tablero>/workflows                             --> CREAR WORKFLOW EN UN TABLERO
# - GET     tableros/<id_tablero>/workflows/<id>                        --> OBTENER WORKFLOW ID
# - PUT     tableros/<id_tablero>/workflows/<id>                        --> MODIFICAR WORKFLOW ID
# - DELETE  tableros/<id_tablero>/workflows/<id>                        --> BORRAR WORKFLOW ID
