from odoo import models, fields, api

class Transporte(models.Model):
    _name = 'quintocargo.transporte'
    _description = 'Transporte'

    matricula = fields.Char(string='Matrícula', required=True)
    capacidad = fields.Float(string='Capacidad', required=True)
    tipo_vehiculo = fields.Selection([('camion', 'Camión'), ('furgoneta', 'Furgoneta')], string='Tipo de vehículo', required=True)
    fecha_compra = fields.Date(string='Fecha de compra', required=True)
    fecha_itv = fields.Date(string='Fecha de ITV', required=True)

    # Estado del transporte
    estado_transporte = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('en_uso', 'En Uso')
    ], string='Estado', default='disponible', required=True)

    # Relación con el modelo mudanza
    mudanza_ids = fields.Many2many('quintocargo.mudanzas', string='Mudanza asignada')

    # Función para comprobar si el transporte está en estado válido
    @api.constrains('fecha_itv')
    def _check_itv_validity(self):
        for record in self:
            if record.fecha_itv and record.fecha_itv < fields.Date.today():
                record.estado_transporte = 'en_mantenimiento'  # Cambiar el estado si la ITV está vencida
            else:
                # Si la ITV es válida, aseguramos que el estado sea 'disponible'
                if record.estado_transporte != 'en_uso':
                    record.estado_transporte = 'disponible'
