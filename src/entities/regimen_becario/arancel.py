from sqlalchemy import Column, String, Integer
from src.entities.entity import Base
from marshmallow import Schema, fields


class Arancel(Base):
    __tablename__ = 'aranceles'

    tipo = Column(String, primary_key=True)
    monto = Column(Integer)

    def __init__(self, tipo, monto):
        self.tipo = tipo
        self.monto = monto


class ArancelSchema(Schema):
    tipo = fields.Str()
    monto = fields.Int()
