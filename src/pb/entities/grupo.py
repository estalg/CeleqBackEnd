from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields

class Grupo(Base):
    __tablename__ = 'grupos'
    descripcion = Column(String, primary_key=True)

    def __init__(self, descripcion):
        self.descripcion = descripcion

class GruposSchema(Schema):
    descripcion = fields.Str()