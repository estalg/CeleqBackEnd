from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...entities.vinculo_externo.analisisCotizacion import Analisis, AnalisisSchema, TipoMuestra, TipoMuestraSchema
from ...entities.entity import Session

bp_analisis = Blueprint('bp_analisis', __name__)


@bp_analisis.route('/analisis')
@jwt_required
def consultar_analisis():
    session = Session()
    objeto_analisis = session.query(Analisis).all()

    schema = AnalisisSchema(many=True)
    analisis = schema.dump(objeto_analisis)

    session.close()
    return jsonify(analisis)

@bp_analisis.route('/analisis/tipoMuestra')
@jwt_required
def consultar_analisis_tipoMuestra():
    tipoMuestra = request.args.get('tipoMuestra')
    session = Session()
    objeto_analisis = session.query(Analisis).filter_by(tipoMuestra=tipoMuestra).all()

    schema = AnalisisSchema(many=True)
    analisis = schema.dump(objeto_analisis)

    session.close()
    return jsonify(analisis)


@bp_analisis.route('/analisis/id', methods=['GET'])
@jwt_required
def consultar_analisis_id():
    descripcion = request.args.get('descripcion')
    tipoMuestra = request.args.get('tipoMuestra')
    session = Session()
    objeto_analisis = session.query(Analisis).get((descripcion, tipoMuestra))

    schema = AnalisisSchema()
    analisis = schema.dump(objeto_analisis)
    session.close()
    return jsonify(analisis)


@bp_analisis.route('/analisis', methods=['POST'])
@jwt_required
def agregar_analisis():
    # mount exam object
    posted_analisis = AnalisisSchema(only=('descripcion', 'tipoMuestra', 'metodo', 'precio', 'acreditacion')).load(
        request.get_json())

    analisis = Analisis(**posted_analisis)

    # persist exam
    session = Session()
    session.add(analisis)
    session.commit()

    # return created exam
    nuevo_analisis = AnalisisSchema().dump(analisis)
    session.close()
    return jsonify(nuevo_analisis), 201


@bp_analisis.route('/analisis/editar', methods=['POST'])
@jwt_required
def editar_analisis():
    posted_analisis = AnalisisSchema(only=('descripcion', 'tipoMuestra', 'metodo', 'precio', 'acreditacion')).load(
        request.get_json())

    analisis_actualizado = Analisis(**posted_analisis)

    session = Session()
    objeto_analisis = session.query(Analisis).get((analisis_actualizado.descripcion, analisis_actualizado.tipoMuestra))
    if objeto_analisis is None:
        return "Análisis no encontrado", 404

    schema = AnalisisSchema()

    objeto_analisis.metodo = analisis_actualizado.metodo
    objeto_analisis.precio = analisis_actualizado.precio
    objeto_analisis.acreditacion = analisis_actualizado.acreditacion

    session.add(objeto_analisis)
    session.commit()
    analisis = schema.dump(objeto_analisis)
    session.close()

    return jsonify(analisis)


@bp_analisis.route('/analisis', methods=['DELETE'])
@jwt_required
def eliminar_analisis():
    descripcion = request.args.get('descripcion')
    tipoMuestra = request.args.get('tipoMuestra')

    session = Session()
    objeto_analisis = session.query(Analisis).get((descripcion, tipoMuestra))
    if objeto_analisis is None:
        return "Análisis no encontrado", 404

    session.delete(objeto_analisis)
    session.commit()

    session.close()
    return '', 200

#TipoMuestra

@bp_analisis.route('/tipoMuestra')
@jwt_required
def consultar_tipoMuestra():
    session = Session()
    objeto_tipoMuestra = session.query(TipoMuestra).all()

    schema = TipoMuestraSchema(many=True)
    tipo = schema.dump(objeto_tipoMuestra)

    session.close()
    return jsonify(tipo)


@bp_analisis.route('/tipoMuestra/id', methods=['GET'])
@jwt_required
def consultar_tipoMuestra_id():
    tipo = request.args.get('tipo')
    session = Session()
    objeto_tipo = session.query(Analisis).get(tipo)

    schema = TipoMuestraSchema()
    tipoMuestra = schema.dump(objeto_tipo)
    session.close()
    return jsonify(tipoMuestra)


@bp_analisis.route('/tipoMuestra', methods=['POST'])
@jwt_required
def agregar_tipoMuestra():
    # mount exam object
    posted_tipoMuestra = TipoMuestraSchema().load(
        request.get_json())

    tipoMuestra = TipoMuestra(**posted_tipoMuestra)

    # persist exam
    session = Session()
    session.add(tipoMuestra)
    session.commit()

    # return created exam
    nuevo_tipoMuestra = TipoMuestraSchema().dump(tipoMuestra)
    session.close()
    return jsonify(nuevo_tipoMuestra), 201


@bp_analisis.route('/tipoMuestra', methods=['DELETE'])
@jwt_required
def eliminar_tipoMuestra():
    tipo = request.args.get('tipo')

    session = Session()
    objeto_tipoMuestra = session.query(TipoMuestra).get(tipo)
    if objeto_tipoMuestra is None:
        return "Tipo de muestra no encontrado", 404

    session.delete(objeto_tipoMuestra)
    session.commit()

    session.close()
    return '', 200
