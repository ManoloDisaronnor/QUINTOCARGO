from odoo import models, fields

class Mudanzas(models.Model):
    _name = 'quintocargo.mudanzas'
    _description = 'Mudanzas'

    cod_mudanza = fields.Integer('Código de mudanza', required=True)
    nombre = fields.Char('Nombre', required=True)
    telefono = fields.Char('Teléfono', required=True)
    fecha_recogida = fields.Datetime('Fecha de recogida', required=True)
    fecha_entrega = fields.Datetime('Fecha de entrega', required=True)
    direccion_origen = fields.Char('Dirección de origen', required=True)
    direccion_destino = fields.Char('Dirección de destino', required=True)
    precio = fields.Float('Precio', required=True)   
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En curso'),
        ('finalizada', 'Finalizada'),
    ], string='Estado', required=True, default='pendiente')
    metros_cubicos_usados = fields.Float('Metros cúbicos usados', required=True)

    # Relación con el modelo almacen
    almacen_id = fields.Many2one("quintocargo.almacen",string="Almacen")
    empleado_id = fields.Many2many("quintocargo.empleado",string="Empleados asignados")
    # cliente_id = fields.Many2one("quintocargo.cliente",string="Cliente")
    bienes_ids = fields.One2many("quintocargo.bien_asegurado","mudanza_id",string="Bienes")
    