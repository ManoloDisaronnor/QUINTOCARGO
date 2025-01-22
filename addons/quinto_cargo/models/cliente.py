from odoo import models, fields

class cliente(models.Model):
    _inherit = 'quintocargo.persona'
    _name = 'quintocargo.cliente'
    _description = 'Cliente'

    tipoCliente  = fields.Selection([('particular', 'Particular'),
                                     ('empresa', 'Empresa')], 'Tipo de cliente', required=True, default = 'empresa')
    
    
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
            record.unlink()
        return {
        # Para cerrar la ventana emergente y recargar la pagina automaticamente
        'type': 'ir.actions.client',
        'tag': 'reload',
    }