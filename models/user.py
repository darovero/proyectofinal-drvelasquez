from models.db import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False, nullable=False)
    es_empleado = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, username, password, email=None, es_admin=False, es_empleado=False):
        """Inicializa un usuario con username, contraseña encriptada y roles opcionales"""
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password).decode('utf-8')
        self.es_admin = es_admin
        self.es_empleado = es_empleado

    def verify_password(self, password):
        """Verifica si la contraseña ingresada es correcta"""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username, password):
        """Autentica un usuario buscando en la base de datos"""
        user = cls.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user
        return None

    def __repr__(self):
        return f"<User {self.username} - Admin: {self.es_admin} | Empleado: {self.es_empleado}>"
