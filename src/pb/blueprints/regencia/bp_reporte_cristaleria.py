from flask import Blueprint, make_response
from fpdf import FPDF
from ...entities.regencia.cristaleria import Cristaleria, CristaleriaSchema
from ...entities.entity import Session
from flask_jwt_extended import jwt_required


class CustomPDF(FPDF):

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
        self.cell(20, 8, "Inventario cristalería", 0, 0, 'C')

        self.set_font('Arial', '', 10)
        self.ln(10)
        self.set_x(95)
        self.cell(20, 8,
                  "________________________________________________________________________________________________",
                  0, 0, 'C')

        self.ln(10)

        self.set_font('Arial', 'B', 12)

        self.cell(0, 8, "CRISTALERÍA", 0, 0, 'L')
        self.ln(10)

        self.set_font('Arial', 'B', 12)

        width_cell = (20, 100, 25, 25, 25)

        self.set_x(10)
        self.cell(width_cell[0], 10, 'Caja', 1, 0, 'C')
        self.cell(width_cell[1], 10, 'Artículo', 1, 0, 'C')
        self.cell(width_cell[2], 10, 'Cantidad', 1, 0, 'C')
        self.cell(width_cell[3], 10, 'Capacidad', 1, 0, 'C')
        self.cell(width_cell[4], 10, 'Material', 1, 1, 'C')

    def footer(self):
        self.set_font('Arial', '', 8)
        self.set_y(-25)

        self.cell(0, 8,
                  "Este documento es propiedad del CELEQ. Se prohíbe la reproducción o distribución sin previa autorización.",
                  0, 0, 'C')
        self.ln(5)

        self.cell(0, 8, "Favor confirmar su vigencia antes de hacer uso de esta versión, por si ha sido modificado.", 0,
                  0, 'C')
        self.ln(5)

        self.cell(0, 10, "Página " + str(self.page_no()) +
                  '/{nb}', 0, 0, 'C')

    def Table(self):
        session = Session()
        objeto_Cristaleria = session.query(Cristaleria).all()
        schema = CristaleriaSchema(many=True)
        cristalerias = schema.dump(objeto_Cristaleria)

        width_cell = (20, 100, 25, 25, 25)

        self.set_font('Arial', '', 10)

        for cristaleria in cristalerias:
            self.set_x(10)
            self.cell(width_cell[0], 6, cristaleria['caja'], 1, 0)
            self.cell(width_cell[1], 6, cristaleria['nombre'], 1, 0)
            self.cell(width_cell[2], 6, str(cristaleria['cantidad']), 1, 0)
            self.cell(width_cell[3], 6, cristaleria['capacidad'], 1, 0)
            self.cell(width_cell[4], 6, cristaleria['material'], 1, 0)
            self.ln(6)

        session.close()


bp_reporte_cristaleria = Blueprint('bp_reporte_cristaleria', __name__)


@bp_reporte_cristaleria.route('/cristaleria/reporte', methods=['GET'])
#@jwt_required
def create_pdf():
    pdf = CustomPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.Table()

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='reporte_cristaleria.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response
