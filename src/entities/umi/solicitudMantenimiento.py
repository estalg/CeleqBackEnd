from sqlalchemy import Column, String, Integer, ForeignKey, Date
from src.entities.entity import Base
from marshmallow import Schema, fields


class SolicitudMantenimiento(Base):
    __tablename__ = 'solicitudmantenimiento'

    id = Column(Integer, primary_key=True)
    anno = Column(Integer, primary_key=True)
    nombreSolicitante = Column(String)
    telefono = Column(String)
    contactoAdicional = Column(String)
    urgencia = Column(String)
    areaTrabajo = Column(String)
    lugarTrabajo = Column(String)
    descripcionTrabajo = Column(String)
    estado = Column(String)
    cedulaUsuario = Column(String, ForeignKey('usuarios.cedula'))

    def __init__(self, id, anno, nombreSolicitante, telefono, contactoAdicional, urgencia, areaTrabajo, lugarTrabajo, descripcionTrabajo, estado, cedulaUsuario):
        self.id = id
        self.anno = anno
        self.nombreSolicitante = nombreSolicitante
        self.telefono = telefono
        self.contactoAdicional = contactoAdicional
        self.urgencia = urgencia
        self.areaTrabajo = areaTrabajo
        self.lugarTrabajo = lugarTrabajo
        self.descripcionTrabajo = descripcionTrabajo
        self.estado = estado
        self.cedulaUsuario = cedulaUsuario

class SolicitudMantenimientoAprobada(Base):
    __tablename__ = 'solicitudmantenimientoaprobada'

    idSolicitud = Column(Integer, ForeignKey('solicitudmantenimiento.id'), primary_key=True)
    annoSolicitud = Column(Integer, ForeignKey('solicitudmantenimiento.anno'), primary_key=True)
    fechaAprobacion = Column(Date)
    personaAsignada = Column(String)
    observacionesAprob = Column(String)
    recibido = Column(String)
    insumos = Column(String)
    costoEstimado = Column(String)
    observacionesAnalisis = Column(String)
    ubicacionArchivo = Column(String)
    periodoEjecucion = Column(String)
    observacionesFinales = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, fechaAprobacion, personaAsignada, observacionesAprob, recibido, insumos, costoEstimado, observacionesAnalisis, ubicacionArchivo, periodoEjecucion, observacionesFinales):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.fechaAprobacion = fechaAprobacion
        self.personaAsignada = personaAsignada
        self.observacionesAprob = observacionesAprob
        self.recibido = recibido
        self.insumos = insumos
        self.costoEstimado = costoEstimado
        self.observacionesAnalisis = observacionesAnalisis
        self.ubicacionArchivo = ubicacionArchivo
        self.periodoEjecucion = periodoEjecucion
        self.observacionesFinales = observacionesFinales

class SolicitudMantenimientoRechazada(Base):
    __tablename__ = 'solicitudmantenimientorechazada'

    idSolicitud = Column(Integer, ForeignKey('solicitudmantenimiento.id'), primary_key=True)
    annoSolicitud = Column(Integer, ForeignKey('solicitudmantenimiento.anno'), primary_key=True)
    motivo = Column(String)

    def __init__(self, idSolicitud, annoSolicitud, motivo):
        self.idSolicitud = idSolicitud
        self.annoSolicitud = annoSolicitud
        self.motivo = motivo

class SolicitudMantenimientoSchema(Schema):
    id = fields.Int()
    anno = fields.Int()
    nombreSolicitante = fields.Str()
    telefono = fields.Str()
    contactoAdicional = fields.Str()
    urgencia = fields.Str()
    areaTrabajo = fields.Str()
    lugarTrabajo = fields.Str()
    descripcionTrabajo = fields.Str()
    estado = fields.Str()
    cedulaUsuario = fields.Str()

class SolicitudMantenimientoAprobadaSchema(Schema):
    idSolicitud = fields.Int()
    annoSolicitud = fields.Int()
    fechaAprobacion = fields.Str()
    personaAsignada = fields.Date()
    observacionesAprob = fields.Str()
    recibido = fields.Str()
    insumos = fields.Str()
    costoEstimado = fields.Str()
    observacionesAnalisis = fields.Str()
    ubicacionArchivo = fields.Str()
    periodoEjecucion = fields.Str()
    observacionesFinales = fields.Str()

class SolicitudMantenimientoRechazadaSchema(Schema):
    idSolicitud = fields.Int()
    annoSolicitud = fields.Int()
    monto = fields.Str()