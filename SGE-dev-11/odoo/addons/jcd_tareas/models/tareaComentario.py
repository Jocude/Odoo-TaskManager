from odoo import models, fields
class TareaComentario(models.Model):
    _name = 'jcd_tareas.tarea.comentario'
    _description = 'Comentario de Tarea'

    tarea_id = fields.Many2one('jcd_tareas.tarea', string="Tarea", required=True)
    comentario = fields.Text(string="Comentario", required=True)
    autor_id = fields.Many2one('res.users', string="Autor", default=lambda self: self.env.user)
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now)