from odoo import fields, models


class Etiqueta(models.Model):
    _name = "jcd_tareas.etiqueta"
    _description = "Etiqueta de tarea"
    _order = "name"

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("name_unique", "unique(name)", "Ya existe una etiqueta con ese nombre."),
    ]
