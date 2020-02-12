from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...entities.vinculo_externo.feriados import Feriados, FeriadosSchema, SemanaSanta, SemanaSantaSchema
from ...entities.entity import Session
import dateutil.parser
import datetime

bp_feriados = Blueprint('bp_feriados', __name__)

@bp_feriados.route('/feriados')
@jwt_required
def consultar_Feriados():
    session = Session()
    objeto_Feriado = session.query(Feriados).all()

    schema = FeriadosSchema(many=True)
    feriados = schema.dump(objeto_Feriado)

    session.close()
    return jsonify(feriados)

@bp_feriados.route('/feriados/id', methods=['GET'])
@jwt_required
def consultar_feriado_id():
    id = request.args.get('id')
    session = Session()
    objeto_feriado = session.query(Feriados).get(id)

    schema = FeriadosSchema()
    feriado = schema.dump(objeto_feriado)
    session.close()
    return jsonify(feriado)

@bp_feriados.route('/feriados/SS', methods=['GET'])
@jwt_required
def consultar_semanaSanta_id():
    session = Session()
    objeto_feriado = session.query(SemanaSanta).first()

    schema = SemanaSantaSchema()
    feriado = schema.dump(objeto_feriado)
    session.close()
    return jsonify(feriado)

@bp_feriados.route('/feriados/semanaSanta', methods=['GET'])
@jwt_required
def consultar_semanaSanta():
    session = Session()
    objeto_Feriado = session.query(SemanaSanta).all()

    schema = SemanaSantaSchema(many=True)
    feriados = schema.dump(objeto_Feriado)

    session.close()
    return jsonify(feriados)

@bp_feriados.route('/feriados', methods=['POST'])
@jwt_required
def agregar_feriado():
    r = request.get_json()

    r['fecha'] = datetime.date(dateutil.parser.parse(r['fecha']).year, dateutil.parser.parse(r['fecha']).month, dateutil.parser.parse(r['fecha']).day).strftime('%Y-%m-%d')

    # mount exam object
    posted_feriado = FeriadosSchema(only=('descripcion', 'fecha')).load(r)
    posted_feriado['id'] = 0

    feriado = Feriados(**posted_feriado)

    # persist exam
    session = Session()
    session.add(feriado)
    session.commit()

    # return created exam
    #nuevo_feriado = FeriadosSchema().dump(feriado)
    session.close()
    return r, 201

@bp_feriados.route('/feriados/editar', methods=['POST'])
@jwt_required
def editar_feriado():
    r = request.get_json()

    r['fecha'] = datetime.date(dateutil.parser.parse(r['fecha']).year, dateutil.parser.parse(r['fecha']).month,
                               dateutil.parser.parse(r['fecha']).day).strftime('%Y-%m-%d')

    posted_feriado = FeriadosSchema(only=('id', 'descripcion', 'fecha')).load(r)

    feriado_actualizado = Feriados(**posted_feriado)

    session = Session()
    objeto_feriado = session.query(Feriados).get(feriado_actualizado.id)
    if objeto_feriado is None:
        return "Feriado no encontrado", 404

    schema = FeriadosSchema()

    objeto_feriado.descripcion = feriado_actualizado.descripcion
    objeto_feriado.fecha = feriado_actualizado.fecha

    session.add(objeto_feriado)
    session.commit()
    feriado = schema.dump(objeto_feriado)
    session.close()

    return jsonify(feriado)

@bp_feriados.route('/feriados/editarSS', methods=['POST'])
@jwt_required
def editar_semanaSanta():
    r = request.get_json()

    r['fechaInicio'] = datetime.date(dateutil.parser.parse(r['fechaInicio']).year,
                                     dateutil.parser.parse(r['fechaInicio']).month,
                                     dateutil.parser.parse(r['fechaInicio']).day).strftime('%Y-%m-%d')
    r['fechaFinal'] = datetime.date(dateutil.parser.parse(r['fechaFinal']).year,
                                     dateutil.parser.parse(r['fechaFinal']).month,
                                     dateutil.parser.parse(r['fechaFinal']).day).strftime('%Y-%m-%d')

    posted_feriado = SemanaSantaSchema(only=('id', 'descripcion', 'fechaInicio', 'fechaFinal')).load(r)

    feriado_actualizado = SemanaSanta(**posted_feriado)

    session = Session()
    objeto_feriado = session.query(SemanaSanta).first()
    if objeto_feriado is None:
        return "Feriado no encontrado", 404

    schema = SemanaSantaSchema()

    objeto_feriado.descripcion = feriado_actualizado.descripcion
    objeto_feriado.fechaInicio = feriado_actualizado.fechaInicio
    objeto_feriado.fechaFinal = feriado_actualizado.fechaFinal

    session.add(objeto_feriado)
    session.commit()
    feriado = schema.dump(objeto_feriado)
    session.close()

    return jsonify(feriado)

@bp_feriados.route('/feriados', methods=['DELETE'])
@jwt_required
def eliminar_feriado():
    id = request.args.get('id')
    session = Session()
    objeto_feriado = session.query(Feriados).get(id)
    if objeto_feriado is None:
        return "Feriado no encontrado", 404

    session.delete(objeto_feriado)
    session.commit()

    session.close()
    return '', 200