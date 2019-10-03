from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from ...entities.entity import Session
from ...entities.regencia.solicitud_regencia import SolicitudRegencia, SolicitudRegenciaSchema
from ...entities.regencia.reactivos_solicitados import ReactivosSolicitados, ReactivosSolicitadosSchema
from ...entities.regencia.cristaleria_solicitada import CristaleriaSolicitada, CristaleriaSolicitadaSchema
from datetime import datetime

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

@bp_solicitudes_regencia.route('/solicitudRegencia/pendientes', methods=['GET'])
@jwt_required
def consultar_solicitudes_regencia_pendientes():
    session = Session()
    objeto_solicitud = session.query(SolicitudRegencia).filter_by(estado='Pendiente').all()

    schema = SolicitudRegenciaSchema(many=True)
    solicitud = schema.dump(objeto_solicitud)

    session.close()
    return jsonify(solicitud)

@bp_solicitudes_regencia.route('/solicitudRegencia/usuario', methods=['GET'])
@jwt_required
def consultar_solicitudes_regencia_usuario():
    cedula = request.args.get('cedula')
    session = Session()
    objeto_solicitud = session.query(SolicitudRegencia).filter_by(cedulaUsuario=cedula).all()

    schema = SolicitudRegenciaSchema(many=True)
    solicitud = schema.dump(objeto_solicitud)

    session.close()
    return jsonify(solicitud)

@bp_solicitudes_regencia.route('/solicitudRegencia/id', methods=['GET'])
@jwt_required
def consultar_solicitudes_regencia_id():
    id = request.args.get('idSolicitud')
    anno = request.args.get('annoSolicitud')
    session = Session()
    objeto_solicitud = session.query(SolicitudRegencia).get((id, anno))

    objeto_reactivos_solicitados = session.query(ReactivosSolicitados).filter_by(idSolicitud=objeto_solicitud.id, annoSolicitud=objeto_solicitud.anno).all()
    objeto_cristleria_solicitada = session.query(CristaleriaSolicitada).filter_by(idSolicitud=objeto_solicitud.id, annoSolicitud=objeto_solicitud.anno).all()



    schema = SolicitudRegenciaSchema()
    solicitud = schema.dump(objeto_solicitud)
    session.close()
    return jsonify(solicitud)

@bp_solicitudes_regencia.route('/solicitudRegencia', methods=['POST'])

def agregar_solicitud_regencia():
    datos_solicitud =request.get_json()
    session = Session()
    try:
        id = session.query(func.max(SolicitudRegencia.id)).filter_by(anno=datos_solicitud['anno']).first()[0]
        if id:
            id += 1
        else:
            id = 1

        datos_solicitud['fechaSolicitud'] = datos_solicitud['fechaSolicitud'].split('T')[0]
        solicitud = SolicitudRegencia(id, datos_solicitud['anno'], datos_solicitud['fechaSolicitud'],
                                      None, datos_solicitud['estado'],
                                      datos_solicitud['nombreSolicitante'], datos_solicitud['nombreEncargado'],
                                      datos_solicitud['correoSolicitante'], datos_solicitud['observacion'],
                                      datos_solicitud['unidad'], datos_solicitud['cedulaUsuario'])
        session.add(solicitud)
        session.commit()
        reactivos = datos_solicitud['reactivosSolicitados']
        cristalerias = datos_solicitud['cristaleriaSolicitada']

        for reactivo in reactivos:
            reactivo_solicitado = ReactivosSolicitados(id, datos_solicitud['anno'], reactivo['nombre'],
                                                       reactivo['pureza'], reactivo['cantidadSolicitada'], 'Pendiente',
                                                       '')
            session.add(reactivo_solicitado)

        for cristaleria in cristalerias:
            cristaleria_solicitada = CristaleriaSolicitada(id, datos_solicitud['anno'], cristaleria['nombre'],
                                                           cristaleria['material'], cristaleria['capacidad'],
                                                           cristaleria['cantidadSolicitada'], 'Pendiente', '')
            session.add(cristaleria_solicitada)

        session.commit()
        return '', 200
    except Exception as e:
        print(e)
        session.rollback()
        return 'Ha ocurrido un error al crear la solicitud', 400