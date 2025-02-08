from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class Almacen(models.Model):
    _name = 'quintocargo.almacen'
    _description = 'Almacen'
    _rec_name = 'nombre'  # Usar 'nombre' en lugar del ID en los selectores
    
    nombre = fields.Char(string='Nombre', required=True)
    direccion = fields.Char(string='Dirección', required=True)
    capacidad = fields.Float(string='Capacidad', required=True, help='Capacidad en metros cúbicos')
    # Reflejamos la relación con mudanza para saber en el almacén que mudanzas hay guardadas
    mudanzas_ids = fields.One2many("quintocargo.mudanzas","almacen_id",string="Mudanzas")

    # Para que la capacidad no pueda ser negativo ni 0
    @api.constrains('capacidad')
    def _check_capacidad(self):
        for record in self:
            if record.capacidad <= 0:
                raise ValidationError("La capacidad del almacén debe ser mayor a 0.")

            
    # Para que un almacen no se pueda borrar si existen mudanzas asociadas
    @api.constrains('mudanzas_ids')
    def _check_mudanzas_asociadas(self):
        for record in self:
            if record.mudanzas_ids:
                raise ValidationError("No puedes eliminar un almacén que tenga mudanzas asociadas.")
            

    # Para que no se puedan superar los metros cúbicos disponibles 
    @api.constrains('mudanzas_ids')
    def _check_capacidad_disponible(self):
        for record in self:
            total_ocupado = sum(record.mudanzas_ids.mapped('metros_cubicos_usados'))
            if total_ocupado > record.capacidad:
                raise ValidationError("La capacidad del almacén ha sido excedida. Reduce el volumen de mudanzas.")