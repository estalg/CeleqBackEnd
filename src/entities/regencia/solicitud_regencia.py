from sqlalchemy import Column, String, Integer, Date, ForeignKey
from ..entity import Base
from marshmallow import Schema, fields


class SolicitudRegencia(Base):
    __tablename__ = 'solicitud_react_crist'

    id = Column(Integer, primary_key=True)
    anno = Column(Integer, primary_key=True)
    fechaSolicitud = Column(Date)
    fechaAprobacion = Column(Date)
    estado = Column(String)
    nombreSolicitante = Column(String)
    nombreEncargado = Column(String)
    correoSolicitante = Column(String)
    observacion = Column(String)

    unidad = Column(String, ForeignKey("unidad.nombre"))
    cedulaUsuario = Column(String, ForeignKey('usuarios.cedula'))

    def __init__(self, id, anno, fechaSolicitud, fechaAprobacion, estado, nombreSolicitante, nombreEncargado,
                 correoSolicitante, observacion, unidad, cedulaUsuario):
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


class SolicitudRegenciaSchema(Schema):
    id = fields.Int()
    anno = fields.Int()
    fechaSolicitud = fields.Date()
    fechaAprobacion = fields.Date()
    estado = fields.Str()
    nombreSolicitante = fields.Str()
    nombreEncargado = fields.Str()
    correoSolicitante = fields.Str()
    observacion = fields.Str()
