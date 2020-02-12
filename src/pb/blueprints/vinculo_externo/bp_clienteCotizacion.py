from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...entities.vinculo_externo.clienteCotizacion import clienteCotizacion, clienteCotizacionSchema
from ...entities.entity import Session

bp_clienteCotizacion = Blueprint('bp_clienteCotizacion', __name__)


@bp_clienteCotizacion.route('/clientes')
@jwt_required
def consultar_clientes():
    session = Session()
    objeto_cliente = session.query(clienteCotizacion).all()

    schema = clienteCotizacionSchema(many=True)
    clientes = schema.dump(objeto_cliente)

    session.close()
    return jsonify(clientes)


@bp_clienteCotizacion.route('/clientes/id', methods=['GET'])
@jwt_required
def consultar_cliente_id():
    nombre = request.args.get('nombre')
    session = Session()
    objeto_cliente = session.query(clienteCotizacion).get(nombre)

    schema = clienteCotizacionSchema()
    cliente = schema.dump(objeto_cliente)
    session.close()
    return jsonify(cliente)


@bp_clienteCotizacion.route('/clientes', methods=['POST'])
@jwt_required
def agregar_cliente():
    # mount exam object
    posted_cliente = clienteCotizacionSchema(
        only=('nombre', 'telefono', 'telefono2', 'correo', 'fax', 'direccion', 'persona_trae_muestra', 'contacto')).load(request.get_json())

    cliente = clienteCotizacion(**posted_cliente)

    # persist exam
    session = Session()
    session.add(cliente)
    session.commit()

    # return created exam
    nuevo_cliente = clienteCotizacionSchema().dump(cliente)
    session.close()
    return jsonify(nuevo_cliente), 201


@bp_clienteCotizacion.route('/clientes/editar', methods=['POST'])
@jwt_required
def editar_cliente():
    nombreViejo = request.args.get('nombreViejo')
    posted_cliente = clienteCotizacionSchema(
        only=('nombre', 'telefono', 'telefono2', 'correo', 'fax', 'direccion', 'persona_trae_muestra', 'contacto')).load(request.get_json())

    cliente_actualizado = clienteCotizacion(**posted_cliente)

    session = Session()
    objeto_cliente = session.query(clienteCotizacion).get(nombreViejo)
    if objeto_cliente is None:
        return "Cliente no encontrado", 404

    schema = clienteCotizacionSchema()

    objeto_cliente.nombre = cliente_actualizado.nombre
    objeto_cliente.telefono = cliente_actualizado.telefono
    objeto_cliente.telefono2 = cliente_actualizado.telefono2
    objeto_cliente.correo = cliente_actualizado.correo
    objeto_cliente.fax = cliente_actualizado.fax
    objeto_cliente.direccion = cliente_actualizado.direccion
    objeto_cliente.persona_trae_muestra = cliente_actualizado.persona_trae_muestra
    objeto_cliente.contacto = cliente_actualizado.contacto

    session.add(objeto_cliente)
    session.commit()
    cliente = schema.dump(objeto_cliente)
    session.close()

    return jsonify(cliente)
