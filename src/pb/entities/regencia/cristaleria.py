from sqlalchemy import Column, String, Integer
from ..entity import Base
from marshmallow import Schema, fields

class Cristaleria(Base):
    __tablename__ = 'cristaleria'

    nombre = Column(String, primary_key=True)
    material = Column(String, primary_key=True)
    capacidad = Column(String, primary_key=True)
    cantidad = Column(Integer)
    caja = Column(String)

    def __init__(self, nombre, material, capacidad, cantidad, caja):
        self.nombre = nombre
        self.material = material
        self.capacidad = capacidad
        self.cantidad = cantidad
        self.caja = caja


class CristaleriaSchema(Schema):
    nombre = fields.Str()
    material = fields.Str()
    capacidad = fields.Str()
    cantidad = fields.Int()
    caja = fields.Str()