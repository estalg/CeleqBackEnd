from sqlalchemy import Column, String
from .entity import Base
from marshmallow import Schema, fields

class Usuario(Base):
    __tablename__ = 'usuarios'

    cedula = Column(String, primary_key=True)
    correo = Column(String)
    telefono = Column(String)
    nombre = Column(String)
    apellido1 = Column(String)
    apellido2 = Column(String)
    contrasenna = Column(String)

    def __init__(self, cedula, correo, telefono, nombre, apellido1, apellido2, contrasenna):
        self.cedula = cedula
        self.correo = correo
        self.telefono = telefono
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.contrasenna = contrasenna

class UsuarioSchema(Schema):
    cedula = fields.Str()
    correo = fields.Str()
    telefono = fields.Str()
    nombre = fields.Str()
    apellido1 = fields.Str()
    apellido2 = fields.Str()
    contrasenna = fields.Str()