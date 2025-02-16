from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.user_service import UsuarioService

usuario_controller = Blueprint('usuario_controller', __name__)

@usuario_controller.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    return UsuarioService.get_all_usuarios()

@usuario_controller.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_usuario(usuario_id):
    return UsuarioService.get_usuario_by_id(usuario_id)

@usuario_controller.route('/usuarios', methods=['POST'])
@jwt_required()
def create_usuario():
    data = request.get_json()
    if not data or not all(key in data for key in ['cedula', 'nombre', 'apellido']):
        return jsonify({"message": "Datos incompletos"}), 400
    return UsuarioService.create_usuario(data)

@usuario_controller.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def update_usuario(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "No hay datos para actualizar"}), 400
    return UsuarioService.update_usuario(usuario_id, data)

@usuario_controller.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(usuario_id):
    return UsuarioService.delete_usuario(usuario_id)