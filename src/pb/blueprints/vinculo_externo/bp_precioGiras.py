from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ...entities.entity import Session
from ...entities.vinculo_externo.precioGiras import precioGiras, precioGirasSchema

bp_precioGiras = Blueprint('bp_precioGiras', __name__)

@bp_precioGiras.route('/precioGiras')
@jwt_required
def consultar_precio():
    session = Session()
    objeto_precio = session.query(precioGiras).all()

    schema = precioGirasSchema(many=True)
    precio = schema.dump(objeto_precio)

    session.close()
    return jsonify(precio)

@bp_precioGiras.route('/precioGiras', methods=['POST'])
@jwt_required
def agregar_precio():
    # mount exam object
    posted_precio = precioGirasSchema(only=('variable', 'valor')).load(request.get_json())

    precio = precioGiras(**posted_precio)

    # persist exam
    session = Session()
    session.add(precio)
    session.commit()

    # return created exam
    nuevo_precio = precioGirasSchema().dump(precio)
    session.close()
    return jsonify(nuevo_precio), 201

@bp_precioGiras.route('/precioGiras/editar', methods=['POST'])
@jwt_required
def editar_precio():
    posted_precio = precioGirasSchema(only=('variable', 'valor')).load(request.get_json())

    precio_actualizado = precioGiras(**posted_precio)

    session = Session()
    objeto_precio = session.query(precioGiras).get(precio_actualizado.variable)
    if objeto_precio is None:
        return "Precio de gira no encontrado", 404

    schema = precioGirasSchema()

    objeto_precio.valor = precio_actualizado.valor

    session.add(objeto_precio)
    session.commit()
    precio = schema.dump(objeto_precio)
    session.close()

    return jsonify(precio)

@bp_precioGiras.route('/precioGiras', methods=['DELETE'])
@jwt_required
def eliminar_precio():
    variable = request.args.get('variable')
    session = Session()
    objeto_precio = session.query(precioGiras).get(variable)
    if objeto_precio is None:
        return "Precio de giras no encontrado", 404

    session.delete(objeto_precio)
    session.commit()

    session.close()
    return '', 200