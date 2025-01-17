from odoo import models, fields

class persona(models.Model):
    _name = 'quintocargo.persona'
    _description = 'Persona'

    dni = fields.Char('DNI', required=True, help='Introduzca su DNI', size = 9)
    foto = fields.Binary('Foto', help='Introduzca su foto')
    nombre = fields.Char('Nombre', required=True, help='Introduzca su nombre', size = 25)
    apellidos = fields.Char('Apellidos', required=True, help='Introduzca sus apellidos', size = 50)
    direccion = fields.Char('Dirección', help='Introduzca su dirección', size = 60)
    telefono = fields.Integer('Teléfono', required=True, help='Introduzca su teléfono', digits = (9))
    email = fields.Char('Email', required=True, help='Introduzca su email', size = 50)
    fecha_nacimiento = fields.Date('Fecha de nacimiento', required=True, help='Introduzca su fecha de nacimiento')
    cuenta_corriente = fields.Char('Cuenta corriente', required=True, help='Introduzca su cuenta corriente', size = 24)

