from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from pb.entities.regencia.cristaleria import Cristaleria, CristaleriaSchema
from pb.entities.entity import Session

bp_cristaleria = Blueprint('bp_cristaleria', __name__)

@bp_cristaleria.route('/cristaleria')
@jwt_required
def consultar_Cristaleria():
    session = Session()
    objeto_Cristaleria = session.query(Cristaleria).all()

    schema = CristaleriaSchema(many=True)
    cristaleria = schema.dump(objeto_Cristaleria)

    session.close()
    return jsonify(cristaleria)

@bp_cristaleria.route('/cristaleria/id', methods=['GET'])
@jwt_required
def consultar_cristaleria_id():
    nombre = request.args.get('nombre')
    material = request.args.get('material')
    capacidad = request.args.get('capacidad')
    session = Session()
    objeto_cristaleria = session.query(Cristaleria).get((nombre,material,capacidad))

    schema = CristaleriaSchema()
    cristaleria = schema.dump(objeto_cristaleria)
    session.close()
    return jsonify(cristaleria)

@bp_cristaleria.route('/cristaleria', methods=['POST'])
@jwt_required
def agregar_cristaleria():
    # mount exam object
    posted_cristaleria = CristaleriaSchema(only=('nombre', 'material', 'capacidad', 'cantidad', 'caja'))\
        .load(request.get_json())

    cristaleria = Cristaleria(**posted_cristaleria)

    # persist exam
    session = Session()
    session.add(cristaleria)
    session.commit()

    # return created exam
    nueva_cristaleria = CristaleriaSchema().dump(cristaleria)
    session.close()
    return jsonify(nueva_cristaleria), 201

@bp_cristaleria.route('/cristaleria/editar', methods=['POST'])
@jwt_required
def editar_cristaleria():
    posted_cristaleria = CristaleriaSchema(only=('nombre', 'material', 'capacidad', 'cantidad', 'caja'))\
        .load(request.get_json())

    cristaleria_actualizada = Cristaleria(**posted_cristaleria)

    session = Session()
    objeto_cristaleria = session.query(Cristaleria).get((cristaleria_actualizada.nombre, cristaleria_actualizada.material, cristaleria_actualizada.capacidad))
    if objeto_cristaleria is None:
        return "Cristalería no encontrada", 404

    schema = CristaleriaSchema()

    objeto_cristaleria.cantidad = cristaleria_actualizada.cantidad
    objeto_cristaleria.caja = cristaleria_actualizada.caja

    session.add(objeto_cristaleria)
    session.commit()
    cristaleria = schema.dump(objeto_cristaleria)
    session.close()

    return jsonify(cristaleria)

@bp_cristaleria.route('/cristaleria', methods=['DELETE'])
@jwt_required
def eliminar_cristaleria():
    nombre = request.args.get('nombre')
    material = request.args.get('material')
    capacidad = request.args.get('capacidad')
    session = Session()
    objeto_cristaleria = session.query(Cristaleria).get((nombre, material, capacidad))
    if objeto_cristaleria is None:
        return "Cristalería no encontrada", 404

    session.delete(objeto_cristaleria)
    session.commit()

    session.close()
    return '', 200