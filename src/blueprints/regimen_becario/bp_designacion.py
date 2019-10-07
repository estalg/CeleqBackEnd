from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from ...entities.entity import Session
from ...entities.regimen_becario.designacion import Designacion, DesignacionSchema, Estudiante, EstudianteSchema
from ...entities.usuario import Usuario, UsuarioSchema

bp_designaciones = Blueprint('bp_designaciones', __name__)


@bp_designaciones.route('/designacion', methods=['GET'])
# @jwt_required
def consultar_solicitudes_regencia():
    session = Session()
    objeto_designacion = session.query(Designacion).all()

    schema = DesignacionSchema(many=True)
    solicitud = schema.dump(objeto_designacion)

    for designacion in objeto_designacion:
        estudiante = session.query(Estudiante).filter(Estudiante.identificacion == designacion.idEstudiante).all()
        responsable = session.query(Usuario).filter(Usuario.cedula == designacion.responsable)



    session.close()
    return jsonify(solicitud)
