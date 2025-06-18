from odoo import models, fields

class Etiqueta(models.Model):
    _name = 'jcd_tareas.etiqueta'  
    _description = 'Etiqueta para Tareas'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Color', default=0)