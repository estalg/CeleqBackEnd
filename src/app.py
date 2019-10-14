from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache

from src.entities.entity import engine, Base
from .cache import cache
from .blueprints.bp_autenticacion import bp_autenticacion
from .blueprints.bp_files import bp_files
from .blueprints.bp_unidad import bp_unidad
from .blueprints.bp_usuario import bp_usuario
from .blueprints.regencia.bp_cristaleria import bp_cristaleria
from .blueprints.regencia.bp_reactivo import bp_reactivo
from .blueprints.regencia.bp_solicitudes_regencia import bp_solicitudes_regencia
from .blueprints.regimen_becario.bp_arancel import bp_arancel
from .blueprints.regimen_becario.bp_presupuesto import bp_presupuesto
from .blueprints.umi.bp_solicitudMantenimiento import bp_solicitudMantenimiento

# creating the Flask application
app = Flask(__name__)
CORS(app)

config = {
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "JWT_SECRET_KEY": '$celeqcrktlqm'
}

app.config.from_mapping(config)
# app.config['JWT_SECRET_KEY'] = '$celeqcrktlqm'
jwt = JWTManager(app)

cache.init_app(app)

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
app.register_blueprint(bp_solicitudes_regencia)
app.register_blueprint(bp_unidad)

if __name__ == '__main__':
    app.run()
