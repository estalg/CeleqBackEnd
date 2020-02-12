from sqlalchemy import Column, String, Float, Integer
from ...entities.entity import Base
from marshmallow import Schema, fields

class Giras(Base):
    __tablename__ = 'Giras'

    id = Column(Integer, primary_key=True)
    provincia = Column(String)
    canton = Column(String)
    localidad = Column(String)
    cantidadTecnicos = Column(Integer)
    cantidadProfesionales = Column(Integer)
    nochesAlojamiento = Column(Integer)
    horasMuestreo = Column(Integer)
    gastoTotal = Column(Float)
    idCotizacion = Column(Integer)
    annoCotizacion = Column(Integer)

    def __init__(self, id, provincia, canton, localidad, cantidadTecnicos, cantidadProfesionales, nochesAlojamiento, horasMuestreo,
                 gastoTotal, idCotizacion, annoCotizacion):
        self.id = id
        self.provincia = provincia
        self.canton = canton
        self.localidad = localidad
        self.cantidadTecnicos = cantidadTecnicos
        self.cantidadProfesionales = cantidadProfesionales
        self.nochesAlojamiento = nochesAlojamiento
        self.horasMuestreo = horasMuestreo
        self.gastoTotal = gastoTotal
        self.idCotizacion = idCotizacion
        self.annoCotizacion = annoCotizacion

class GirasSchema(Schema):
    id = fields.Int()
    provincia = fields.Str()
    canton = fields.Str()
    localidad = fields.Str()
    cantidadTecnicos = fields.Int()
    cantidadProfesionales = fields.Int()
    nochesAlojamiento = fields.Int()
    horasMuestreo = fields.Int()
    gastoTotal = fields.Float()
    idCotizacion = fields.Int()
    annoCotizacion = fields.Int()