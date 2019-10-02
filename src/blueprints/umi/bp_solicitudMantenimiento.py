from flask import Blueprint, jsonify, request
from src.entities.entity import Session
from ...entities.umi.solicitudMantenimiento import SolicitudMantenimiento, SolicitudMantenimientoAprobada, SolicitudMantenimientoRechazada,\
    SolicitudMantenimientoSchema, SolicitudMantenimientoAprobadaSchema, SolicitudMantenimientoRechazadaSchema

bp_solicitudMantenimiento = Blueprint('bp_solicitudMantenimiento', __name__)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento')
#@jwt_required
def consultar_SolicitudMantenimiento():
    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).all()

    schema = SolicitudMantenimientoSchema(many=True)
    solicitudMantenimiento = schema.dump(objeto_solicitudMantenimiento)

    session.close()
    return jsonify(solicitudMantenimiento)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/pendiente')
#@jwt_required
def consultar_SolicitudMantenimiento_pendientes():
    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).filter(SolicitudMantenimiento.estado == 'pendiente').all()

    schema = SolicitudMantenimientoSchema(many=True)
    solicitudMantenimiento = schema.dump(objeto_solicitudMantenimiento)

    session.close()
    return jsonify(solicitudMantenimiento)

@bp_solicitudMantenimiento.route('solicitudMantenimiento/aprobar')
#@jwt_required
def aprobar_solicitud():
    id = request.args.get('id')
    anno = request.args.get('anno')
    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get((id, anno))
    schema = SolicitudMantenimientoSchema()
    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrada", 404


@bp_solicitudMantenimiento.route('/solicitudMantenimiento/id', methods=['GET'])
#@jwt_required
def consultar_solicitudMantenimiento_id():
    id = request.args.get('id')
    anno = request.args.get('anno')
    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get((id,anno))

    schema = SolicitudMantenimientoSchema()
    solicitudMantenimiento = schema.dump(objeto_solicitudMantenimiento)
    session.close()
    return jsonify(solicitudMantenimiento)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento', methods=['POST'])
#@jwt_required
def agregar_solicitudMantenimiento():
    # mount exam object
    posted_solicitudMantenimiento = SolicitudMantenimientoSchema(only=('id', 'anno','nombreSolicitante','telefono','contactoAdicional','urgencia',
                                                                       'areaTrabajo','lugarTrabajo','descripcionTrabajo','estado'))\
        .load(request.get_json())

    solicitudMantenimiento = SolicitudMantenimiento(**posted_solicitudMantenimiento)

    # persist exam
    session = Session()
    session.add(solicitudMantenimiento)
    session.commit()

    # return created exam
    nuevo_solicitudMantenimiento = SolicitudMantenimientoSchema().dump(solicitudMantenimiento)
    session.close()
    return jsonify(nuevo_solicitudMantenimiento), 201

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/editar', methods=['POST'])
#@jwt_required
def editar_solicitudMantenimiento():
    posted_solicitudMantenimiento = SolicitudMantenimientoSchema(only=('id', 'anno','nombreSolicitante','telefono','contactoAdicional','urgencia',
                                                                       'areaTrabajo','lugarTrabajo','descripcionTrabajo','estado'))\
        .load(request.get_json())

    solicitudMantenimiento_actualizado = SolicitudMantenimiento(**posted_solicitudMantenimiento)

    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get((solicitudMantenimiento_actualizado.id, solicitudMantenimiento_actualizado.anno))
    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrada", 404

    schema = SolicitudMantenimientoSchema()

    objeto_solicitudMantenimiento.nombreSolicitante = solicitudMantenimiento_actualizado.nombreSolicitante
    objeto_solicitudMantenimiento.telefono = solicitudMantenimiento_actualizado.telefono
    objeto_solicitudMantenimiento.contactoAdicional = solicitudMantenimiento_actualizado.contactoAdicional
    objeto_solicitudMantenimiento.urgencia = solicitudMantenimiento_actualizado.urgencia
    objeto_solicitudMantenimiento.areaTrabajo = solicitudMantenimiento_actualizado.areaTrabajo
    objeto_solicitudMantenimiento.lugarTrabajo = solicitudMantenimiento_actualizado.lugarTrabajo
    objeto_solicitudMantenimiento.descripcionTrabajo = solicitudMantenimiento_actualizado.descripcionTrabajo
    objeto_solicitudMantenimiento.estado = solicitudMantenimiento_actualizado.estado

    session.add(objeto_solicitudMantenimiento)
    session.commit()
    solicitudMantenimiento = schema.dump(objeto_solicitudMantenimiento)
    session.close()

    return jsonify(solicitudMantenimiento)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento', methods=['DELETE'])
#@jwt_required
def eliminar_solicitudMantenimiento():
    id = request.args.get('id')
    anno = request.args.get('anno')

    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get((id,anno))
    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrado", 404

    session.delete(objeto_solicitudMantenimiento)
    session.commit()

    session.close()
    return '', 200
