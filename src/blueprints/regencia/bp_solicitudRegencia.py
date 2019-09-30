from flask import Blueprint, jsonify, request
from ...entities.regencia.solicitudRegencia import Solicitud, Reactivos_Solicitados, Cristaleria_Solicitada, SolicitudSchema
from ...entities.entity import Session

bp_solicitudRegencia = Blueprint('bp_solicitudRegencia', __name__)

@bp_solicitudRegencia.route('/solicitudRegencia')
def consultar_Solicitud():
    session = Session()
    objeto_Solicitud = session.query(Solicitud).all()

    schema = SolicitudSchema(many=True)
    solicitud = schema.dump(objeto_Solicitud)

    session.close()
    return jsonify(solicitud)