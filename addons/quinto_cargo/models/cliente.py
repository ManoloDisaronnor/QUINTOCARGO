from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class cliente(models.Model):
    _inherit = 'quintocargo.persona'
    _name = 'quintocargo.cliente'
    _description = 'Cliente'

    tipoCliente  = fields.Selection([('particular', 'Particular'),
                                     ('empresa', 'Empresa')], 'Tipo de cliente', required=True, default = 'empresa')
    mudanza_ids = fields.One2many("quintocargo.mudanzas", "cliente_id", string="Mudanzas")
    
    
    # Definir la acción para abrir la vista de formulario en vista Kanban
    def action_open(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cliente',
            'view_mode': 'form',
            'res_model': 'quintocargo.cliente',
            'res_id': self.id,
            'target': 'current',
        }
    
    # Definir la acción para eliminar un registro en vista Kanban
    def action_delete(self):
        for record in self:
            # Verificar si existen mudanzas no finalizadas
            if record.mudanza_ids.filtered(lambda m: m.estado != 'finalizada'):
                raise UserError(_("No se puede eliminar el cliente porque tiene mudanzas pendientes o almacenadas."))
            record.unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    

    # RESTRICCIÓN PARA EVITAR INSERTAR MUDANZAS FINALIZADAS
    @api.onchange('mudanza_ids')
    def _onchange_mudanza_finalizada(self):
        for mudanza in self.mudanza_ids:
            if mudanza.estado == 'finalizada':
                self.mudanza_ids -= mudanza  # Elimina la selección de la mudanza "finalizada"
                return {
                    'warning': {
                        'title': "⚠️ No permitido",
                        'message': f'No puedes seleccionar la mudanza "{mudanza.nombre}" porque está finalizada.',
                        'type': 'warning',
                    }
                }

    # CÁLCULO DEL NÚMERO TOTAL DE MUDANZAS QUE HA HECHO UN CLIENTE
    @api.depends('mudanza_ids')
    def _compute_total_mudanzas(self):
        for record in self:
            record.total_mudanzas = len(record.mudanza_ids)