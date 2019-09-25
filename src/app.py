from flask import Flask
from flask_cors import CORS
from src.entities.entity import engine, Base
from .blueprints.bp_usuario import bp_usuario

# creating the Flask application
app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

app.register_blueprint(bp_usuario)

if __name__ == '__main__':
    app.run()
