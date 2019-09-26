from flask import Blueprint, jsonify, request
from ...entities.regencia.reactivo import Reactivo, ReactivoSchema
from ...entities.entity import Session

bp_reactivo = Blueprint('bp_reactivo', __name__)

@bp_reactivo.route('/reactivo')
def consultar_Reactivo():
    session = Session()
    objeto_reactivo = session.query(Reactivo).all()

    schema = ReactivoSchema(many=True)
    reactivo = schema.dump(objeto_reactivo)

    session.close()
    return jsonify(reactivo)

@bp_reactivo.route('/reactivo/id', methods=['GET'])
def consultar_reactivo_id():
    nombre = request.args.get('nombre')
    pureza = request.args.get('pureza')
    session = Session()
    objeto_reactivo = session.query(Reactivo).get((nombre,pureza))

    schema = ReactivoSchema()
    reactivo = schema.dump(objeto_reactivo)
    session.close()
    return jsonify(reactivo)

@bp_reactivo.route('/reactivo', methods=['POST'])
def agregar_reactivo():
    # mount exam object
    posted_reactivo = ReactivoSchema(only=('nombre', 'pureza', 'cantidad', 'estado', 'estante'))\
        .load(request.get_json())

    reactivo = Reactivo(**posted_reactivo)

    # persist exam
    session = Session()
    session.add(reactivo)
    session.commit()

    # return created exam
    nuevo_reactivo = ReactivoSchema().dump(reactivo)
    session.close()
    return jsonify(nuevo_reactivo), 201

@bp_reactivo.route('/reactivo/editar', methods=['POST'])
def editar_reactivo():
    posted_reactivo = ReactivoSchema(only=('nombre', 'pureza', 'cantidad', 'estado', 'estante'))\
        .load(request.get_json())

    reactivo_actualizado = Reactivo(**posted_reactivo)

    session = Session()
    objeto_reactivo = session.query(Reactivo).get((reactivo_actualizado.nombre, reactivo_actualizado.pureza))
    if objeto_reactivo is None:
        return "Reactivo no encontrado", 404

    schema = ReactivoSchema()

    objeto_reactivo.cantidad = reactivo_actualizado.cantidad
    objeto_reactivo.estado = reactivo_actualizado.estado
    objeto_reactivo.estante = reactivo_actualizado.estante

    session.add(objeto_reactivo)
    session.commit()
    reactivo = schema.dump(objeto_reactivo)
    session.close()

    return jsonify(reactivo)

@bp_reactivo.route('/reactivo', methods=['DELETE'])
def eliminar_cristaleria():
    nombre = request.args.get('nombre')
    pureza = request.args.get('pureza')
    session = Session()
    objeto_reactivo = session.query(Reactivo).get((nombre, pureza))
    if objeto_reactivo is None:
        return "Reactivo no encontrado", 404

    session.delete(objeto_reactivo)
    session.commit()

    session.close()
    return '', 200