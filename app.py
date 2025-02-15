from flask import Flask, render_template
from flask_cors import CORS
from config.settings import Config
from config.database import db, create_database
from controllers.status_controller import status_controller
from controllers.video_controller import video_controller
from flask_migrate import Migrate
from controllers.auth_controller import auth_controller
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Aplicar configuración
app.config.from_object(Config)
jwt = JWTManager(app)

# Inicializar DB
db.init_app(app)


migrate = Migrate(app, db)

from models import User
# Crear la base de datos si no existe
with app.app_context():
    create_database()

# Registrar Blueprints
app.register_blueprint(status_controller)
app.register_blueprint(video_controller)
app.register_blueprint(auth_controller)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
