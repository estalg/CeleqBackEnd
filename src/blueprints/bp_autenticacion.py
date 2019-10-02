from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity

from ..entities.entity import Session
from ..entities.usuario import Usuario, UsuarioSchema
from ..entities.usuariosgrupos import UsuariosGrupos
from ..entities.grupospermisos import GruposPermisos
import hashlib

bp_autenticacion = Blueprint('bp_autenticacion', __name__)

@bp_autenticacion.route('/login', methods=['POST'])
def login():
    posted_usuario = UsuarioSchema(only=('cedula', 'contrasenna')) \
        .load(request.get_json())

    contrasennaEncriptada = hashlib.sha1(posted_usuario['contrasenna'].encode())

    session = Session()
    usuario_base = session.query(Usuario).get(posted_usuario['cedula'])
    if usuario_base is None:
        session.close()
        return 'Usuario no existe', 404
    if usuario_base.contrasenna != contrasennaEncriptada.hexdigest():
        session.close()
        return 'Contraseña incorrecta', 406

    permisos = []

    grupos = session.query(UsuariosGrupos).filter_by(usuario=usuario_base.cedula).all()
    for grupo in grupos:
        permisosGrupos = session.query(GruposPermisos).filter_by(grupo=grupo.grupo).all()
        for permiso in permisosGrupos:
            if permiso not in permisos:
                permisos.append(permiso)

    for i in range(len(permisos)):
        permisos[i] = str(permisos[i].permiso)

    payload = {'cedula': usuario_base.cedula, 'correo': usuario_base.correo, 'telefono': usuario_base.telefono,
               'nombre': usuario_base.nombre, 'apellido1': usuario_base.apellido1, 'apellido2': usuario_base.apellido2,
               'permisos': permisos}

    access_token = create_access_token(identity=payload)
    refresh_token = create_refresh_token(identity=payload)

    return jsonify({'jwt': access_token, 'refreshToken': refresh_token}), 200

@bp_autenticacion.route('/login/refresh')
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return {'access_token': access_token}, 200