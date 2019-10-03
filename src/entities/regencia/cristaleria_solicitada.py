from sqlalchemy import Column, String, Integer, ForeignKey
from ..entity import Base
from marshmallow import Schema, fields


class CristaleriaSolicitada(Base):
    __tablename__ = 'cristaleriasolicitada'

    idSolicitud = Column(Integer, ForeignKey("solicitud_react_crist.id"), primary_key=True)
    annoSolicitud = Column(Integer, ForeignKey("solicitud_react_crist.anno"), primary_key=True)
    nombreCristaleria = Column(String, ForeignKey("cristaleria.nombre"), primary_key=True)
    material = Column(String, ForeignKey("cristaleria.material"), primary_key=True)
    capacidad = Column(String, ForeignKey("cristaleria.capacidad"), primary_key=True)
    cantidadSolicitada = Column(Integer)
    estadoEnSolicitud = Column(String)
    justificacionRechazo = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, nombreCristaleria, material, capacidad, cantidadSolicitada, estadoEnSolicitud,
                 justificacionRechazo):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.nombreCristaleria = nombreCristaleria
        self.material = material
        self.capacidad = capacidad
        self.cantidadSolicitada = cantidadSolicitada
        self.estadoEnSolicitud = estadoEnSolicitud
        self.justificacionRechazo = justificacionRechazo


class CristaleriaSolicitadaSchema(Schema):
    idSolicitud = fields.Int()
    annoSolicitud = fields.Int()
    nombreCristaleria = fields.Str()
    material = fields.Str()
    capacidad = fields.Str()
    cantidadSolicitada = fields.Int()
    estadoEnSolicitud = fields.Str()
    justificacionRechazo = fields.Str()
