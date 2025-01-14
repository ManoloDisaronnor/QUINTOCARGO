from odoo import models, fields

class cliente(models.Model):
    _inherit = 'quintocargo.persona'
    _name = 'quintocargo.cliente'
    _description = 'Cliente'

    tipoCliente  = fields.Selection([('particular', 'Particular'),
                                     ('empresa', 'Empresa')], 'Tipo de cliente', required=True, default = 'empresa')