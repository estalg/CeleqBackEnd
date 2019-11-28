from flask import Blueprint, request, make_response
from fpdf import FPDF
from src.pb.entities.regimen_becario.designacion import Designacion, DesignacionSchema
from src.pb.entities.umi.estudiante import Estudiante, EstudianteSchema
from src.pb.entities.usuario import Usuario, UsuarioSchema
from src.pb.entities.unidad import Unidad, UnidadSchema
from src.pb.entities.entity import Session
from src.pb.entities.umi.p9 import P9, P9Schema
from src.pb.entities.regimen_becario.arancel import Arancel, ArancelSchema
from datetime import date


class CustomPDF(FPDF):
    ciclo = ''
    anno = ''

    def header(self):
        # self.add_font('Arial', 'B', 'arial.php')
        self.set_font('Arial', 'B', 12)
        # $this->Image('../../Logos/LogoUcr.png', 10, 8, 33);
        # $this->Image('../../Logos/LogoCeleq.gif', 180, 10, 20);

        self.set_y(13)
        self.set_x(95)

        self.cell(20, 8, "UNIVERSIDAD DE COSTA RICA", 0, 0, 'C')

        self.ln(5)
        self.set_x(95)
        self.cell(20, 8, "CENTRO DE ELECTROQUÍMICA Y ENERGÍA QUÍMICA", 0, 0, 'C')

        self.set_font('Arial', 'B', 14)
        self.ln(6)
        self.set_x(95)
        self.cell(20, 8, "Designación estudiante", 0, 0, 'C')

        self.ln(6)
        self.set_x(95)
        self.cell(20, 8, self.ciclo + ' ciclo de ' + self.anno, 0, 0, 'C')

        self.set_font('Arial', '', 10)
        self.ln(10)
        self.set_x(95)
        self.cell(20, 8,
                  "________________________________________________________________________________________________",
                  0, 0, 'C')

        self.ln(6)

    def footer(self):
        self.set_font('Arial', '', 8)
        self.set_y(-25)
        self.multi_cell(140, 7,
                        "Este documento es propiedad del CELEQ. Se prohíbe la reproducción o distribución sin previa\n"
                        "autorización.",
                        1, 'C', 0, False)
        self.set_y(-25)
        self.set_x(150)
        today = date.today()
        self.multi_cell(50, 7, "Fecha de impresión\n" + today.strftime("%d/%m/%Y"), 1, 'C')

    def Table(self, tipo, anno, ciclo):
        session = Session()

        if tipo == 'estudiante':
            objeto_Designacion = session.query(Designacion).filter(Designacion.anno == anno,
                                                                   Designacion.ciclo == ciclo).group_by(
                Designacion.idEstudiante).all()
            schema = DesignacionSchema(many=True)
            designaciones = schema.dump(objeto_Designacion)

            self.set_font('Arial', '', 10)

            for designacion in designaciones:
                self.add_page('P')
                objeto_estudiante = session.query(Estudiante).get(designacion['idEstudiante'])
                schema = EstudianteSchema()
                estudiante = schema.dump(objeto_estudiante)

                objeto_Designacion2 = session.query(Designacion).filter(
                    Designacion.idEstudiante == estudiante['identificacion'], Designacion.anno == anno,
                    Designacion.ciclo == ciclo).all()
                schema = DesignacionSchema(many=True)
                designaciones2 = schema.dump(objeto_Designacion2)

                self.set_x(60)
                self.cell(20, 8,
                          "Estudiante: " + estudiante['nombre'] + ' ' + estudiante['apellido1'] + ' ' + estudiante[
                              'apellido2'], 0, 0, 'C')
                self.set_x(130)
                self.cell(10, 8, "Identificación: " + estudiante['identificacion'], 0, 0, 'C')
                self.ln(2)
                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(1)
                self.set_x(10)
                self.multi_cell(185, 6,
                                "Por este medio se le notifica que para el actual ciclo lectivo se ha procedido a realizarle las siguientes"
                                " designaciones. Se le recuerda su obligación de cumplir con las obligaciones establecidas en la Reglamentación"
                                " Universitaria vigente, así como en las directrices propias del CELEQ, que se transcriben al final de "
                                "este documento.", 0, 0, 'C')
                self.ln(1)
                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(3)

                width_cell = (20, 25, 25, 25, 25, 50)

                self.set_x(10)
                self.cell(width_cell[0], 10, 'Modalidad', 1, 0, 'C')
                self.cell(width_cell[1], 10, 'Horas', 1, 0, 'C')
                self.cell(width_cell[2], 10, 'Presupuesto', 1, 0, 'C')
                self.cell(width_cell[3], 10, 'Inicio', 1, 0, 'C')
                self.cell(width_cell[4], 10, 'Final', 1, 0, 'C')
                self.cell(width_cell[5], 10, 'Profesor/Funcionario', 1, 1, 'C')

                for designacion2 in designaciones2:
                    objeto_responsable = session.query(Usuario).get(designacion2['responsable'])
                    schema = UsuarioSchema()
                    responsable = schema.dump(objeto_responsable)
                    self.set_x(10)
                    self.cell(width_cell[0], 6, designacion2['modalidad'], 1, 0)
                    self.cell(width_cell[1], 6, str(designacion2['horas']), 1, 0)
                    self.cell(width_cell[2], 6, designacion2['presupuesto'], 1, 0)
                    self.cell(width_cell[3], 6, designacion2['fechaInicio'], 1, 0)
                    self.cell(width_cell[4], 6, designacion2['fechaFinal'], 1, 0)
                    self.cell(width_cell[5], 6,
                              responsable['nombre'] + ' ' + responsable['apellido1'] + ' ' + responsable['apellido2'],
                              1, 1)
                self.ln(2)

                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(2)

                self.set_x(10)
                self.cell(50, 6, "Obligaciones de los estudiantes:", 0, 0, 'L')
                self.ln(10)

                self.set_x(10)
                self.cell(180, 6,
                          "1. Cumplir con el horario acordado con el profesor o funcionario responsable y con el número total de horas",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "semanales de la designación, para lo cual se deben reportar en la Recepción del Centro a la entrada y salida.",
                          0, 1, 'L')

                self.set_x(10)
                self.cell(180, 6,
                          "2. Realizar de forma responsable las labores y funciones que le han sido asignadas.",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "3. Para los estudiantes que realicen horas en un laboratorio, es imprescindible cumplir siempre con las ",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "medidas de seguridad establecidas: uso de gabacha, lentes de seguridad, zapatos cerrados y otras de",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "acuerdo a las funciones que se le han asignado.",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 8,
                          "De igual forma, nunca permanecer solo en uno de los laboratorios, sin la adecuada supervición de un ",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "responsable.",
                          0, 1, 'L')

                self.set_x(10)
                self.cell(180, 6,
                          "4. Velar por el adecuado uso de los equipos Universitarios y en caso de desperfecto o rotura, comunicarlo de",
                          0, 1, 'L')
                self.set_x(10)
                self.cell(180, 6,
                          "inmediato al responsable.",
                          0, 1, 'L')

                self.set_x(10)
                self.cell(180, 6,
                          "5. Portar siempre en lugar visible, el gafete de identificación. El incumplimiento de este requisito significará su",
                          0, 1, 'L')
                self.cell(180, 6,
                          "retirada del edificio.",
                          0, 1, 'L')
                self.cell(180, 6,
                          "6. No permitir el ingreso a las instalaciones del CELEQ, de personas ajenas al Centro, sin antes contar con",
                          0, 1, 'L')
                self.cell(180, 6,
                          "la debida autorización.",
                          0, 1, 'L')
                self.cell(180, 6,
                          "7. Al finalizar la designación, entregar en la Recepción del Centro, el correspondiente informe de ",
                          0, 1, 'L')
                self.cell(180, 6,
                          "cumplimiento de funciones, con el visto bueno del profesor o funcionario responsable.",
                          0, 1, 'L')

        elif tipo == 'responsable':
            objeto_Designacion = session.query(Designacion).filter(Designacion.anno == anno,
                                                                   Designacion.ciclo == ciclo).group_by(
                Designacion.responsable).all()
            schema = DesignacionSchema(many=True)
            designaciones = schema.dump(objeto_Designacion)

            self.set_font('Arial', '', 10)

            for designacion in designaciones:
                self.add_page('P')
                objeto_responsable = session.query(Usuario).get(designacion['responsable'])
                schema = UsuarioSchema()
                responsable = schema.dump(objeto_responsable)

                objeto_Designacion2 = session.query(Designacion).filter(
                    Designacion.responsable == responsable['cedula'], Designacion.anno == anno,
                    Designacion.ciclo == ciclo).all()
                schema = DesignacionSchema(many=True)
                designaciones2 = schema.dump(objeto_Designacion2)

                objeto_unidad = session.query(Unidad).filter(Unidad.encargado == responsable['cedula']).first()
                schema = UnidadSchema()
                unidad = schema.dump(objeto_unidad)

                self.set_x(60)
                self.cell(20, 8,
                          "Responsable: " + responsable['nombre'] + ' ' + responsable['apellido1'] + ' ' + responsable[
                              'apellido2'], 0, 0, 'C')
                self.set_x(130)
                self.cell(10, 8, "Unidad o Laboratorio: " + designacion['unidad'], 0, 0, 'C')
                self.ln(2)
                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(1)
                self.set_x(10)
                self.multi_cell(185, 6,
                                "Por este medio se le notifica que para el actual ciclo lectivo se ha procedido a realizar las designaciones"
                                " de estudiante abajo detalladas. Se le recuerda su obligación de velar por el cumplimiento de las horas de "
                                "cada uno de los estudiantes, así como de las obligaciones para las cuales fueron designados. Así mismo, se reitera"
                                " la obligatoriedad de entregar un informe del trabajo realizado por los estudiantes, una vez finalice el semestre.",
                                0, 0, 'C')
                self.ln(1)
                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(3)

                width_cell = (60, 25, 25, 25, 25)

                self.set_x(25)
                self.cell(width_cell[0], 10, 'Estudiante', 1, 0, 'C')
                self.cell(width_cell[1], 10, 'Identificación', 1, 0, 'C')
                self.cell(width_cell[2], 10, 'Modalidad', 1, 0, 'C')
                self.cell(width_cell[3], 10, 'Horas', 1, 0, 'C')
                self.cell(width_cell[4], 10, 'Presupuesto', 1, 1, 'C')

                for designacion2 in designaciones2:
                    objeto_estudiante = session.query(Estudiante).get(designacion2['idEstudiante'])
                    schema = EstudianteSchema()
                    estudiante = schema.dump(objeto_estudiante)
                    self.set_x(25)
                    self.cell(width_cell[0], 6,
                              estudiante['nombre'] + ' ' + estudiante['apellido1'] + ' ' + estudiante['apellido2'], 1,
                              0)
                    self.cell(width_cell[1], 6, designacion2['idEstudiante'], 1, 0)
                    self.cell(width_cell[2], 6, designacion2['modalidad'], 1, 0)
                    self.cell(width_cell[3], 6, str(designacion2['horas']), 1, 0)
                    self.cell(width_cell[4], 6, designacion2['presupuesto'], 1, 1)

                self.ln(2)
        elif tipo == 'presupuesto':
            self.add_page()
            objeto_Designacion = session.query(Designacion).filter(Designacion.anno == anno,
                                                                   Designacion.ciclo == ciclo).group_by(
                Designacion.presupuesto).all()
            schema = DesignacionSchema(many=True)
            designaciones = schema.dump(objeto_Designacion)

            self.set_font('Arial', '', 10)

            for designacion in designaciones:
                objeto_Designacion2 = session.query(Designacion).filter(
                    Designacion.presupuesto == designacion['presupuesto'], Designacion.anno == anno,
                    Designacion.ciclo == ciclo).distinct(Designacion.presupuesto).group_by(
                    Designacion.presupuesto).all()
                schema = DesignacionSchema(many=True)
                designaciones2 = schema.dump(objeto_Designacion2)

                self.cell(0, 8,
                          "Presupuesto: " + designacion['presupuesto'], 0, 0, 'C')
                self.ln(2)
                self.set_x(95)
                self.cell(20, 8,
                          "________________________________________________________________________________________________",
                          0, 1, 'C')
                self.ln(1)

                for designacion2 in designaciones2:
                    objeto_Designacion3 = session.query(Designacion).filter(Designacion.anno == anno,
                                                                            Designacion.ciclo == ciclo,
                                                                            Designacion.presupuesto == designacion2[
                                                                                'presupuesto']).group_by(
                        Designacion.modalidad)
                    schema = DesignacionSchema(many=True)
                    designaciones3 = schema.dump(objeto_Designacion3)

                    for designacion3 in designaciones3:
                        objeto_Designacion4 = session.query(Designacion).filter(Designacion.anno == anno,
                                                                                Designacion.ciclo == ciclo,
                                                                                Designacion.presupuesto == designacion3[
                                                                                    'presupuesto'],
                                                                                Designacion.modalidad == designacion3[
                                                                                    'modalidad']).distinct(
                            Designacion.modalidad).all()
                        schema = DesignacionSchema(many=True)
                        designaciones4 = schema.dump(objeto_Designacion4)

                        width_cell = (45, 22, 18, 11, 22, 45, 18, 18)

                        self.set_x(6)
                        self.cell(width_cell[0], 10, 'Estudiante', 1, 0, 'C')
                        self.cell(width_cell[1], 10, 'Identificación', 1, 0, 'C')
                        self.cell(width_cell[2], 10, 'Modalidad', 1, 0, 'C')
                        self.cell(width_cell[3], 10, 'Horas', 1, 0, 'C')
                        self.cell(width_cell[4], 10, 'Presupuesto', 1, 0, 'C')
                        self.cell(width_cell[5], 10, 'Responsable', 1, 0, 'C')
                        self.cell(width_cell[6], 10, 'Unidad', 1, 0, 'C')
                        self.cell(width_cell[7], 10, 'P9/SHA', 1, 1, 'C')

                        totalHoras = 0

                        for designacion4 in designaciones4:
                            objeto_estudiante = session.query(Estudiante).get(designacion4['idEstudiante'])
                            schema = EstudianteSchema()
                            estudiante = schema.dump(objeto_estudiante)

                            objeto_responsable = session.query(Usuario).get(designacion4['responsable'])
                            schema = UsuarioSchema()
                            responsable = schema.dump(objeto_responsable)

                            objeto_unidad = session.query(Unidad).filter(
                                Unidad.encargado == responsable['cedula']).first()
                            schema = UnidadSchema()
                            unidad = schema.dump(objeto_unidad)

                            objeto_p9 = session.query(P9).filter(P9.idDesignacion == designacion4['id'],
                                                                 P9.annoDesignacion == designacion4['anno']).first()
                            schema = P9Schema()
                            p9 = schema.dump(objeto_p9)

                            self.set_x(6)
                            self.cell(width_cell[0], 6,
                                      estudiante['nombre'] + ' ' + estudiante['apellido1'] + ' ' + estudiante[
                                          'apellido2'], 1, 0)
                            self.cell(width_cell[1], 6, designacion4['idEstudiante'], 1, 0)
                            self.cell(width_cell[2], 6, designacion4['modalidad'], 1, 0)
                            self.cell(width_cell[3], 6, str(designacion4['horas']), 1, 0)
                            self.cell(width_cell[4], 6, designacion2['presupuesto'], 1, 0)
                            self.cell(width_cell[5], 6,
                                      responsable['nombre'] + ' ' + responsable['apellido1'] + ' ' + responsable[
                                          'apellido2'], 1, 0)
                            self.cell(width_cell[6], 6, designacion4['unidad'], 1, 0)
                            self.cell(width_cell[7], 6, p9['numero'], 1, 1)

                            totalHoras += designacion4['horas']

                        self.ln(2)
                        self.set_x(85)
                        precioHora = session.query(Arancel).get(designacion3['modalidad'])
                        schema = ArancelSchema()
                        precio = schema.dump(precioHora)
                        self.cell(width_cell[0], 10,
                                  '| TOTAL HORAS: ' + str(totalHoras) + ' | COSTO TOTAL X MES: ' + str(
                                      precio['monto'] * totalHoras) + ' |', 0, 0, 'C')
                        self.ln(13)

                self.ln(2)

        session.close()


bp_reporte_designaciones = Blueprint('bp_reporte_designaciones', __name__)


@bp_reporte_designaciones.route('/designacion/reporte', methods=['GET'])
# @jwt_required
def create_pdf():
    tipo = request.args.get('tipo')
    anno = request.args.get('anno')
    ciclo = request.args.get('ciclo')
    pdf = CustomPDF()
    pdf.ciclo = ciclo
    pdf.anno = anno
    pdf.alias_nb_pages()

    pdf.Table(tipo, anno, ciclo)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    if tipo == 'estudiante':
        response.headers.set('Content-Disposition', 'attachment',
                             filename='reporte_designacion_estudiante_' + anno + '_' + ciclo + '.pdf')
    elif tipo == 'responsable':
        response.headers.set('Content-Disposition', 'attachment',
                             filename='reporte_designacion_responsable_' + anno + '_' + ciclo + '.pdf')
    else:
        response.headers.set('Content-Disposition', 'attachment',
                             filename='reporte_designacion_presupuesto_' + anno + '_' + ciclo + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response
