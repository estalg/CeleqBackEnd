from flask import Blueprint, jsonify, request

from src.entities.usuariosgrupos import UsuariosGrupos, UsuariosGruposSchema
from ..entities.entity import Session
from ..entities.usuario import Usuario, UsuarioSchema
from flask_jwt_extended import jwt_required

bp_usuario = Blueprint('bp_usuarios', __name__)

@bp_usuario.route('/usuarios')
@jwt_required
def consultar_Usuario():
    session = Session()
    objeto_Usuario = session.query(Usuario).all()

    schema = UsuarioSchema(many=True)
    usuario = schema.dump(objeto_Usuario)

    session.close()
    return jsonify(usuario)

@bp_usuario.route('/usuarios/id', methods=['GET'])
@jwt_required
def consultar_usuario_id():
    cedula = request.args.get('cedula')
    session = Session()
    objeto_usuario = session.query(Usuario).get(cedula)

    schema = UsuarioSchema()
    usuario = schema.dump(objeto_usuario)
    session.close()
    return jsonify(usuario)

@bp_usuario.route('/usuarios', methods=['POST'])
@jwt_required
def agregar_usuario():
    # mount exam object
    posted_usuario = UsuarioSchema(only=('cedula', 'correo', 'telefono', 'nombre', 'apellido1', 'apellido2', 'contrasenna'))\
        .load(request.get_json())

    usuario = Usuario(**posted_usuario)

    # persist exam
    session = Session()
    session.add(usuario)
    session.commit()

    # return created exam
    nuevo_usuario = UsuarioSchema().dump(usuario)
    session.close()
    return jsonify(nuevo_usuario), 201

@bp_usuario.route('/usuarios/editar', methods=['POST'])
@jwt_required
def editar_usuario():
    posted_usuario = UsuarioSchema(only=('cedula', 'correo', 'telefono', 'nombre', 'apellido1', 'apellido2', 'contrasenna'))\
        .load(request.get_json())

    usuario_actualizado = Usuario(**posted_usuario)

    session = Session()
    objeto_usuario = session.query(Usuario).get(usuario_actualizado.cedula)
    if objeto_usuario is None:
        return "Usuario no encontrado", 404

    schema = UsuarioSchema()

    objeto_usuario.correo = usuario_actualizado.correo
    objeto_usuario.telefono = usuario_actualizado.telefono
    objeto_usuario.nombre = usuario_actualizado.nombre
    objeto_usuario.apellido1 = usuario_actualizado.apellido1
    objeto_usuario.apellido2 = usuario_actualizado.apellido2
    objeto_usuario.contrasenna = usuario_actualizado.contrasenna

    session.add(objeto_usuario)
    session.commit()
    usuario = schema.dump(objeto_usuario)
    session.close()

    return jsonify(usuario)

@bp_usuario.route('/usuarios', methods=['DELETE'])
@jwt_required
def eliminar_usuario():
    cedula = request.args.get('cedula')
    session = Session()
    objeto_usuario = session.query(Usuario).get(cedula)
    if objeto_usuario is None:
        return "Usuario no encontrado", 404

    session.delete(objeto_usuario)
    session.commit()

    session.close()
    return '', 200

@bp_usuario.route('/usuarios/grupos', methods=['GET'])
@jwt_required
def consultar_usuarios_grupos():
    grupo = request.args.get('grupo')
    session = Session()
    usuarios_base = session.query(Usuario).filter(Usuario.cedula == UsuariosGrupos.usuario).filter(UsuariosGrupos.grupo == grupo).all()

    schema = UsuarioSchema(many=True)
    usuarios = schema.dump(usuarios_base)

    session.close()
    return jsonify(usuarios), 200