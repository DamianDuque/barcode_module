from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import os
import base64
#import werkzeug

class Barcode(models.Model):
    _name = 'barcode.barcode'
    _description = 'Códigos de Barras'

    @api.model
    def generate_pdf_report(self, data):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_file_path = os.path.join(script_dir, "Uso_adecuado_de_los_codigos_de_barras.pdf")

        with open(pdf_file_path, "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")

        # Construct a temporary download link
        download_link = f"data:application/pdf;base64,{pdf_base64}"
        
        return download_link


    name = fields.Char(string='Nombre del Producto', required=False)
    barcode = fields.Char(string='Código de Barras', required=True)
    state = fields.Selection([
        ('asignado', 'Asignado'),
        ('pendiente', 'Pendiente'),
        ('sin_asignar', 'Sin Asignar')],
        string='Estado', default='pendiente')
    
    _sql_constraints = [
        ('barcode_uniq', 'UNIQUE (barcode)',  'Los codigos de barras deben ser unicos!')
    ]
    
    @api.constrains('barcode')
    def _check_number(self):
        number = self.barcode
        if len(number) != 13:
            raise ValidationError(('El codigo de barras debe ser de exactamente 13 cifras'))
        if not number.isnumeric():
            raise ValidationError(('El codigo de barras debe ser un numero'))
