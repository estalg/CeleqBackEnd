from sqlalchemy import Column, String, Integer, Date
from src.pb.entities.entity import Base
from marshmallow import Schema, fields

class P9(Base):
    __tablename__ = 'p9'

    numero = Column(String, primary_key=True)
    ubicacionArchivo = Column(String)
    idDesignacion = Column(Integer)
    annoDesignacion = Column(Integer)
    fecha = Column(Date)

    def __init__(self, numero, ubicacionArchivo, idDesignacion, annoDesignacion, fecha):
        self.numero = numero
        self.ubicacionArchivo = ubicacionArchivo
        self.idDesignacion = idDesignacion
        self.annoDesignacion = annoDesignacion
        self.fecha = fecha


class P9Schema(Schema):
    numero = fields.Str()
    ubicacionArchivo = fields.Str()
    idDesignacion = fields.Int()
    annoDesignacion = fields.Int()
    fecha = fields.Str()
