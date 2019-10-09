from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, desc

from ...entities.entity import Session
from ...entities.regimen_becario.designacion import Designacion, DesignacionSchema
from ...entities.umi.estudiante import Estudiante, EstudianteSchema
from ...entities.usuario import Usuario, UsuarioSchema
from ...entities.umi.p9 import P9, P9Schema
from ...entities.regimen_becario.arancel import Arancel, ArancelSchema

bp_designaciones = Blueprint('bp_designaciones', __name__)


@bp_designaciones.route('/designacion', methods=['GET'])
@jwt_required
def consultar_designaciones():
    session = Session()
    objeto_designacion = session.query(Designacion).all()

    schema = DesignacionSchema(many=True)
    designaciones = schema.dump(objeto_designacion)

    for designacion in designaciones:
        estudiante = session.query(Estudiante).get(designacion['idEstudiante'])
        responsable = session.query(Usuario).get(designacion['responsable'])
        designacion['nombre'] = estudiante.nombre
        designacion['apellido'] = estudiante.apellido1
        designacion['apellido2'] = estudiante.apellido2
        designacion['responsable'] = (responsable.nombre + ' ' + responsable.apellido1 + ' ' + responsable.apellido2)

    session.close()
    return jsonify(designaciones)


@bp_designaciones.route('/designacion/id', methods=['GET'])
@jwt_required
def consultar_designacion_id():
    id = request.args.get('id')
    anno = request.args.get('anno')

    session = Session()
    objeto_designacion = session.query(Designacion).get((id, anno))

    schema = DesignacionSchema(many=False)
    designacion = schema.dump(objeto_designacion)

    objeto_estudiante = session.query(Estudiante).get(designacion['idEstudiante'])
    objeto_responsable = session.query(Usuario).get(designacion['responsable'])
    objeto_p9 = session.query(P9).filter(P9.idDesignacion == designacion['id'],
                                         P9.annoDesignacion == designacion['anno']).order_by(desc(P9.fecha)).all()

    schema = UsuarioSchema(many=False)
    responsable = schema.dump(objeto_responsable)

    schema = EstudianteSchema(many=False)
    estudiante = schema.dump(objeto_estudiante)

    schema = P9Schema(many=False)
    p9 = schema.dump(objeto_p9[0])

    designacion['nombre'] = estudiante['nombre']
    designacion['apellido1'] = estudiante['apellido1']
    designacion['apellido2'] = estudiante['apellido2']

    designacion['responsable'] = (
                responsable['nombre'] + ' ' + responsable['apellido1'] + ' ' + responsable['apellido2'])

    designacion['numero'] = p9['numero']
    designacion['ubicacionArchivo'] = p9['ubicacionArchivo']
    designacion['idDesignacion'] = p9['idDesignacion']
    designacion['annoDesignacion'] = p9['annoDesignacion']
    designacion['fecha'] = p9['fecha']

    session.close()
    return jsonify(designacion)


@bp_designaciones.route('/designacion', methods=['POST'])
@jwt_required
def agregar_designacion():
    datos_designacion = request.get_json()

    datos_designacion['fecha'] = datos_designacion['fecha'].split('T')[0]
    datos_designacion['fechaInicio'] = datos_designacion['fechaInicio'].split('T')[0]
    datos_designacion['fechaFinal'] = datos_designacion['fechaFinal'].split('T')[0]

    session = Session()

    objeto_estudiante = session.query(Estudiante).get(datos_designacion['identificacion'])

    if objeto_estudiante is None:
        estudiante = Estudiante(datos_designacion['identificacion'], datos_designacion['tipoId'], datos_designacion['nombre'],
                                datos_designacion['apellido1'], datos_designacion['apellido2'], datos_designacion['correo'],
                                datos_designacion['celular'], datos_designacion['telefonoFijo'], datos_designacion['carrera'])

        session.add(estudiante)
    else:
        objeto_estudiante.nombre = datos_designacion['nombre']
        objeto_estudiante.apellido1 = datos_designacion['apellido1']
        objeto_estudiante.apellido2 = datos_designacion['apellido2']
        objeto_estudiante.correo = datos_designacion['correo']
        objeto_estudiante.celular = datos_designacion['celular']
        objeto_estudiante.telefonoFijo = datos_designacion['telefonoFijo']
        objeto_estudiante.carrera = datos_designacion['carrera']

        session.add(objeto_estudiante)

    objeto_arancel = session.query(Arancel).get(datos_designacion['modalidad'])
    schema = ArancelSchema()
    arancel = schema.dump(objeto_arancel)
    monto = arancel['monto'] * datos_designacion['horas']

    id = session.query(func.max(Designacion.id)).filter_by(anno=datos_designacion['anno']).first()[0]
    if id:
        id += 1
    else:
        id = 1

    designacion = Designacion(id, datos_designacion['anno'], datos_designacion['ciclo'], datos_designacion['fechaInicio'],
                              datos_designacion['fechaFinal'], datos_designacion['convocatoria'], datos_designacion['horas'],
                              datos_designacion['modalidad'], monto, datos_designacion['inopia'], datos_designacion['motivoInopia'],
                              datos_designacion['tramitado'], datos_designacion['observaciones'], datos_designacion['identificacion'],
                              datos_designacion['presupuesto'], datos_designacion['responsable'], datos_designacion['unidad'],
                              datos_designacion['adHonorem'])
    session.add(designacion)

    p9 = P9(datos_designacion['numero'], datos_designacion['ubicacionArchivo'], datos_designacion['id'], datos_designacion['anno'], datos_designacion['fecha'])

    session.add(p9)

    session.commit()

    schema = DesignacionSchema()
    objeto_designacion = schema.dump(designacion)

    session.close()

    return jsonify(objeto_designacion)

@bp_designaciones.route('/estudiantes', methods=['POST'])
@jwt_required
def consultar_estudiantes():
    session = Session()
    objeto_Estudiante = session.query(Estudiante).all()

    schema = EstudianteSchema(many=True)
    estudiantes = schema.dump(objeto_Estudiante)

    session.close()
    return jsonify(estudiantes)

@bp_designaciones.route('/designacion/editar', methods=['POST'])
#@jwt_required
def editar_designacion():
    datos_designacion = request.get_json()

    session = Session()
    objeto_designacion = session.query(Designacion).get((datos_designacion['id'], datos_designacion['anno']))
    if objeto_designacion is None:
        return "Designación no encontrada", 404

    schema = DesignacionSchema()

    objeto_designacion.responsable = datos_designacion['responsable']
    objeto_designacion.unidad = datos_designacion['unidad']
    objeto_designacion.horas = datos_designacion['horas']
    objeto_designacion.observaciones = datos_designacion['observaciones']
    objeto_designacion.tramitado = datos_designacion['tramitado']
    objeto_designacion.fechaFinal = datos_designacion['fechaFinal']

    session.add(objeto_designacion)

    designacion = schema.dump(objeto_designacion)

    p9 = session.query(P9).get(datos_designacion['numero'])

    if p9 is None:
        objeto_p9 = P9(datos_designacion['numero'], datos_designacion['ubicacionArchivo'], datos_designacion['id'], datos_designacion['anno'],
                       datos_designacion['fecha'])

    session.add(objeto_p9)

    session.commit()

    session.close()

    return jsonify(designacion)