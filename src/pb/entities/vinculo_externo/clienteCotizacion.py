from sqlalchemy import Column, String, Boolean
from ...entities.entity import Base
from marshmallow import Schema, fields

class clienteCotizacion(Base):
    __tablename__ = 'ClienteCotizacion'

    nombre = Column(String, primary_key=True)
    telefono = Column(String)
    telefono2 = Column(String)
    correo = Column(String)
    fax = Column(String)
    direccion = Column(String)
    persona_trae_muestra = Column(String)
    contacto = Column(String)

    def __init__(self, nombre, telefono, telefono2, correo, fax, direccion, persona_trae_muestra, contacto):
        self.nombre = nombre
        self.telefono = telefono
        self.telefono2 = telefono2
        self.correo = correo
        self.fax = fax
        self.direccion = direccion
        self.persona_trae_muestra = persona_trae_muestra
        self.contacto = contacto

class clienteCotizacionSchema(Schema):
    nombre = fields.Str()
    telefono = fields.Str()
    telefono2 = fields.Str()
    correo = fields.Str()
    fax = fields.Str()
    direccion = fields.Str()
    persona_trae_muestra = fields.Str()
    contacto = fields.Str()