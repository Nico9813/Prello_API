from .usuario import Usuario

def test_crear_usuario():
    user = Usuario("asda")
    assert user.nombre == "asda"