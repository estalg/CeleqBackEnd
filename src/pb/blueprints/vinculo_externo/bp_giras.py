from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ...entities.vinculo_externo.giras import Giras, GirasSchema
from ...entities.entity import Session

bp_giras = Blueprint('bp_giras', __name__)

@bp_giras.route('/giras', methods=['POST'])
@jwt_required
def agregar_gira():
    posted_gira = GirasSchema(only=('provincia', 'canton', 'localidad', 'cantidadTecnicos', 'cantidadProfesionales', 'nochesAlojamiento',
                                    'horasMuestreo', 'gastoTotal', 'idCotizacion', 'annoCotizacion')).load(request.get_json())
    posted_gira['id'] = 0

    gira = Giras(**posted_gira)

    # persist exam
    session = Session()
    session.add(gira)
    session.commit()

    # return created exam
    nueva_gira = GirasSchema().dump(gira)
    session.close()
    return nueva_gira, 201

@bp_giras.route('/giras/cotizacion')
@jwt_required
def consultar_Gira_cotizacion():
    idCotizacion = request.args.get('idCotizacion')
    annoCotizacion = request.args.get('annoCotizacion')

    session = Session()
    objeto_Gira = session.query(Giras).filter_by(idCotizacion=idCotizacion,annoCotizacion=annoCotizacion).first()

    schema = GirasSchema(many=False)
    gira = schema.dump(objeto_Gira)

    session.close()
    return jsonify(gira)