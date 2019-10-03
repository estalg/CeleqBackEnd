from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .entity import Base
from marshmallow import Schema, fields

class Unidad(Base):
    __tablename__ = 'unidad'

    nombre = Column(String, primary_key=True)
    encargado = Column(String, ForeignKey("usuarios.cedula"))

    def __init__(self, nombre, encargado):
        self.nombre = nombre
        self.encargado = encargado



class UnidadSchema(Schema):
    nombre = fields.Str()
    encargado = fields.Str()
