from sqlalchemy import Table, Column, Integer, \
    String, MetaData, join, ForeignKey, Date
from sqlalchemy.orm import relationship

from ..entity import Base
from marshmallow import Schema, fields

class Solicitud(Base):
    __tablename__ = 'solicitud_react_crist'

    id = Column(String, primary_key=True)
    anno = Column(String, primary_key=True)
    fechaSolicitud = Column(Date)
    fechaAprobacion = Column(Date)
    estado = Column(String)
    nombreSolicitante = Column(String)
    nombreEncargado = Column(String)
    correoSolicitante = Column(String)
    observacion = Column(String)
    unidad = Column(String)
    cedulaUsuario = Column(String)

    def __init__(self, id, anno, fechaSolicitud, fechaAprobacion, estado, nombreSolicitante, nombreEncargado, correoSolicitante, observacion, unidad, cedulaUsuario):
        self.id = id
        self.anno = anno
        self.fechaSolicitud = fechaSolicitud
        self.fechaAprobacion = fechaAprobacion
        self.estado = estado
        self.nombreSolicitante = nombreSolicitante
        self.nombreEncargado = nombreEncargado
        self.correoSolicitante = correoSolicitante
        self.observacion = observacion
        self.unidad = unidad
        self.cedulaUsuario = cedulaUsuario

class Reactivos_Solicitados(Base):
    __tablename__ = 'reactivossolicitados'

    idSolicitud = Column(String, primary_key=True)
    annoSolicitud = Column(String, primary_key=True)
    nombreReactivo = Column(String, primary_key=True)
    pureza = Column(String)
    cantidad = Column(String)
    estadoEnSolicitud = Column(String)
    justificacionRechazo = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, nombreReactivo, pureza, cantidad, estadoEnSolicitud, justificacionRechazo):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.nombreReactivo = nombreReactivo
        self.pureza = pureza
        self.cantidad = cantidad
        self.estadoEnSolicitud = estadoEnSolicitud
        self.justificacionRechazo = justificacionRechazo

class Cristaleria_Solicitada(Base):
    __tablename__ = 'cristaleriasolicitada'

    idSolicitud = Column(String, primary_key=True)
    annoSolicitud = Column(String, primary_key=True)
    nombreCristaleria = Column(String, primary_key=True)
    material = Column(String)
    capacidad = Column(String)
    cantidad = Column(Integer)
    estadoEnSolicitud = Column(Integer)
    justificacionRechazo = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, nombreCristaleria, material, capacidad, cantidad, estadoEnSolicitud, justificacionRechazo):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.nombreCristaleria = nombreCristaleria
        self.material = material
        self.capacidad = capacidad
        self.cantidad = cantidad
        self.estadoEnSolicitud = estadoEnSolicitud
        self.justificacionRechazo = justificacionRechazo

class SolicitudSchema(Schema):
    id = fields.Str()
    anno = fields.Str()
    fechaSolicitud = fields.Date()
    fechaAprobacion = fields.Date()
    estado = fields.Str()
    nombreSolicitante = fields.Str()
    nombreEncargado = fields.Str()
    correoSolicitante = fields.Str()
    observacion = fields.Str()
    unidad = fields.Str()
    cedulaUsuario = fields.Str()
    reactivos = relationship("")