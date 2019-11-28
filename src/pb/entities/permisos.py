from sqlalchemy import Column, String, Integer
from .entity import Base
from marshmallow import Schema, fields

class Permisos(Base):
    __tablename__ = 'permisos'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)

    def __init__(self, id, descripcion):
        self.id = id
        self.descripcion = descripcion

class PermisosSchema(Schema):
    id = fields.Int()
    descripcion = fields.Str()