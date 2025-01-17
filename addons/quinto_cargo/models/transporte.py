
from odoo import models, fields, api

class transporte(models.Model):
    _name = 'quintocargo.transporte'
    _description = 'Transporte'

    matricula = fields.Char(string='Matrícula', required=True)
    capacidad = fields.Float(string='Capacidad', required=True)
    tipo_vehiculo = fields.Selection([ ('camion', 'Camión'), 
                                      ('furgoneta', 'Furgoneta'),], string='Tipo de vehículo', required=True)
    fecha_compra = fields.Date(string='Fecha de compra', required=True)
    fecha_itv = fields.Date(string='Fecha de ITV', required=True)