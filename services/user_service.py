from models.user_profile import Usuario
from models.login import User
from config.database import db
from schemas.user_schemas import UsuarioSchema
from datetime import datetime

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

class UsuarioService:
    @staticmethod
    def get_all_usuarios():
        usuarios = Usuario.query.all()
        return usuarios_schema.dump(usuarios), 200

    @staticmethod
    def get_usuario_by_id(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404
        return usuario_schema.dump(usuario), 200

    @staticmethod
    def create_usuario(data):
        try:
            # Crear el usuario de login primero
            username = f"{data['nombre'].lower()}{data['apellido'].lower()}"
            new_user = User(
                username=username,
                email=data.get('email', f"{username}@example.com")
            )
            # Usar la cédula como contraseña
            new_user.set_password(data['cedula'])
            db.session.add(new_user)
            db.session.flush()  # Para obtener el ID del usuario creado

            # Crear el usuario principal
            new_usuario = Usuario(
                cedula=data['cedula'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if 'fecha_nacimiento' in data else None,
                user_id=new_user.id
            )
            db.session.add(new_usuario)
            db.session.commit()

            return usuario_schema.dump(new_usuario), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error al crear usuario: {str(e)}"}, 400

    @staticmethod
    def update_usuario(usuario_id, data):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        try:
            # Actualizar campos del usuario
            for key, value in data.items():
                if key == 'fecha_nacimiento' and value:
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                if hasattr(usuario, key):
                    setattr(usuario, key, value)

            # Si se proporciona email o username, actualizar el usuario de login
            if usuario.user and ('email' in data or 'username' in data):
                if 'email' in data:
                    usuario.user.email = data['email']
                if 'username' in data:
                    usuario.user.username = data['username']

            db.session.commit()
            return usuario_schema.dump(usuario), 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error al actualizar usuario: {str(e)}"}, 400

    @staticmethod
    def delete_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        try:
            # Eliminar el usuario de login si existe
            if usuario.user:
                db.session.delete(usuario.user)
            db.session.delete(usuario)
            db.session.commit()
            return {"message": "Usuario eliminado exitosamente"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error al eliminar usuario: {str(e)}"}, 400