from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api


class Mudanzas(models.Model):
    _name = 'quintocargo.mudanzas'
    _description = 'Mudanzas'

    _rec_name = 'cod_mudanza'  # Usar 'cod_mudanza' en lugar del ID en los selectores

    cod_mudanza = fields.Integer('Código de mudanza', required=True)
    nombre = fields.Char('Nombre', required=True)
    telefono = fields.Char('Teléfono', required=True)
    fecha_recogida = fields.Datetime('Fecha de recogida', required=True, default=fields.Datetime.now)
    fecha_entrega = fields.Datetime('Fecha de entrega', required=True, default=fields.Datetime.now)
    direccion_origen = fields.Char('Dirección de origen', required=True)
    direccion_destino = fields.Char('Dirección de destino', required=True)
    precio = fields.Float('Precio', required=True)   
    estado = fields.Selection([
                            ('pendiente', 'Pendiente'),
                            ('en_curso', 'En curso'),
                            ('almacenado', 'Almacenado'),
                            ('finalizada', 'Finalizada'),], string='Estado', required=True, default='pendiente')
    metros_cubicos_usados = fields.Float('Metros cúbicos usados', required=True)
    comentario = fields.Char('Comentario')

    # Relación con el modelo almacen
    almacen_id = fields.Many2one("quintocargo.almacen",string="Almacen")
    empleado_id = fields.Many2many("quintocargo.empleado",string="Empleados asignados")
    cliente_id = fields.Many2one("quintocargo.cliente",string="Cliente")
    bienes_ids = fields.One2many("quintocargo.bien_asegurado","mudanza_id",string="Bienes")
    
    @api.constrains('fecha_recogida', 'fecha_entrega')
    def _check_fechas(self):
        for record in self:
            if record.fecha_recogida and record.fecha_entrega:
                if record.fecha_recogida > record.fecha_entrega:
                    raise ValidationError(
                        "La fecha de recogida no puede ser posterior a la fecha de entrega. "
                        "Por favor, verifica las fechas ingresadas."
                    )
                if record.fecha_recogida < fields.Datetime.now() or record.fecha_entrega < fields.Datetime.now():
                    # Comprueba que ni la fecha de recogida ni la fecha de entrega sea posterior a la fecha actual
                    raise ValidationError(
                        "La fecha de recogida no puede estar en el pasado."
                    )
    
    # Método para borrar mudanza
    def action_borrar_mudanza(self):
        """ Borrar la mudanza seleccionada """
        for record in self:
            record.unlink()

    # Método para cambiar estado a 'finalizada'
    def action_finalizar_mudanza(self):
        """ Cambiar estado de la mudanza a 'finalizada' """
        for record in self:
            record.write({'estado': 'finalizada'})