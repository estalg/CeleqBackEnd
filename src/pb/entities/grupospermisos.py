from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields

class GruposPermisos(Base):
    __tablename__ = 'grupospermisos'
    grupo = Column(String, primary_key=True)
    permiso = Column(String, primary_key=True)

    def __init__(self, grupo, permiso):
        self.grupo = grupo
        self.permiso = permiso

class GruposPermisosSchema(Schema):
    grupo = fields.Str()
    permiso = fields.Str()
