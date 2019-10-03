from flask import Blueprint, jsonify, request
from src.entities.entity import Session
from ...entities.umi.solicitudMantenimiento import SolicitudMantenimiento, SolicitudMantenimientoAprobada, SolicitudMantenimientoRechazada,\
    SolicitudMantenimientoSchema, SolicitudMantenimientoAprobadaSchema, SolicitudMantenimientoRechazadaSchema
from ...entities.usuario import Usuario
from ...entities.usuariosgrupos import UsuariosGrupos

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

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/pendientes')
#@jwt_required
def consultar_SolicitudMantenimiento_pendientes():
    session = Session()
    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).filter(SolicitudMantenimiento.estado == 'pendiente').all()

    schema = SolicitudMantenimientoSchema(many=True)
    solicitudMantenimiento = schema.dump(objeto_solicitudMantenimiento)

    session.close()
    return jsonify(solicitudMantenimiento)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/analizadas', methods=['GET'])
#@jwt_required
def consultar_SolicitudMantenimiento_analizadas():
    session = Session()
    esAdmin = False
    cedula = request.args.get('cedula')

    objeto_usuarioGrupo = session.query(UsuariosGrupos).filter(UsuariosGrupos.usuario == cedula).all()

    for ug in objeto_usuarioGrupo:
        if(ug.grupo == 'Administrador'):
            esAdmin = True

    if not esAdmin:
        objeto_solicitudMantenimientoAnalizada = session.query(SolicitudMantenimiento, SolicitudMantenimientoAprobada).filter(SolicitudMantenimiento.id == SolicitudMantenimientoAprobada.idSolicitud,
        SolicitudMantenimiento.anno == SolicitudMantenimientoAprobada.annoSolicitud).filter(SolicitudMantenimiento.estado == 'Analizada').all()

        for solicitud in objeto_solicitudMantenimientoAnalizada:
            objeto_usuario = session.query(Usuario).get(solicitud.SolicitudMantenimientoAprobada.personaAsignada)
            solicitud.SolicitudMantenimientoAprobada.nombrePersonaAsignada = (objeto_usuario.nombre + ' ' + objeto_usuario.apellido1 + ' ' + objeto_usuario.apellido2)

        solicitudes_aprobadas = []
        for solicitud in objeto_solicitudMantenimientoAnalizada:
            solicitudes_aprobadas.append(solicitud.SolicitudMantenimientoAprobada)

        schema = SolicitudMantenimientoAprobadaSchema(many=True)

        solicitudAnalizada = schema.dump(solicitudes_aprobadas)
    else:
        objeto_solicitudMantenimientoAnalizada = session.query(SolicitudMantenimiento,
                                                               SolicitudMantenimientoAprobada).filter(
            SolicitudMantenimiento.id == SolicitudMantenimientoAprobada.idSolicitud,
            SolicitudMantenimiento.anno == SolicitudMantenimientoAprobada.annoSolicitud).filter(
            SolicitudMantenimiento.estado == 'Analizada').filter(SolicitudMantenimientoAprobada.personaAsignada == cedula).all()

        for solicitud in objeto_solicitudMantenimientoAnalizada:
            objeto_usuario = session.query(Usuario).get(solicitud.SolicitudMantenimientoAprobada.personaAsignada)
            solicitud.SolicitudMantenimientoAprobada.nombrePersonaAsignada = (
                        objeto_usuario.nombre + ' ' + objeto_usuario.apellido1 + ' ' + objeto_usuario.apellido2)

        solicitudes_aprobadas = []
        for solicitud in objeto_solicitudMantenimientoAnalizada:
            solicitudes_aprobadas.append(solicitud.SolicitudMantenimientoAprobada)

        schema = SolicitudMantenimientoAprobadaSchema(many=True)

        solicitudAnalizada = schema.dump(solicitudes_aprobadas)

    session.close()

    return jsonify(solicitudAnalizada)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/aprobadas')
#@jwt_required
def consultar_SolicitudMantenimiento_aprobadas():
    session = Session()
    esAdmin = False
    cedula = request.args.get('cedula')

    objeto_usuarioGrupo = session.query(UsuariosGrupos).filter(UsuariosGrupos.usuario == cedula).all()

    for ug in objeto_usuarioGrupo:
        if(ug.grupo == 'Administrador'):
            esAdmin = True

    if(esAdmin):
        objeto_solicitudMantenimientoAnalizada = session.query(SolicitudMantenimientoAprobada).all()

        for solicitud in objeto_solicitudMantenimientoAnalizada:
            objeto_usuario = session.query(Usuario).get(solicitud.personaAsignada)
            solicitud.nombrePersonaAsignada = (objeto_usuario.nombre + ' ' + objeto_usuario.apellido1 + ' ' + objeto_usuario.apellido2)

        schema = SolicitudMantenimientoAprobadaSchema(many=True)

        solicitudAnalizada = schema.dump(objeto_solicitudMantenimientoAnalizada)
    else:
        objeto_solicitudMantenimientoAnalizada = session.query(SolicitudMantenimientoAprobada).filter(SolicitudMantenimientoAprobada.personaAsignada == cedula).all()

        for solicitud in objeto_solicitudMantenimientoAnalizada:
            objeto_usuario = session.query(Usuario).get(solicitud.personaAsignada)
            solicitud.nombrePersonaAsignada = (
                        objeto_usuario.nombre + ' ' + objeto_usuario.apellido1 + ' ' + objeto_usuario.apellido2)

        schema = SolicitudMantenimientoAprobadaSchema(many=True)

        solicitudAnalizada = schema.dump(objeto_solicitudMantenimientoAnalizada)

    session.close()

    return jsonify(solicitudAnalizada)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/aprobar', methods=['POST'])
#@jwt_required
def aprobar_solicitud():
    session = Session()

    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get((request.json['id'], request.json['anno']))

    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrada", 404

    objeto_solicitudMantenimiento.estado = request.json['estado']

    session.add(objeto_solicitudMantenimiento)

    if (request.json['estado'] == 'Aprobada'):
        nueva_solicitudAprobada = SolicitudMantenimientoAprobada(request.json['id'],request.json['anno'], request.json['fechaAprobacion'],
                                                                 request.json['personaAsignada'], request.json['observacionesAprob'],'','','','',
                                                                 '','','')
        session.add(nueva_solicitudAprobada)

        session.commit()

        nuevo_solicitudMantenimientoAprobada = SolicitudMantenimientoAprobadaSchema().dump(nueva_solicitudAprobada)
        session.close()

        return jsonify(nuevo_solicitudMantenimientoAprobada)
    else:
        nueva_solicitudRechazada = SolicitudMantenimientoRechazada(request.json['id'],request.json['anno'], request.json['motivoRechazo'])
        session.add(nueva_solicitudRechazada)

        session.commit()

        nuevo_solicitudMantenimientoRechazada = SolicitudMantenimientoRechazadaSchema().dump(nueva_solicitudRechazada)
        session.close()

        return jsonify(nuevo_solicitudMantenimientoRechazada)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/analizar', methods=['POST'])
#@jwt_required
def analizar_solicitud():
    session = Session()

    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get(
        (request.json['id'], request.json['anno']))

    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrada", 404

    objeto_solicitudMantenimiento.estado = request.json['estado']

    session.add(objeto_solicitudMantenimiento)

    objeto_solicitudMantenimientoAnalizada = session.query(SolicitudMantenimientoAprobada).get((request.json['id'], request.json['anno']))

    objeto_solicitudMantenimientoAnalizada.insumos = request.json['insumos']
    objeto_solicitudMantenimientoAnalizada.costoEstimado = request.json['costoEstimado']
    objeto_solicitudMantenimientoAnalizada.observacionesAnalisis = request.json['observacionesAnalisis']
    objeto_solicitudMantenimientoAnalizada.ubicacionArchivo = request.json['ubicacion']

    session.add(objeto_solicitudMantenimientoAnalizada)

    session.commit()

    solicitudMantenimientoAprobada_editada = SolicitudMantenimientoAprobadaSchema().dump(objeto_solicitudMantenimientoAnalizada)

    session.close()

    return jsonify(solicitudMantenimientoAprobada_editada)

@bp_solicitudMantenimiento.route('/solicitudMantenimiento/finalizar', methods=['POST'])
#@jwt_required
def finalizar_solicitud():
    session = Session()

    objeto_solicitudMantenimiento = session.query(SolicitudMantenimiento).get(
        (request.json['id'], request.json['anno']))

    if objeto_solicitudMantenimiento is None:
        return "Solicitud no encontrada", 404

    objeto_solicitudMantenimiento.estado = request.json['estado']

    session.add(objeto_solicitudMantenimiento)

    objeto_solicitudMantenimientoFinalizada = session.query(SolicitudMantenimientoAprobada).get(
        (request.json['id'], request.json['anno']))

    objeto_solicitudMantenimientoFinalizada.periodoEjecucion = request.json['periodoEjecucion']
    objeto_solicitudMantenimientoFinalizada.observacionesFinales = request.json['observacionesFinales']

    session.add(objeto_solicitudMantenimientoFinalizada)

    session.commit()

    solicitudMantenimientoAprobada_editada = SolicitudMantenimientoAprobadaSchema().dump(
        objeto_solicitudMantenimientoFinalizada)

    session.close()

    return jsonify(solicitudMantenimientoAprobada_editada)

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
