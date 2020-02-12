from sqlalchemy import Column, Float, String
from ...entities.entity import Base
from marshmallow import Schema, fields

class precioGiras(Base):
    __tablename__ = 'precioGiras'

    variable = Column(String, primary_key=True)
    valor = Column(Float)

    def __init__(self, variable, valor):
        self.variable = variable
        self.valor = valor

class precioGirasSchema(Schema):
    variable = fields.Str()
    valor = fields.Float()