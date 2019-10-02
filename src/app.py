from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.entities.entity import engine, Base
from .blueprints.bp_usuario import bp_usuario
from .blueprints.bp_autenticacion import bp_autenticacion
from .blueprints.regencia.bp_cristaleria import bp_cristaleria
from .blueprints.regencia.bp_reactivo import bp_reactivo
from .blueprints.regimen_becario.bp_arancel import bp_arancel
from .blueprints.regimen_becario.bp_presupuesto import bp_presupuesto
from .blueprints.umi.bp_solicitudMantenimiento import bp_solicitudMantenimiento
from .blueprints.bp_files import bp_files

# creating the Flask application
app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = '$celeqcrktlqm'
jwt = JWTManager(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

app.register_blueprint(bp_usuario)
app.register_blueprint(bp_autenticacion)
app.register_blueprint(bp_cristaleria)
app.register_blueprint(bp_reactivo)
app.register_blueprint(bp_arancel)
app.register_blueprint(bp_presupuesto)
app.register_blueprint(bp_solicitudMantenimiento)
app.register_blueprint(bp_files)

if __name__ == '__main__':
    app.run()
