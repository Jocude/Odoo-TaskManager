from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RegistroTiempo(models.Model):
    """Parte de horas: tiempo dedicado por una persona a una tarea en un día."""

    _name = "jcd_tareas.registro_tiempo"
    _description = "Registro de tiempo"
    _order = "fecha desc, id desc"

    tarea_id = fields.Many2one("jcd_tareas.tarea", string="Tarea", required=True, ondelete="cascade")
    proyecto_id = fields.Many2one(related="tarea_id.proyecto_id", store=True, string="Proyecto")
    usuario_id = fields.Many2one("res.users", string="Usuario", required=True, default=lambda self: self.env.user)
    fecha = fields.Date(string="Fecha", required=True, default=fields.Date.context_today)
    horas = fields.Float(string="Horas", required=True)
    descripcion = fields.Char(string="Descripción")

    @api.constrains("horas")
    def _check_horas(self):
        for registro in self:
            if registro.horas <= 0 or registro.horas > 24:
                raise ValidationError("Las horas de un registro deben estar entre 0 y 24.")
