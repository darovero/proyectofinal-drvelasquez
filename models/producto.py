from models.db import db

producto_ingrediente = db.Table(
    "producto_ingrediente",
    db.Column("producto_id", db.Integer, db.ForeignKey("producto.id"), primary_key=True),
    db.Column("ingrediente_id", db.Integer, db.ForeignKey("ingrediente.id"), primary_key=True)
)

class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    heladeria_id = db.Column(db.Integer, db.ForeignKey("heladeria.id"), nullable=False)

    # Relación con Ingredientes
    ingredientes = db.relationship(
        "Ingrediente",
        secondary=producto_ingrediente,
        back_populates="productos"
    )

    def __init__(self, nombre, precio, tipo, heladeria_id):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.heladeria_id = heladeria_id

    def calcular_costo_produccion(self):
        """Calcula el costo de producción de un producto basado en el costo de sus ingredientes."""
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_rentabilidad(self):
        """Calcula la rentabilidad del producto (precio de venta - costo de producción)."""
        return self.precio - self.calcular_costo_produccion()

    def calorias_totales(self):
        """Calcula la suma de calorías de todos los ingredientes del producto."""
        return sum(ingrediente.calorias for ingrediente in self.ingredientes)

    def vender(self):
        """Reduce el stock de los ingredientes si están disponibles."""
        for ingrediente in self.ingredientes:
            if ingrediente.stock < 1:
                raise ValueError(f"¡Oh no! Nos hemos quedado sin {ingrediente.nombre}")
            ingrediente.stock -= 1
        db.session.commit()
        return f"Producto {self.nombre} vendido exitosamente"

    def reabastecer(self, cantidad=5):
        """Aumenta el stock de los ingredientes necesarios para este producto."""
        for ingrediente in self.ingredientes:
            ingrediente.stock += cantidad
        db.session.commit()
        return f"Se ha reabastecido el stock de los ingredientes para {self.nombre}"

    def __repr__(self):
        return f"<Producto {self.nombre} - {self.tipo}>"
