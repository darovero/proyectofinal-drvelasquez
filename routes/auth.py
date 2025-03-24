from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.db import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario con roles opcionales."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    es_admin = data.get('es_admin', False)
    es_empleado = data.get('es_empleado', False)

    if not username or not email or not password:
        return jsonify({"error": "Username, email y contraseña son obligatorios"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    new_user = User(username=username, email=email, password=password, es_admin=es_admin, es_empleado=es_empleado)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

@auth.route('/login', methods=['POST'])
def login():
    """Autentica un usuario y devuelve su información."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.authenticate(username, password)

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    login_user(user)

    return jsonify({
        "message": "Inicio de sesión exitoso",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "es_admin": user.es_admin,
            "es_empleado": user.es_empleado
        }
    }), 200

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cierra la sesión del usuario."""
    logout_user()
    return jsonify({"message": "Cierre de sesión exitoso"}), 200

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    """Retorna la información del usuario autenticado con sus roles."""
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "es_admin": current_user.es_admin,
        "es_empleado": current_user.es_empleado
    }), 200
