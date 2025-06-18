from odoo import models, fields

class Proyecto(models.Model):
    _name = 'jcd_tareas.jcd_proyecto'
    _description = 'Gestión de Proyecto'

    name = fields.Char(string="Nombre del Proyecto", required=True)
    prioridad = fields.Integer(string="Prioridad")
    coste = fields.Float(string="Coste Estimado")
    fecha_vencimiento = fields.Datetime(string="Fecha de Vencimiento")
    description = fields.Text(string="Descripción")
    activo = fields.Boolean(string="Proyecto Activo", default=True)
    tareas_ids = fields.One2many('jcd_tareas.tarea', 'proyecto_id', string="Tareas")
    image = fields.Image(string="Imagen Identificativa", help="Sube una imagen para identificar este proyecto")