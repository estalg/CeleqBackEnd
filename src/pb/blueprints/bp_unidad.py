from flask import Blueprint, jsonify, request
from pb.entities.entity import Session
from pb.entities.unidad import Unidad, UnidadSchema
from flask_jwt_extended import jwt_required

bp_unidad = Blueprint('bp_unidad', __name__)


@bp_unidad.route('/unidad')
@jwt_required
def consultar_unidad():
    session = Session()
    objeto_unidad = session.query(Unidad).all()

    schema = UnidadSchema(many=True)
    unidad = schema.dump(objeto_unidad)

    session.close()
    return jsonify(unidad)


@bp_unidad.route('/unidad/id', methods=['GET'])
@jwt_required
def consultar_unidad_id():
    nombre = request.args.get('nombre')
    session = Session()
    objeto_unidad = session.query(Unidad).get(nombre)

    schema = UnidadSchema()
    unidad = schema.dump(objeto_unidad)
    session.close()
    return jsonify(unidad)


@bp_unidad.route('/unidad', methods=['POST'])
@jwt_required
def agregar_unidad():
    # mount exam object
    posted_unidad = UnidadSchema(
        only=('nombre', 'encargado')) \
        .load(request.get_json())

    unidad = Unidad(**posted_unidad)

    # persist exam
    session = Session()
    session.add(unidad)
    session.commit()

    # return created exam
    nuevo_unidad = UnidadSchema().dump(unidad)
    session.close()
    return jsonify(nuevo_unidad), 201


@bp_unidad.route('/unidad/editar', methods=['POST'])
@jwt_required
def editar_unidad():
    posted_unidad = UnidadSchema(
        only=('nombre', 'encargado')) \
        .load(request.get_json())

    unidad_actualizado = Unidad(**posted_unidad)

    session = Session()
    objeto_unidad = session.query(Unidad).get(unidad_actualizado.nombre)
    if objeto_unidad is None:
        return "Unidad no encontrada", 404

    schema = UnidadSchema()

    objeto_unidad.encargado = unidad_actualizado.encargado

    session.add(objeto_unidad)
    session.commit()
    unidad = schema.dump(objeto_unidad)
    session.close()

    return jsonify(unidad)


@bp_unidad.route('/unidad', methods=['DELETE'])
@jwt_required
def eliminar_unidad():
    nombre = request.args.get('nombre')
    session = Session()
    objeto_unidad = session.query(Unidad).get(nombre)
    if objeto_unidad is None:
        return "Unidad no encontrada", 404

    session.delete(objeto_unidad)
    session.commit()

    session.close()
    return '', 200
