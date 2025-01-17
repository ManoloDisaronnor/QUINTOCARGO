#-*-coding: utf-8-*-

from odoo import models, fields

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

    # Relación con el modelo mudanza
    # mudanza_id = fields.Many2one('quintocargo.mudanzas', string='Mudanza asignada')