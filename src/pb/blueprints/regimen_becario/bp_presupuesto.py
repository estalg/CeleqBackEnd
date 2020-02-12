from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ...entities.entity import Session
from ...entities.regimen_becario.presupuesto import Presupuesto, PresupuestoSchema

bp_presupuesto = Blueprint('bp_presupuesto', __name__)

@bp_presupuesto.route('/presupuesto')
@jwt_required
def consultar_Presupuesto():
    session = Session()
    objeto_presupuesto = session.query(Presupuesto).all()

    schema = PresupuestoSchema(many=True)
    presupuesto = schema.dump(objeto_presupuesto)

    session.close()
    return jsonify(presupuesto)

@bp_presupuesto.route('/presupuesto/id', methods=['GET'])
@jwt_required
def consultar_presupuesto_id():
    codigo = request.args.get('codigo')
    session = Session()
    objeto_presupuesto = session.query(Presupuesto).get(codigo)

    schema = PresupuestoSchema()
    presupuesto = schema.dump(objeto_presupuesto)
    session.close()
    return jsonify(presupuesto)

@bp_presupuesto.route('/presupuesto', methods=['POST'])
@jwt_required
def agregar_presupuesto():
    # mount exam object
    posted_presupuesto = PresupuestoSchema(only=('codigo', 'nombre'))\
        .load(request.get_json())

    presupuesto = Presupuesto(**posted_presupuesto)

    # persist exam
    session = Session()
    session.add(presupuesto)
    session.commit()

    # return created exam
    nuevo_presupuesto = PresupuestoSchema().dump(presupuesto)
    session.close()
    return jsonify(nuevo_presupuesto), 201

@bp_presupuesto.route('/presupuesto/editar', methods=['POST'])
@jwt_required
def editar_presupuesto():
    posted_presupuesto = PresupuestoSchema(only=('codigo', 'nombre'))\
        .load(request.get_json())

    presupuesto_actualizado = Presupuesto(**posted_presupuesto)

    session = Session()
    objeto_presupuesto = session.query(Presupuesto).get(presupuesto_actualizado.codigo)
    if objeto_presupuesto is None:
        return "Presupuesto no encontrado", 404

    schema = PresupuestoSchema()

    objeto_presupuesto.nombre = presupuesto_actualizado.nombre

    session.add(objeto_presupuesto)
    session.commit()
    presupuesto = schema.dump(objeto_presupuesto)
    session.close()

    return jsonify(presupuesto)

@bp_presupuesto.route('/presupuesto', methods=['DELETE'])
@jwt_required
def eliminar_presupuesto():
    codigo = request.args.get('codigo')
    session = Session()
    objeto_presupuesto = session.query(Presupuesto).get(codigo)
    if objeto_presupuesto is None:
        return "Presupuesto no encontrado", 404

    session.delete(objeto_presupuesto)
    session.commit()

    session.close()
    return '', 200
