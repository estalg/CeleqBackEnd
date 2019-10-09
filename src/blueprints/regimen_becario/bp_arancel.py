from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.entities.entity import Session
from ...entities.regimen_becario.arancel import Arancel, ArancelSchema

bp_arancel = Blueprint('bp_arancel', __name__)

@bp_arancel.route('/arancel')
@jwt_required
def consultar_Arancel():
    session = Session()
    objeto_arancel = session.query(Arancel).all()

    schema = ArancelSchema(many=True)
    arancel = schema.dump(objeto_arancel)

    session.close()
    return jsonify(arancel)

@bp_arancel.route('/arancel/id', methods=['GET'])
@jwt_required
def consultar_arancel_id():
    tipo = request.args.get('tipo')
    session = Session()
    objeto_arancel = session.query(Arancel).get(tipo)

    schema = ArancelSchema()
    arancel = schema.dump(objeto_arancel)
    session.close()
    return jsonify(arancel)

@bp_arancel.route('/arancel', methods=['POST'])
@jwt_required
def agregar_arancel():
    # mount exam object
    posted_arancel = ArancelSchema(only=('tipo', 'monto'))\
        .load(request.get_json())

    arancel = Arancel(**posted_arancel)

    # persist exam
    session = Session()
    session.add(arancel)
    session.commit()

    # return created exam
    nuevo_arancel = ArancelSchema().dump(arancel)
    session.close()
    return jsonify(nuevo_arancel), 201

@bp_arancel.route('/arancel/editar', methods=['POST'])
@jwt_required
def editar_arancel():
    posted_arancel = ArancelSchema(only=('tipo', 'monto'))\
        .load(request.get_json())

    arancel_actualizado = Arancel(**posted_arancel)

    session = Session()
    objeto_arancel = session.query(Arancel).get(arancel_actualizado.tipo)
    if objeto_arancel is None:
        return "Arancel no encontrado", 404

    schema = ArancelSchema()

    objeto_arancel.monto = arancel_actualizado.monto

    session.add(objeto_arancel)
    session.commit()
    arancel = schema.dump(objeto_arancel)
    session.close()

    return jsonify(arancel)

@bp_arancel.route('/arancel', methods=['DELETE'])
@jwt_required
def eliminar_arancel():
    tipo = request.args.get('tipo')
    session = Session()
    objeto_arancel = session.query(Arancel).get(tipo)
    if objeto_arancel is None:
        return "Arancel no encontrado", 404

    session.delete(objeto_arancel)
    session.commit()

    session.close()
    return '', 200

