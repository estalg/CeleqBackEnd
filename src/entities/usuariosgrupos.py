from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .entity import Base
from marshmallow import Schema, fields

class UsuariosGrupos(Base):
    __tablename__ = 'usuariosgrupos'
    usuario = Column(String, ForeignKey("usuarios.cedula"), primary_key=True)
    grupo = Column(String, ForeignKey("grupos.descripcion"), primary_key=True)

    usuarios = relationship("Usuario", foreign_keys=[usuario])
    grupos = relationship("Grupo", foreign_keys=[grupo])

    def __init__(self, usuario, grupo):
        self.usuario = usuario
        self.grupo = grupo

class UsuariosGruposSchema(Schema):
    usuario = fields.Str()
    grupo = fields.Str()
