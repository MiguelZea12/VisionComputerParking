from models.login import User
from config.database import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from schemas.login_schemas import UserSchema

user_schema = UserSchema()

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        """Registra un nuevo usuario con contraseña encriptada."""
        if User.query.filter_by(email=email).first():
            return {"message": "El email ya está registrado"}, 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Encripta la contraseña
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Usuario registrado exitosamente"}, 201

    @staticmethod
    def login_user(email, password):
        """Autentica al usuario y genera un token JWT."""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))  # ✅ Convertir a str
            user_data = user_schema.dump(user)  
            return {"access_token": access_token, "user": user_data}, 200
        
        return {"message": "Credenciales inválidas"}, 401


