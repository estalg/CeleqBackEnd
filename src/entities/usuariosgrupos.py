from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields

class UsuariosGrupos(Base):
    __tablename__ = 'usuariosgrupos'
    usuario = Column(String, primary_key=True)
    grupo = Column(String, primary_key=True)

    def __init__(self, usuario, grupo):
        self.usuario = usuario
        self.grupo = grupo

class UsuariosGruposSchema(Schema):
    usuario = fields.Str()
    grupo = fields.Str()
