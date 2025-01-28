from odoo import models, fields, api
from odoo.exceptions import ValidationError

class empleado(models.Model):
    _inherit = 'quintocargo.persona'
    _name = 'quintocargo.empleado'
    _description = 'Empleado'

    cargo = fields.Selection([('director', 'Director'),
                              ('subdirector', 'Subdirector'),
                              ('jefe', 'Jefe'),
                              ('empleado', 'Empleado'),
                              ], 'Cargo', required=True, default = 'empleado')
    fecha_contratacion = fields.Date('Fecha de contratación', required=True)
    sueldo = fields.Float('Sueldo', required=True, digits = (10,2))
    horas_trabajadas = fields.Float('Horas trabajadas', required=True, digits = (5,2))
    mudanza_ids = fields.Many2many("quintocargo.mudanzas", "empleado_id", string="Mudanzas")

    # Definir la acción para abrir la vista de formulario en vista Kanban
    def action_open(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Empleado',
            'view_mode': 'form',
            'res_model': 'quintocargo.empleado',
            'res_id': self.id,
            'target': 'current',
        }
    
    # Definir la acción para eliminar un registro en vista Kanban
    def action_delete(self):
        for record in self:
            record.unlink()
        return {
        # Para cerrar la ventana emergente y recargar la pagina automaticamente
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

    # CÁLCULO DEL NÚMERO TOTAL DE MUDANZAS QUE HA HECHO UN EMPLEADO
    @api.depends('mudanza_ids')
    def _compute_total_mudanzas(self):
        for record in self:
            record.total_mudanzas = len(record.mudanza_ids)