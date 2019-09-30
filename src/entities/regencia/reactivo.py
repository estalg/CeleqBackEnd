from sqlalchemy import Column, String, Integer
from ..entity import Base
from marshmallow import Schema, fields

class Reactivo(Base):
    __tablename__ = 'reactivos'

    nombre = Column(String, primary_key=True)
    pureza = Column(String, primary_key=True)
    cantidad = Column(Integer)
    estado = Column(String)
    estante = Column(String)

    def __init__(self, nombre, pureza, cantidad, estado, estante):
        self.nombre = nombre
        self.pureza = pureza
        self.cantidad = cantidad
        self.estado = estado
        self.estante = estante


class ReactivoSchema(Schema):
    nombre = fields.Str()
    pureza = fields.Str()
    cantidad = fields.Int()
    estado = fields.Str()
    estante = fields.Str()