from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...entities.vinculo_externo.localizaciones import Localizaciones, LocalizacionesSchema
from ...entities.entity import Session

bp_localizaciones = Blueprint('bp_localizaciones', __name__)

@bp_localizaciones.route('/localizaciones')
@jwt_required
def consultar_localizaciones():
    session = Session()
    objeto_localizacion = session.query(Localizaciones).all()

    schema = LocalizacionesSchema(many=True)
    localizaciones = schema.dump(objeto_localizacion)

    session.close()
    return jsonify(localizaciones)

@bp_localizaciones.route('/localizaciones/provincias')
@jwt_required
def consultar_localizaciones_provincias():
    session = Session()
    objeto_localizacion = session.query(Localizaciones).distinct(Localizaciones.provincia).group_by(Localizaciones.provincia).all()

    schema = LocalizacionesSchema(many=True)
    localizaciones = schema.dump(objeto_localizacion)

    session.close()
    return jsonify(localizaciones)

@bp_localizaciones.route('/localizaciones/id', methods=['GET'])
@jwt_required
def consultar_localizacion_id():
    provincia = request.args.get('provincia')
    canton = request.args.get('canton')
    localidad = request.args.get('localidad')
    session = Session()
    objeto_localizacion = session.query(Localizaciones).get((provincia, canton, localidad))

    schema = LocalizacionesSchema()
    localizacion = schema.dump(objeto_localizacion)
    session.close()
    return jsonify(localizacion)

@bp_localizaciones.route('/localizaciones', methods=['POST'])
@jwt_required
def agregar_localizacion():
    # mount exam object
    posted_localizacion = LocalizacionesSchema(only=('provincia', 'canton', 'localidad', 'distancia','hospedaje')).load(request.get_json())

    localizacion = Localizaciones(**posted_localizacion)

    # persist exam
    session = Session()
    session.add(localizacion)
    session.commit()

    # return created exam
    nueva_localizacion = LocalizacionesSchema().dump(localizacion)
    session.close()
    return jsonify(nueva_localizacion), 201

@bp_localizaciones.route('/localizaciones/editar', methods=['POST'])
@jwt_required
def editar_localizacion():
    posted_localizacion = LocalizacionesSchema(only=('provincia', 'canton', 'localidad', 'distancia','hospedaje')).load(request.get_json())

    localizacion_actualizada = Localizaciones(**posted_localizacion)

    session = Session()
    objeto_localizacion = session.query(Localizaciones).get((localizacion_actualizada.provincia, localizacion_actualizada.canton, localizacion_actualizada.localidad))
    if objeto_localizacion is None:
        return "Localización no encontrada", 404

    schema = LocalizacionesSchema()

    objeto_localizacion.distancia = localizacion_actualizada.distancia
    objeto_localizacion.hospedaje = localizacion_actualizada.hospedaje

    session.add(objeto_localizacion)
    session.commit()
    localizacion = schema.dump(objeto_localizacion)
    session.close()

    return jsonify(localizacion)

@bp_localizaciones.route('/localizaciones', methods=['DELETE'])
@jwt_required
def eliminar_localizacion():
    provincia = request.args.get('provincia')
    canton = request.args.get('canton')
    localidad = request.args.get('localidad')

    session = Session()
    objeto_localizacion = session.query(Localizaciones).get((provincia, canton, localidad))
    if objeto_localizacion is None:
        return "Localización no encontrada", 404

    session.delete(objeto_localizacion)
    session.commit()

    session.close()
    return '', 200

@bp_localizaciones.route('/localizaciones/provincia', methods=['GET'])
@jwt_required
def filtar_provincia():
    provincia = request.args.get('provincia')
    session = Session()
    objeto_localizacion = session.query(Localizaciones).filter_by(provincia=provincia).distinct(Localizaciones.canton).group_by(Localizaciones.canton).all()

    schema = LocalizacionesSchema(many=True)
    localizacion = schema.dump(objeto_localizacion)
    session.close()
    return jsonify(localizacion), 200

@bp_localizaciones.route('/localizaciones/canton', methods=['GET'])
@jwt_required
def filtar_canton():
    canton = request.args.get('canton')
    session = Session()
    objeto_localizacion = session.query(Localizaciones).filter_by(canton=canton).all()

    schema = LocalizacionesSchema(many=True)
    localizacion = schema.dump(objeto_localizacion)
    session.close()
    return jsonify(localizacion), 200