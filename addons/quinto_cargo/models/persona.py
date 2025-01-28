import base64
from odoo import models, fields, api
from odoo import modules
from odoo.exceptions import ValidationError
import re
import uuid
from datetime import date

def get_default_img():
    with open(modules.get_module_resource('quinto_cargo', 'static/img', 'imagenPerfilPorDefecto.png'),
              'rb') as f:
        return base64.b64encode(f.read())

class persona(models.Model):
    _name = 'quintocargo.persona'
    _description = 'Persona'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    dni = fields.Char('DNI', required=True, help='Introduzca su DNI', size = 9)
    foto = fields.Binary('Foto', help='Introduzca su foto', required=True, default=get_default_img())
    nombre = fields.Char('Nombre', required=True, help='Introduzca su nombre', size = 25)
    apellidos = fields.Char('Apellidos', required=True, help='Introduzca sus apellidos', size = 50)
    direccion = fields.Char('Dirección', help='Introduzca su dirección', size=60)
    telefono = fields.Char('Teléfono', required=True, help='Introduzca su teléfono', size = 9)
    email = fields.Char('Email', required=True, help='Introduzca su email', size = 50)
    fecha_nacimiento = fields.Date('Fecha de nacimiento', required=True, help='Introduzca su fecha de nacimiento')
    cuenta_corriente = fields.Char('Cuenta corriente', required=True, help='Introduzca su cuenta corriente', size = 24)

    display_name = fields.Char(string="Nombre completo", compute="_compute_display_name", store=True)
    edad = fields.Integer(string="Edad", compute="_compute_age", store=True)
    total_mudanzas = fields.Integer(string="Número de Mudanzas", compute="_compute_total_mudanzas", store=True)

    # CÁLCULO DEL NOMBRE COMPLETO A PARTIR DEL NOMBRE Y APELLIDOS
    @api.depends('nombre', 'apellidos')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.nombre} {record.apellidos}"

    # CÁLCULO DE LA EDAD A PARTIR DE LA FECHA DE NACIMIENTO
    @api.depends('fecha_nacimiento')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                record.edad = today.year - record.fecha_nacimiento.year - (
                    (today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day)
                )
            else:
                record.edad = 0

    # VALIDACIÓN DEL TELÉFONO PARA QUE EMPIECE POR 6 O 7 Y TENGA 9 DÍGITOS
    @api.constrains('telefono')
    def _check_telefono(self):
        for record in self:
            if not re.fullmatch(r'[67]\d{8}$', record.telefono):
                raise ValidationError("El teléfono debe empezar por 6 o 7 y tener exactamente 9 dígitos.")

    # VALIDACIÓN DEL EMAIL PARA QUE TENGA EL FORMATO example@example.xxx
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,3}$', record.email):
                raise ValidationError("El email no tiene un formato válido (example@example.xxx).")

    # VALIDACIÓN DEL DNI
    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if not re.fullmatch(r'^\d{8}[A-Za-z]$', record.dni):
                raise ValidationError("El DNI debe tener 8 números seguidos de una letra (ej: 12345678A).")

    # VALIDACIÓN DE LA FECHA DE NACIMIENTO PARA QUE NO SEA EN EL FUTURO
    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento and record.fecha_nacimiento > date.today():
                raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")

    # VALIDACIÓN DE LA CUENTA CORRIENTE EN FORMATO ESPAÑOL
    @api.constrains('cuenta_corriente')
    def _check_cuenta_corriente(self):
        for record in self:
            if not re.fullmatch(r'^ES\d{22}$', record.cuenta_corriente):
                raise ValidationError("El número de cuenta debe seguir el formato IBAN español (ES + 22 dígitos).")
            
    # SQL CONSTRAINT PAR NO REPETIR LOS CAMPOS DNI, EMAIL Y TELEFONO
    _sql_constraints = [
        ('dni_unique', 'UNIQUE(dni)', 'El DNI debe ser único.'),
        ('email_unique', 'UNIQUE(email)', 'El email debe ser único.'),
        ('telefono_unique', 'UNIQUE(telefono)', 'El teléfono debe ser único.'),
    ]