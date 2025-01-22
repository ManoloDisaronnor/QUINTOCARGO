from odoo import models, fields

class Almacen(models.Model):
    _name = 'quintocargo.almacen'
    _description = 'Almacen'
    _rec_name = 'nombre'  # Usar 'nombre' en lugar del ID en los selectores
    
    nombre = fields.Char(string='Nombre', required=True)
    direccion = fields.Char(string='Dirección', required=True)
    capacidad = fields.Float(string='Capacidad', required=True, help='Capacidad en metros cúbicos')

    # Reflejamos la relación con mudanza para saber en el almacén que mudanzas hay guardadas
    mudanzas_ids = fields.One2many("quintocargo.mudanzas","almacen_id",string="Mudanzas")