from odoo import models, fields

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