from sqlalchemy import Column, String, Integer, Date
from ...entities.entity import Base
from marshmallow import Schema, fields

class Feriados(Base):
    __tablename__ = 'feriados'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    fecha = Column(Date)

    def __init__(self, id, descripcion, fecha):
        self.id = id
        self.descripcion = descripcion
        self.fecha = fecha

class FeriadosSchema(Schema):
    id = fields.Int()
    descripcion = fields.Str()
    fecha = fields.Date()

class SemanaSanta(Base):
    __tablename__ = 'semanaSanta'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    fechaInicio = Column(Date)
    fechaFinal = Column(Date)

    def __init__(self, id, descripcion, fechaInicio, fechaFinal):
        self.id = id
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFinal = fechaFinal

class SemanaSantaSchema(Schema):
    id = fields.Int()
    descripcion = fields.Str()
    fechaInicio = fields.Date()
    fechaFinal = fields.Date()