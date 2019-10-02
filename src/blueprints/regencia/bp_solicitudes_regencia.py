from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ...entities.regencia.reactivo import Reactivo, ReactivoSchema
from ...entities.entity import Session
from ...entities.regencia.solicitud_regencia import SolicitudRegencia, SolicitudRegenciaSchema
from ...entities.regencia.reactivos_solicitados import ReactivosSolicitados, ReactivosSolicitadosSchema
from ...entities.regencia.cristaleria_solicitada import CristaleriaSolicitada, CristaleriaSolicitadaSchema

bp_solicitudes_regencia = Blueprint('bp_solicitudes_regencia', __name__)

@bp_solicitudes_regencia.route('/solicitudRegencia', methods=['GET'])
@jwt_required
def consultar_solicitudes_regencia():
    session = Session()
    objeto_solicitud = session.query(SolicitudRegencia).all()

    schema = SolicitudRegenciaSchema(many=True)
    solicitud = schema.dump(objeto_solicitud)

    session.close()
    return jsonify(solicitud)

@bp_solicitudes_regencia.route('/solicitudRegencia/id', methods=['GET'])
def consultar_solicitudes_regencia_id():
    id = request.args.get('idSolicitud')
    anno = request.args.get('annoSolicitud')
    session = Session()
    objeto_solicitud = session.query(SolicitudRegencia).get((id, anno))

    objeto_reactivos_solicitados = session.query(ReactivosSolicitados).filter_by(idSolicitud=objeto_solicitud.id, annoSolicitud=objeto_solicitud.anno).all()
    objeto_cristleria_solicitada = session.query(CristaleriaSolicitada).filter_by(idSolicitud=objeto_solicitud.id, annoSolicitud=objeto_solicitud.anno).all()

    objeto_solicitud.reactivos_solicitados = objeto_reactivos_solicitados
    objeto_solicitud.cristaleria_solicitada = objeto_cristleria_solicitada


    schema = SolicitudRegenciaSchema()
    solicitud = schema.dump(objeto_solicitud)
    session.close()
    return jsonify(solicitud)
