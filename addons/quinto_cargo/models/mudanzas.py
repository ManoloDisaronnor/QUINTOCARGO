from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api


class Mudanzas(models.Model):
    _name = 'quintocargo.mudanzas'
    _description = 'Mudanzas'

    _rec_name = 'cod_mudanza'  # Usar 'cod_mudanza' en lugar del ID en los selectores

    cod_mudanza = fields.Integer('Código de mudanza', required=True, unique=True)
    nombre = fields.Char('Nombre', required=True)
    telefono = fields.Char('Teléfono', required=True)
    fecha_recogida = fields.Datetime('Fecha de recogida', required=True, default=fields.Datetime.now)
    fecha_entrega = fields.Datetime('Fecha de entrega', required=True, default=fields.Datetime.now)
    direccion_origen = fields.Char('Dirección de origen', required=True)
    direccion_destino = fields.Char('Dirección de destino', required=True)
    precio = fields.Float('Precio', required=True)   
    estado = fields.Selection([
                            ('pendiente', 'Pendiente'),
                            ('almacenado', 'Almacenado'),
                            ('finalizada', 'Finalizada'),], string='Estado', required=True, default='pendiente')
    metros_cubicos_usados = fields.Float('Metros cúbicos usados', required=True)
    comentario = fields.Char('Comentario')

    # Relación con el modelo almacen
    almacen_id = fields.Many2one("quintocargo.almacen",string="Almacen")
    empleado_ids = fields.Many2many("quintocargo.empleado", "mudanza_empleado_rel", "mudanza_id", "empleado_id", string="Empleados asignados")
    cliente_id = fields.Many2one("quintocargo.cliente",string="Cliente")
    bienes_ids = fields.One2many("quintocargo.bien_asegurado","mudanza_id",string="Bienes")
    
    @api.constrains('fecha_recogida', 'fecha_entrega')
    def _check_fechas(self):
        """ Valida que la fecha de recogida y entrega sean correctas """
        for record in self:
            now = fields.Datetime.now()
            
            # La fecha de recogida no puede ser anterior a la fecha actual
            if record.fecha_recogida < now:
                raise ValidationError("La fecha de recogida no puede estar en el pasado.")
            
            # La fecha de entrega no puede ser anterior a la fecha de recogida
            if record.fecha_entrega < record.fecha_recogida:
                raise ValidationError("La fecha de entrega no puede ser anterior a la fecha de recogida.")
        
    # Método para borrar mudanza SOLO SI ESTA FINALIZADA
    def action_borrar_mudanza(self):
        """ Borrar la mudanza seleccionada """
        for record in self:
            if record.estado != 'finalizada':
                raise ValidationError("Solo puedes eliminar mudanzas que estén en estado 'Finalizada'.")
            record.unlink()

    # Método para cambiar estado a 'finalizada'
    def action_finalizar_mudanza(self):
        """ Cambiar estado de la mudanza a 'finalizada' """
        for record in self:
            record.write({'estado': 'finalizada'})

    # Método para verificar si el cod_mudanza ya existe y si existe que no permita insertarlo
    @api.constrains('cod_mudanza')
    def _check_cod_mudanza(self):
        for record in self:
            existing_mudanza = self.search([
                ('cod_mudanza', '=', record.cod_mudanza),
                ('id', '!=', record.id)  # Excluye el propio registro si está editando
            ])
            if existing_mudanza:
                raise ValidationError(
                    "Ya existe una mudanza con el código %s. Por favor, ingrese un código diferente." % record.cod_mudanza
                )


    # Método para verificar que el almacen_id y el cliente_id estén seleccionados
    @api.constrains('almacen_id', 'cliente_id')
    def _check_almacen_cliente(self):
        for record in self:
            if not record.almacen_id:
                raise ValidationError("Debe seleccionar un almacén antes de crear la mudanza.")
            if not record.cliente_id:
                raise ValidationError("Debe seleccionar un cliente antes de crear la mudanza.")