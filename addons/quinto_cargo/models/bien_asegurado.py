#-*-coding: utf-8-*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class bien_asegurado(models.Model):
    _name = 'quintocargo.bien_asegurado'
    _description = 'Bien Asegurado'
    
    nombre= fields.Char(string='Nombre', required=True)
    descripcion= fields.Text(string='Descripción')
    valor= fields.Float(string='Valor', required=True)
    tipo_bien= fields.Selection([('mueble', 'Mueble'), 
                                 ('electrodomestico', 'Electrodomestico'),
                                 ('arte', 'Arte'),
                                 ('inmueble', 'Inmueble')], 
                                string='Tipo de Bien', default='Mueble', required=True)
    
    peso= fields.Float(string='Peso', required=True)
    dimensiones_Alto= fields.Char(string='Dimensiones Alto', required=True)
    dimensiones_Ancho= fields.Char(string='Dimensiones Ancho', required=True)
    dimensiones_Largo= fields.Char(string='Dimensiones Largo', required=True)
    
    imagen = fields.Binary(string='Imagen')
    
    volumen = fields.Float(string='Volumen (cm³)', compute='_compute_volumen', store=True)

    

    # Relación con el modelo mudanza
    mudanza_id = fields.Many2one('quintocargo.mudanzas', string='Mudanza asignada')
    
    @api.constrains('peso', 'valor', 'dimensiones_Alto', 'dimensiones_Ancho', 'dimensiones_Largo')
    def _check_valores(self):
        for record in self:
            try:
                peso = float(record.peso)
                valor = float(record.valor)
                alto = float(record.dimensiones_Alto)
                ancho = float(record.dimensiones_Ancho)
                largo = float(record.dimensiones_Largo)

                if peso <= 0:
                    raise ValidationError("El peso debe ser mayor a 0.")
                if valor <= 0:
                    raise ValidationError("El valor debe ser mayor a 0.")
                if any(dim <= 0 for dim in [alto, ancho, largo]):
                    raise ValidationError("Las dimensiones deben ser mayores a 0.")
            except ValueError:
                raise ValidationError("Asegúrate de que todos los valores numéricos son correctos.")

    @api.depends('dimensiones_Alto', 'dimensiones_Ancho', 'dimensiones_Largo')
    def _compute_volumen(self):
        for record in self:
            try:
                alto = float(record.dimensiones_Alto or 0.0)
                ancho = float(record.dimensiones_Ancho or 0.0)
                largo = float(record.dimensiones_Largo or 0.0)
                record.volumen = alto * ancho * largo
            except (ValueError, TypeError):
                record.volumen = 0.0

    