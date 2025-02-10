from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Almacen(models.Model):
    _name = 'quintocargo.almacen'
    _description = 'Almacen'
    _rec_name = 'nombre'  # Usar 'nombre' en lugar del ID en los selectores
    
    nombre = fields.Char(string='Nombre', required=True)
    direccion = fields.Char(string='Dirección', required=True)
    capacidad = fields.Float(string='Capacidad', required=True, help='Capacidad en metros cúbicos')
    
    # Relación con mudanza
    mudanzas_ids = fields.One2many("quintocargo.mudanzas", "almacen_id", string="Mudanzas")

    # Campo funcional para mostrar la capacidad disponible
    capacidad_disponible = fields.Float(
        string="Capacidad Disponible", 
        compute="_compute_capacidad_disponible", 
        store=True
    )

    @api.depends('mudanzas_ids', 'mudanzas_ids.metros_cubicos_usados', 'capacidad')
    def _compute_capacidad_disponible(self):
        for record in self:
            total_ocupado = sum(record.mudanzas_ids.mapped('metros_cubicos_usados'))
            record.capacidad_disponible = record.capacidad - total_ocupado

    # Restricción: la capacidad no puede ser negativa ni cero
    @api.constrains('capacidad')
    def _check_capacidad(self):
        for record in self:
            if record.capacidad <= 0:
                raise ValidationError("La capacidad del almacén debe ser mayor a 0.")

    # Restricción: no se puede eliminar un almacén con mudanzas asociadas
    @api.constrains('mudanzas_ids')
    def _check_mudanzas_asociadas(self):
        for record in self:
            if record.mudanzas_ids:
                raise ValidationError("No puedes eliminar un almacén que tenga mudanzas asociadas.")
            
    # Restricción: no se pueden superar los metros cúbicos disponibles 
    @api.constrains('mudanzas_ids')
    def _check_capacidad_disponible(self):
        for record in self:
            total_ocupado = sum(record.mudanzas_ids.mapped('metros_cubicos_usados'))
            if total_ocupado > record.capacidad:
                raise ValidationError("La capacidad del almacén ha sido excedida. Reduce el volumen de mudanzas.")
