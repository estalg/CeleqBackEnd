from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from ...entities.vinculo_externo.cotizacion import Cotizacion, CotizacionSchema, CotizacionAnalisis, CotizacionAnalisisSchema
from ...entities.entity import Session
import dateutil.parser
import datetime

bp_cotizacion = Blueprint('bp_cotizacion', __name__)

@bp_cotizacion.route('/cotizacion')
@jwt_required
def consultar_cotizaciones():
    session = Session()
    objeto_cotizacion = session.query(Cotizacion).all()

    schema = CotizacionSchema(many=True)
    cotizaciones = schema.dump(objeto_cotizacion)

    session.close()
    return jsonify(cotizaciones)

@bp_cotizacion.route('/cotizacion/id', methods=['GET'])
@jwt_required
def consultar_cotizacion_id():
    id = request.args.get('id')
    anno = request.args.get('anno')
    session = Session()
    objeto_cotizacion = session.query(Cotizacion).get((id, anno))

    schema = CotizacionSchema()
    cotizacion = schema.dump(objeto_cotizacion)
    session.close()
    return jsonify(cotizacion)


def consultar_cotizacion_ultimo_id_anno(anno: int):
    session = Session()
    max_id = max_id = session.query(func.max(Cotizacion.id)).filter_by(anno=anno)
    session.close()
    if max_id is None:
        return 1
    else:
        return max_id

@bp_cotizacion.route('/cotizacion', methods=['POST'])
@jwt_required
def agregar_cotizacion():
    r = request.get_json()

    r['fechaCotizacion'] = datetime.date(dateutil.parser.parse(r['fechaCotizacion']).year,
                                         dateutil.parser.parse(r['fechaCotizacion']).month,
                                         dateutil.parser.parse(r['fechaCotizacion']).day).strftime('%Y-%m-%d')
    r['fechaSolicitud'] = datetime.date(dateutil.parser.parse(r['fechaSolicitud']).year,
                                         dateutil.parser.parse(r['fechaSolicitud']).month,
                                         dateutil.parser.parse(r['fechaSolicitud']).day).strftime('%Y-%m-%d')
    r['fechaRespuesta'] = datetime.date(dateutil.parser.parse(r['fechaRespuesta']).year,
                                         dateutil.parser.parse(r['fechaRespuesta']).month,
                                         dateutil.parser.parse(r['fechaRespuesta']).day).strftime('%Y-%m-%d')
    # mount exam object
    posted_cotizacion = CotizacionSchema(only=('anno', 'licitacion', 'observaciones','precioMuestreo', 'descuento', 'gastosAdm',
                                               'fechaCotizacion', 'fechaSolicitud', 'fechaRespuesta', 'saldoAfavor', 'granTotal', 'moneda',
                                               'cotizador', 'cliente', 'precioMuestra', 'diasEntregaRes', 'subTotal', 'numeroMuestras',
                                               'usuarioQuimico', 'usuarioFirmante')).load(r)
    posted_cotizacion['id'] = consultar_cotizacion_ultimo_id_anno(posted_cotizacion['anno'])

    cotizacion = Cotizacion(**posted_cotizacion)

    # persist exam
    session = Session()
    session.add(cotizacion)
    session.commit()

    # return created exam
    nueva_cotizacion = CotizacionSchema().dump(cotizacion)
    session.close()
    return jsonify(nueva_cotizacion), 201

@bp_cotizacion.route('/cotizacion/editar', methods=['POST'])
@jwt_required
def editar_cotizacion():
    r = request.get_json()

    r['fechaCotizacion'] = datetime.date(dateutil.parser.parse(r['fechaCotizacion']).year,
                                         dateutil.parser.parse(r['fechaCotizacion']).month,
                                         dateutil.parser.parse(r['fechaCotizacion']).day).strftime('%Y-%m-%d')
    r['fechaSolicitud'] = datetime.date(dateutil.parser.parse(r['fechaSolicitud']).year,
                                        dateutil.parser.parse(r['fechaSolicitud']).month,
                                        dateutil.parser.parse(r['fechaSolicitud']).day).strftime('%Y-%m-%d')
    r['fechaRespuesta'] = datetime.date(dateutil.parser.parse(r['fechaRespuesta']).year,
                                        dateutil.parser.parse(r['fechaRespuesta']).month,
                                        dateutil.parser.parse(r['fechaRespuesta']).day).strftime('%Y-%m-%d')

    posted_cotizacion = CotizacionSchema(
        only=('id', 'anno', 'licitacion', 'observaciones', 'precioMuestreo', 'descuento', 'gastosAdm',
              'fechaCotizacion', 'fechaSolicitud', 'fechaRespuesta', 'saldoAfavor', 'granTotal', 'moneda',
              'cotizador', 'cliente', 'precioMuestra', 'diasEntregaRes', 'subTotal', 'numeroMuestras',
              'usuarioQuimico', 'usuarioFirmante')).load(r)

    cotizacion_actualizada = Cotizacion(**posted_cotizacion)

    session = Session()
    objeto_cotizacion = session.query(Cotizacion).get((cotizacion_actualizada.id, cotizacion_actualizada.anno))
    if objeto_cotizacion is None:
        return "Cotizacion no encontrada", 404

    schema = CotizacionSchema()

    objeto_cotizacion.licitacion = cotizacion_actualizada.licitacion
    objeto_cotizacion.observaciones = cotizacion_actualizada.observaciones
    objeto_cotizacion.precioMuestreo = cotizacion_actualizada.precioMuestreo
    objeto_cotizacion.descuento = cotizacion_actualizada.descuento
    objeto_cotizacion.gastosAdm = cotizacion_actualizada.gastosAdm
    objeto_cotizacion.fechaCotizacion = cotizacion_actualizada.fechaCotizacion
    objeto_cotizacion.fechaSolicitud = cotizacion_actualizada.fechaSolicitud
    objeto_cotizacion.fechaRespuesta = cotizacion_actualizada.fechaRespuesta
    objeto_cotizacion.saldoAfavor = cotizacion_actualizada.saldoAfavor
    objeto_cotizacion.granTotal = cotizacion_actualizada.granTotal
    objeto_cotizacion.moneda = cotizacion_actualizada.moneda
    objeto_cotizacion.cotizador = cotizacion_actualizada.cotizador
    objeto_cotizacion.cliente = cotizacion_actualizada.cliente
    objeto_cotizacion.precioMuestra = cotizacion_actualizada.precioMuestra
    objeto_cotizacion.diasEntregaRes = cotizacion_actualizada.diasEntregaRes
    objeto_cotizacion.subTotal = cotizacion_actualizada.subTotal
    objeto_cotizacion.numeroMuestras = cotizacion_actualizada.numeroMuestras
    objeto_cotizacion.usuarioQuimico = cotizacion_actualizada.usuarioQuimico
    objeto_cotizacion.usuarioFirmante = cotizacion_actualizada.usuarioFirmante

    session.add(objeto_cotizacion)
    session.commit()
    cotizacion = schema.dump(objeto_cotizacion)
    session.close()

    return jsonify(cotizacion)

@bp_cotizacion.route('/cotizacion/analisis', methods=['POST'])
@jwt_required
def agregar_cotizacionAnalisis():
    # mount exam object
    posted_cotAnalisis = CotizacionAnalisisSchema(only=('idCotizacion', 'annoCotizacion', 'descripcion', 'tipoMuestra')).load(request.get_json())

    cotAnalisis = CotizacionAnalisis(**posted_cotAnalisis)

    # persist exam
    session = Session()
    session.add(cotAnalisis)
    session.commit()

    # return created exam
    nueva_cotAnalisis = CotizacionAnalisisSchema().dump(cotAnalisis)
    session.close()
    return jsonify(nueva_cotAnalisis), 201

@bp_cotizacion.route('/cotizacion/analisis', methods=['DELETE'])
@jwt_required
def eliminar_cotizacionAnalisis():
    idCotizacion = request.args.get('idCotizacion')
    annoCotizacion = request.args.get('annoCotizacion')
    descripcion = request.args.get('descripcion')
    tipoMuestra = request.args.get('tipoMuestra')

    session = Session()
    objeto_cotAnalisis = session.query(CotizacionAnalisis).get((idCotizacion, annoCotizacion, descripcion, tipoMuestra))
    if objeto_cotAnalisis is None:
        return "CotAnalisis no encontrada", 404

    session.delete(objeto_cotAnalisis)
    session.commit()

    session.close()
    return '', 200