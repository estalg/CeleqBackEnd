from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import requests
from datetime import date

bp_webService = Blueprint('bp_webService', __name__)

@bp_webService.route('/webService')
@jwt_required
def consultar_web_service():
    today = date.today()
    url = 'https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos?Indicador=317&FechaInicio=' + today.strftime("%d/%m/%Y") + '&FechaFinal=' + today.strftime("%d/%m/%Y") + '&Nombre=CELEQ&SubNiveles=N&CorreoElectronico=informatica.celeq@ucr.ac.cr&Token=8ACLRQEC0C'
    data = requests.get(url)
    contenido = data.content.decode('ascii')
    palabra_clave = '<NUM_VALOR>'
    s2 = contenido[contenido.index(palabra_clave)+11: contenido.index(palabra_clave) + 23]
    dolar = float(s2)
    return str(dolar), 200
