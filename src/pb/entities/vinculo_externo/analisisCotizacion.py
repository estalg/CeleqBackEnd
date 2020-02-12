from sqlalchemy import Column, String, Integer
from ...entities.entity import Base
from marshmallow import Schema, fields

class Analisis(Base):
    __tablename__ = 'Analisis'
    descripcion = Column(String, primary_key=True)
    tipoMuestra = Column(String, primary_key=True)
    metodo = Column(String)
    precio = Column(Integer)
    acreditacion = Column(Integer)

    def __init__(self, descripcion, tipoMuestra, metodo, precio, acreditacion):
        self.descripcion = descripcion
        self.tipoMuestra = tipoMuestra
        self.metodo = metodo
        self.precio = precio
        self.acreditacion = acreditacion

class AnalisisSchema(Schema):
    descripcion = fields.Str()
    tipoMuestra = fields.Str()
    metodo = fields.Str()
    precio = fields.Int()
    acreditacion = fields.Int()

class TipoMuestra(Base):
    __tablename__ = 'tipoMuestra'
    tipo = Column(String, primary_key=True)

    def __init__(self, tipo):
        self.tipo = tipo

class TipoMuestraSchema(Schema):
    tipo = fields.Str()