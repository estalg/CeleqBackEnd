from sqlalchemy import Column, String, Integer, Date, Boolean
from ...entities.entity import Base
from marshmallow import Schema, fields


class Designacion(Base):
    __tablename__ = 'designacion'

    id = Column(Integer, primary_key=True)
    anno = Column(Integer, primary_key=True)
    ciclo = Column(String)
    fechaInicio = Column(Date)
    fechaFinal = Column(Date)
    convocatoria = Column(String)
    horas = Column(Integer)
    modalidad = Column(String)
    monto = Column(Integer)
    inopia = Column(Boolean)
    motivoInopia = Column(String)
    tramitado = Column(Boolean)
    observaciones = Column(String)
    idEstudiante = Column(String)
    presupuesto = Column(String)
    responsable = Column(String)
    unidad = Column(String)
    adHonorem = Column(Boolean)

    def __init__(self, id, anno, ciclo, fechaInicio, fechaFinal, convocatoria, horas, modalidad, monto, inopia, motivoInopia, tramitado, observaciones,
                 idEstudiante, presupuesto, responsable, unidad, adHonorem):
        self.id = id
        self.anno = anno
        self.ciclo = ciclo
        self.fechaInicio =fechaInicio
        self.fechaFinal = fechaFinal
        self.convocatoria = convocatoria
        self.horas = horas
        self.modalidad = modalidad
        self.monto = monto
        self.inopia = inopia
        self.motivoInopia = motivoInopia
        self.tramitado = tramitado
        self.observaciones = observaciones
        self.idEstudiante = idEstudiante
        self.presupuesto = presupuesto
        self.responsable = responsable
        self.unidad = unidad
        self.adHonorem = adHonorem


class DesignacionSchema(Schema):
    id = fields.Int()
    anno = fields.Int()
    ciclo = fields.Str()
    fechaInicio = fields.Str()
    fechaFinal = fields.Str()
    convocatoria = fields.Str()
    horas = fields.Int()
    modalidad = fields.Str()
    monto = fields.Int()
    inopia = fields.Bool()
    motivoInopia = fields.Str()
    tramitado = fields.Bool()
    observaciones = fields.Str()
    idEstudiante = fields.Str()
    presupuesto = fields.Str()
    responsable = fields.Str()
    unidad = fields.Str()
    adHonorem = fields.Bool()
    nombre = fields.Str()
    apellido1 = fields.Str()
    apellido2 = fields.Str()
    carrera = fields.Str()
    responsable = fields.Str()
    numero = fields.Str()
    ubicacionArchivo = fields.Str()
    idDesignacion = fields.Int()
    annoDesignacion = fields.Int()
    fecha = fields.Str()