from main.run import db

class Estado(db.Model):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    def obtener_eventos_posibles(self) -> list:
        return list(Evento_estado)
