from flask import Blueprint, jsonify, request

from src.pb.entities.entity import Session
from src.pb.entities.grupo import Grupo, GruposSchema
from src.pb.entities.permisos import Permisos, PermisosSchema
from src.pb.entities.grupospermisos import GruposPermisos, GruposPermisosSchema
from src.pb.entities.usuariosgrupos import UsuariosGrupos
from src.pb.entities.usuario import Usuario, UsuarioSchema
from flask_jwt_extended import jwt_required

bp_grupos = Blueprint('bp_grupos', __name__)


@bp_grupos.route('/grupos', methods=['GET'])
@jwt_required
def consultar_grupos():
    session = Session()
    objeto_grupos = session.query(Grupo).all()

    schema = GruposSchema(many=True)
    grupos = schema.dump(objeto_grupos)

    session.close()
    return jsonify(grupos), 200


@bp_grupos.route('/grupos/permisos', methods=['GET'])
@jwt_required
def consultar_permisos():
    session = Session()
    objeto_permisos = session.query(Permisos).all()

    schema = PermisosSchema(many=True)
    permisos = schema.dump(objeto_permisos)

    session.close()
    return jsonify(permisos), 200


@bp_grupos.route('/grupos/permisosgrupo', methods=['GET'])
@jwt_required
def consultar_permisos_grupo():
    grupo = request.args.get('grupo')
    session = Session()
    objeto_permisos = session.query(GruposPermisos).filter_by(grupo=grupo).all()

    schema = GruposPermisosSchema(many=True)
    permisos = schema.dump(objeto_permisos)

    session.close()
    return jsonify(permisos), 200


@bp_grupos.route('/grupos/usuarios', methods=['GET'])
@jwt_required
def consultar_usuarios_grupo():
    grupo = request.args.get('grupo')
    session = Session()
    objeto_usuarios_grupo = session.query(UsuariosGrupos).filter_by(grupo=grupo).all()

    objeto_usuarios = []

    for usuario_grupo in objeto_usuarios_grupo:
        usuario = session.query(Usuario).get(usuario_grupo.usuario)
        objeto_usuarios.append(usuario)

    schema = UsuarioSchema(many=True)
    usuarios = schema.dump(objeto_usuarios)
    session.close()
    return jsonify(usuarios), 200


@bp_grupos.route('/grupos', methods=['POST'])
@jwt_required
def agregar_grupo():
    data = request.get_json()
    grupo = Grupo(data['descripcion'])
    session = Session()
    session.add(grupo)
    session.commit()

    permisos = data['permisos']
    for permiso in permisos:
        grupo_permiso = GruposPermisos(grupo.descripcion, permiso['id'])
        session.add(grupo_permiso)

    session.commit()
    session.close()
    return '', 200


@bp_grupos.route('/grupos/editar', methods=['POST'])
@jwt_required
def editar_grupo():
    data = request.get_json()
    grupo = Grupo(data['descripcion']).descripcion
    session = Session()
    permisos_anteriores = session.query(GruposPermisos).filter_by(grupo=grupo).all()
    for permiso in permisos_anteriores:
        session.delete(permiso)

    permisos = data['permisos']
    for permiso in permisos:
        grupo_permiso = GruposPermisos(grupo, permiso['id'])
        session.add(grupo_permiso)

    session.commit()
    session.close()
    return '', 200


@bp_grupos.route('/grupos', methods=['DELETE'])
@jwt_required
def eliminar_grupo():
    descripcion = request.args.get('descripcion')
    session = Session()
    permisos = session.query(GruposPermisos).filter_by(grupo=descripcion).all()
    for permiso in permisos:
        session.delete(permiso)

    grupo = session.query(Grupo).get(descripcion)
    session.delete(grupo)
    session.commit()
    session.close()
    return '', 200


@bp_grupos.route('/grupos/asignarusuario', methods=['POST'])
@jwt_required
def asignar_usuario_grupo():
    data = request.get_json()
    grupo = data['descripcion']
    session = Session()
    usuarios = session.query(UsuariosGrupos).filter_by(grupo=grupo).all()
    for usuario in usuarios:
        session.delete(usuario)

    usuarios = data['usuarios']
    for usuario in usuarios:
        usuario_grupo = UsuariosGrupos(usuario['cedula'], grupo)
        session.add(usuario_grupo)

    session.commit()
    session.close()
    return '', 200