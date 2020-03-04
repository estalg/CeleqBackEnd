from sqlalchemy import Column, String, Integer, Date, Boolean, Float, CHAR
from ...entities.entity import Base
from marshmallow import Schema, fields

class Cotizacion(Base):
    __tablename__ = 'Cotizacion'

    id = Column(Integer, primary_key=True)
    anno = Column(Integer, primary_key=True)
    licitacion = Column(Boolean)
    precioMuestreo = Column(Float)
    descuento = Column(Float)
    gastosAdm = Column(Float)
    fechaCotizacion = Column(Date)
    fechaSolicitud = Column(Date)
    fechaRespuesta = Column(Date)
    observaciones = Column(String)
    iva = Column(Float)
    granTotal = Column(Float)
    moneda = Column(CHAR)
    cotizador = Column(String)
    cliente = Column(String)
    precioMuestra = Column(Float)
    diasEntregaRes = Column(Integer)
    subTotal = Column(Float)
    numeroMuestras = Column(Integer)
    usuarioQuimico = Column(String)
    usuarioFirmante = Column(String)
    cantidadNecesaria = Column(Integer)
    unidadMedida = Column(String)
    especifique = Column(String)

    def __init__(self, id, anno, licitacion, precioMuestreo, descuento, gastosAdm, fechaCotizacion, fechaSolicitud, fechaRespuesta, observaciones, iva,
                 granTotal, moneda, cotizador, cliente, precioMuestra, diasEntregaRes, subTotal, numeroMuestras, usuarioQuimico, usuarioFirmante, cantidadNecesaria,
                 unidadMedida, especifique):
        self.id = id
        self.anno = anno
        self.licitacion = licitacion
        self.precioMuestreo = precioMuestreo
        self.descuento = descuento
        self.gastosAdm = gastosAdm
        self.fechaCotizacion = fechaCotizacion
        self.fechaSolicitud = fechaSolicitud
        self.fechaRespuesta = fechaRespuesta
        self.iva = iva
        self.granTotal = granTotal
        self.moneda = moneda
        self.cotizador = cotizador
        self.cliente = cliente
        self.precioMuestra = precioMuestra
        self.diasEntregaRes = diasEntregaRes
        self.subTotal = subTotal
        self.numeroMuestras = numeroMuestras
        self.usuarioQuimico = usuarioQuimico
        self.usuarioFirmante = usuarioFirmante
        self.observaciones = observaciones
        self.cantidadNecesaria = cantidadNecesaria
        self.unidadMedida = unidadMedida
        self.especifique = especifique

class CotizacionSchema(Schema):
    id = fields.Int()
    anno = fields.Int()
    licitacion = fields.Bool()
    precioMuestreo = fields.Float()
    descuento = fields.Float()
    gastosAdm = fields.Float()
    fechaCotizacion = fields.Date()
    fechaSolicitud = fields.Date()
    fechaRespuesta = fields.Date()
    iva = fields.Float()
    granTotal = fields.Float()
    moneda = fields.Str()
    cotizador = fields.Str()
    cliente = fields.Str()
    precioMuestra = fields.Float()
    diasEntregaRes = fields.Int()
    subTotal = fields.Float()
    numeroMuestras = fields.Int()
    usuarioQuimico = fields.Str()
    usuarioFirmante = fields.Str()
    observaciones = fields.Str()
    cantidadNecesaria = fields.Int()
    unidadMedida = fields.Str()
    especifique = fields.Str()

class CotizacionAnalisis(Base):
    __tablename__ = 'CotizacionAnalisis'

    idCotizacion = Column(Integer, primary_key=True)
    annoCotizacion = Column(Integer, primary_key=True)
    descripcion = Column(String, primary_key=True)
    tipoMuestra = Column(String, primary_key=True)

    def __init__(self, idCotizacion, annoCotizacion, descripcion, tipoMuestra):
        self.idCotizacion = idCotizacion
        self.annoCotizacion = annoCotizacion
        self.descripcion = descripcion
        self.tipoMuestra = tipoMuestra

class CotizacionAnalisisSchema(Schema):
    idCotizacion = fields.Int()
    annoCotizacion = fields.Int()
    descripcion = fields.Str()
    tipoMuestra = fields.Str()