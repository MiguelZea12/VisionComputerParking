from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({"message": "Datos incompletos"}), 400
    
    return AuthService.register_user(data['username'], data['email'], data['password'])

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ['email', 'password']):
        return jsonify({"message": "Datos incompletos"}), 400
    
    return AuthService.login_user(data['email'], data['password'])

@auth_controller.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Usuario {user_id} ha cerrado sesión"}), 200
