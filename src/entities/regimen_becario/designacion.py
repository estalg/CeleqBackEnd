from sqlalchemy import Column, String, Integer
from src.entities.entity import Base
from marshmallow import Schema, fields


class Designacion(Base):
    __tablename__ = 'designacion'

    tipo = Column(String, primary_key=True)
    monto = Column(Integer)

    def __init__(self, tipo, monto):
        self.tipo = tipo
        self.monto = monto


class DesignacionSchema(Schema):
    tipo = fields.Str()
    monto = fields.Int()
