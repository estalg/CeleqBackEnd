from sqlalchemy import Column, String, Float
from ...entities.entity import Base
from marshmallow import Schema, fields

class Localizaciones(Base):
    __tablename__ = 'localizaciones'

    provincia = Column(String, primary_key=True)
    canton = Column(String, primary_key=True)
    localidad = Column(String, primary_key=True)
    distancia = Column(Float)
    hospedaje = Column(Float)

    def __init__(self, provincia, canton, localidad, distancia, hospedaje):
        self.provincia = provincia
        self.canton = canton
        self.localidad = localidad
        self.distancia = distancia
        self.hospedaje = hospedaje

class LocalizacionesSchema(Schema):
    provincia = fields.Str()
    canton = fields.Str()
    localidad = fields.Str()
    distancia = fields.Float()
    hospedaje = fields.Float()