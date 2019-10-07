from sqlalchemy import Column, String, Integer
from src.entities.entity import Base
from marshmallow import Schema, fields


class Presupuesto(Base):
    __tablename__ = 'presupuesto'

    codigo = Column(String, primary_key=True)
    nombre = Column(String)

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


class PresupuestoSchema(Schema):
    codigo = fields.Str()
    nombre = fields.Str()
