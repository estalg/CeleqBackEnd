from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.pb.entities.entity import engine, Base
from .cache import cache
from src.pb.blueprints.bp_autenticacion import bp_autenticacion
from src.pb.blueprints.bp_files import bp_files
from src.pb.blueprints.bp_unidad import bp_unidad
from src.pb.blueprints.bp_usuario import bp_usuario
from src.pb.blueprints.regencia.bp_cristaleria import bp_cristaleria
from src.pb.blueprints.regencia.bp_reactivo import bp_reactivo
from src.pb.blueprints.regencia.bp_solicitudes_regencia import bp_solicitudes_regencia
from src.pb.blueprints.regimen_becario.bp_arancel import bp_arancel
from src.pb.blueprints.regimen_becario.bp_presupuesto import bp_presupuesto
from src.pb.blueprints.umi.bp_solicitudMantenimiento import bp_solicitudMantenimiento
from src.pb.blueprints.regimen_becario.bp_designacion import bp_designaciones
from src.pb.blueprints.bp_grupos import bp_grupos
from src.pb.blueprints.bp_mail import bp_mail
from src.scheduler import scheduler
from src.pb.blueprints.regencia.bp_reporte_cristaleria import bp_reporte_cristaleria
from src.pb.blueprints.regencia.bp_reporte_reactivo import bp_reporte_reactivo
from src.pb.blueprints.regimen_becario.bp_reporte_designaciones import bp_reporte_designaciones

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

scheduler.start()

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
app.register_blueprint(bp_designaciones)
app.register_blueprint(bp_mail)
app.register_blueprint(bp_grupos)
app.register_blueprint(bp_reporte_cristaleria)
app.register_blueprint(bp_reporte_reactivo)
app.register_blueprint(bp_reporte_designaciones)

if __name__ == '__main__':
    app.run(use_reloader=False)
