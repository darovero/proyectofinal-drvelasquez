from models.db import db
from models.producto import Producto
from models.ingredientes import Ingrediente

class Heladeria(db.Model):
    __tablename__ = 'heladeria'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)

    productos = db.relationship('Producto', backref='heladeria', lazy=True)
    ingredientes = db.relationship('Ingrediente', backref='heladeria', lazy=True)

    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

    @classmethod
    def cargar_desde_bd(cls):
        """Carga la heladería con sus productos e ingredientes desde la base de datos."""
        heladeria = cls.query.first()
        if not heladeria:
            return None

        heladeria.productos = Producto.query.filter_by(heladeria_id=heladeria.id).all()
        heladeria.ingredientes = Ingrediente.query.filter_by(heladeria_id=heladeria.id).all()

        return heladeria

    def vender(self, producto):

        ingredientes_faltantes = []

        for ingrediente in producto.ingredientes:
            if ingrediente.stock <= 0:
                ingredientes_faltantes.append(ingrediente.nombre)

        if ingredientes_faltantes:
            raise ValueError(ingredientes_faltantes[0])

        for ingrediente in producto.ingredientes:
            ingrediente.stock -= 1

        db.session.commit()
        return "¡Vendido!"
