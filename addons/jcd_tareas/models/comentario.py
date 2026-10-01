from odoo import fields, models


class Comentario(models.Model):
    _name = "jcd_tareas.comentario"
    _description = "Comentario de tarea"
    _order = "fecha desc, id desc"

    tarea_id = fields.Many2one("jcd_tareas.tarea", string="Tarea", required=True, ondelete="cascade")
    comentario = fields.Text(string="Comentario", required=True)
    autor_id = fields.Many2one(
        "res.users", string="Autor", required=True, readonly=True, default=lambda self: self.env.user
    )
    fecha = fields.Datetime(string="Fecha", required=True, readonly=True, default=fields.Datetime.now)
