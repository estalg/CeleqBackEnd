from sqlalchemy import Column, String
from src.pb.entities.entity import Base
from marshmallow import Schema, fields

class Estudiante(Base):
    __tablename__ = 'estudiante'

    identificacion = Column(String, primary_key=True)
    tipoId = Column(String)
    nombre = Column(String)
    apellido1 = Column(String)
    apellido2 = Column(String)
    correo = Column(String)
    celular = Column(String)
    telefonoFijo = Column(String)
    carrera = Column(String)

    def __init__(self, identificacion, tipoId, nombre, apellido1, apellido2, correo, celular, telefonoFijo, carrera):
        self.identificacion = identificacion
        self.tipoId = tipoId
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.correo = correo
        self.celular = celular
        self.telefonoFijo = telefonoFijo
        self.carrera = carrera

class EstudianteSchema(Schema):
    identificacion = fields.Str()
    tipoId = fields.Str()
    nombre = fields.Str()
    apellido1 = fields.Str()
    apellido2 = fields.Str()
    correo = fields.Str()
    celular = fields.Str()
    telefonoFijo = fields.Str()
    carrera = fields.Str()