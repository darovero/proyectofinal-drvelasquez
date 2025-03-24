from models.db import db

class Ingrediente(db.Model):
    __tablename__ = "ingrediente"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=10)
    heladeria_id = db.Column(db.Integer, db.ForeignKey("heladeria.id"), nullable=False)

    productos = db.relationship(
        "Producto",
        secondary="producto_ingrediente",
        back_populates="ingredientes"
    )

    def __init__(self, nombre, precio, calorias, stock, heladeria_id):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.stock = stock
        self.heladeria_id = heladeria_id

    def es_sano(self):
        """Determina si el ingrediente es considerado sano (ej. menos de 50 calorías)."""
        return self.calorias < 50

    def __repr__(self):
        return f"<Ingrediente {self.nombre} - {self.calorias} Cal>"

    def reabastecer(self, cantidad):
        """Aumenta el stock del ingrediente en la cantidad especificada."""
        self.stock += cantidad
        db.session.commit()
