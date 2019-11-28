from sqlalchemy import Column, String, Integer, ForeignKey
from ..entity import Base
from marshmallow import Schema, fields


class ReactivosSolicitados(Base):
    __tablename__ = 'reactivossolicitados'

    idSolicitud = Column(Integer, ForeignKey("solicitud_react_crist.id"), primary_key=True)
    annoSolicitud = Column(Integer, ForeignKey("solicitud_react_crist.anno"), primary_key=True)
    nombreReactivo = Column(String, ForeignKey("reactivos.nombre"), primary_key=True)
    pureza = Column(String, ForeignKey("reactivos.pureza"), primary_key=True)
    cantidadSolicitada = Column(Integer)
    estadoEnSolicitud = Column(String)
    justificacionRechazo = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, nombreReactivo, pureza, cantidadSolicitada, estadoEnSolicitud,
                 justificacionRechazo):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.nombreReactivo = nombreReactivo
        self.pureza = pureza
        self.cantidad = cantidadSolicitada
        self.estadoEnSolicitud = estadoEnSolicitud
        self.justificacionRechazo = justificacionRechazo


class ReactivosSolicitadosSchema(Schema):
    idSolicitud = fields.Int()
    annoSolicitud = fields.Int()
    nombreReactivo = fields.Str()
    pureza = fields.Str()
    cantidadSolicitada = fields.Int()
    estadoEnSolicitud = fields.Str()
    justificacionRechazo = fields.Str()
