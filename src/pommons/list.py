

def contains(lista: list, elemento)->bool:
    for un_elemento in lista:
        if(un_elemento == elemento):
            return True
    return False

def any(lista: list, funcion)->bool:
    for un_elemento in lista:
        if(funcion(un_elemento)):
            return True
    return False

def find(lista: list, funcion):
    for un_elemento in lista:
        if(funcion(un_elemento)):
            return un_elemento
    return None

def isEmpty(lista: list)->bool:
    return not lista