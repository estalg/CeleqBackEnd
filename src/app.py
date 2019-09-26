from flask import Flask
from flask_cors import CORS
from src.entities.entity import engine, Base
from .blueprints.bp_usuario import bp_usuario
from .blueprints.regencia.bp_cristaleria import bp_cristaleria
from .blueprints.regencia.bp_reactivo import bp_reactivo

# creating the Flask application
app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

app.register_blueprint(bp_usuario)
app.register_blueprint(bp_cristaleria)
app.register_blueprint(bp_reactivo)

if __name__ == '__main__':
    app.run()
