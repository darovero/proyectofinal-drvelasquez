from models.db import db
from models.producto import Producto

class ProductoController:
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos de la base de datos."""
        return Producto.query.all()