from flask import Blueprint, make_response
from fpdf import FPDF
from src.pb.entities.regencia.reactivo import Reactivo, ReactivoSchema
from src.pb.entities.entity import Session


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
        self.cell(20, 8, "Inventario reactivos", 0, 0, 'C')

        self.set_font('Arial', '', 10)
        self.ln(10)
        self.set_x(95)
        self.cell(20, 8,
                  "________________________________________________________________________________________________",
                  0, 0, 'C')

        self.ln(10)

        self.set_font('Arial', 'B', 12)

        self.cell(0, 8, "REACTIVOS", 0, 0, 'L')
        self.ln(10)

        self.set_font('Arial', 'B', 12)

        width_cell = (20, 100, 25, 25, 25)

        self.set_x(10)
        self.cell(width_cell[0], 10, 'Estante', 1, 0, 'C')
        self.cell(width_cell[1], 10, 'Nombre', 1, 0, 'C')
        self.cell(width_cell[2], 10, 'Cantidad', 1, 0, 'C')
        self.cell(width_cell[3], 10, 'Estado', 1, 0, 'C')
        self.cell(width_cell[4], 10, 'Pureza', 1, 1, 'C')

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
        objeto_Reactivo = session.query(Reactivo).all()
        schema = ReactivoSchema(many=True)
        reactivos = schema.dump(objeto_Reactivo)

        width_cell = (20, 100, 25, 25, 25)

        self.set_font('Arial', '', 10)

        for reactivo in reactivos:
            self.set_x(10)
            self.cell(width_cell[0], 6, reactivo['estante'], 1, 0)
            self.cell(width_cell[1], 6, reactivo['nombre'], 1, 0)
            self.cell(width_cell[2], 6, str(reactivo['cantidad']), 1, 0)
            self.cell(width_cell[3], 6, reactivo['estado'], 1, 0)
            self.cell(width_cell[4], 6, reactivo['pureza'], 1, 0)
            self.ln(6)

        session.close()


bp_reporte_reactivo = Blueprint('bp_reporte_reactivo', __name__)


@bp_reporte_reactivo.route('/reactivo/reporte', methods=['GET'])
#@jwt_required
def create_pdf():
    pdf = CustomPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.Table()

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='ejemplo.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response