from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from pb.entities.regencia.cristaleria import Cristaleria
from pb.entities.regencia.reactivo import Reactivo
from pb.entities.entity import Session
from pb.entities.regencia.solicitud_regencia import SolicitudRegencia, SolicitudRegenciaSchema
from pb.entities.regencia.reactivos_solicitados import ReactivosSolicitados, ReactivosSolicitadosSchema
from pb.entities.regencia.cristaleria_solicitada import CristaleriaSolicitada, CristaleriaSolicitadaSchema
from datetime import date

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

    schema_reactivos = ReactivosSolicitadosSchema(many=True)
    reactivos_solicitados = schema_reactivos.dump(objeto_reactivos_solicitados)
    schema_cristaleria = CristaleriaSolicitadaSchema(many=True)
    cristaleria_solicitada = schema_cristaleria.dump(objeto_cristleria_solicitada)

    schema = SolicitudRegenciaSchema()
    solicitud = schema.dump(objeto_solicitud)
    solicitud['reactivosSolicitados'] = reactivos_solicitados
    solicitud['cristaleriaSolicitada'] = cristaleria_solicitada
    session.close()
    return jsonify(solicitud)

@bp_solicitudes_regencia.route('/solicitudRegencia', methods=['POST'])
@jwt_required
def agregar_solicitud_regencia():
    datos_solicitud = request.get_json()
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

@bp_solicitudes_regencia.route('/solicitudRegencia/editar', methods=['POST'])
@jwt_required
def editar_solicitud_regencia():
    datos_solicitud = request.get_json()
    session = Session()
    try:
        solicitud = session.query(SolicitudRegencia).get((datos_solicitud['id'], datos_solicitud['anno']))
        if solicitud is None:
            return "Solicitud no encontrada", 404

        solicitud.fechaAprobacion = date.today()
        solicitud.estado = datos_solicitud['estado']
        session.add(solicitud)

        for reactivo in datos_solicitud['reactivosSolicitados']:
            reactivo_solicitado = session.query(ReactivosSolicitados).get(( datos_solicitud['id'], datos_solicitud['anno'], reactivo['nombreReactivo'], reactivo['pureza']))
            reactivo_solicitado.estadoEnSolicitud = reactivo['estadoEnSolicitud']
            reactivo_solicitado.justificacionRechazo = reactivo['justificacionRechazo']

            reactivo_actualizado = session.query(Reactivo).get((reactivo['nombreReactivo'], reactivo['pureza']))
            cantidad_actualizada = reactivo_actualizado.cantidad - reactivo_solicitado.cantidadSolicitada

            if cantidad_actualizada < 0:
                return 'No hay suficientes reactivos para aprobar la solicitud', 406

            reactivo_actualizado.cantidad = cantidad_actualizada
            session.add(reactivo_actualizado)
            session.add(reactivo_solicitado)

        for cristaleria in datos_solicitud['cristaleriaSolicitada']:
            cristaleria_solicitada = session.query(CristaleriaSolicitada).get(
                (datos_solicitud['id'], datos_solicitud['anno'], cristaleria['nombreCristaleria'], cristaleria['material'], cristaleria['capacidad']))

            cristaleria_solicitada.estadoEnSolicitud = cristaleria['estadoEnSolicitud']
            cristaleria_solicitada.justificacionRechazo = cristaleria['justificacionRechazo']

            cristaleria_actualizada = session.query(Cristaleria).get(
                (cristaleria['nombreCristaleria'], cristaleria['material'], cristaleria['capacidad']))
            cantidad_actualizada = cristaleria_actualizada.cantidad - cristaleria_solicitada.cantidadSolicitada

            if cantidad_actualizada < 0:
                return 'No hay suficiente cristaleria para aprobar la solicitud', 406

            cristaleria_actualizada.cantidad = cantidad_actualizada
            session.add(cristaleria_actualizada)
            session.add(cristaleria_solicitada)

        session.commit()
        session.close()

        return '', 200
    except Exception as e:
        print(e)
        session.rollback()
        return 'Ha ocurrido un error al editar la solicitud', 400
