from odoo import models, fields, api

class Tarea(models.Model):
    _name = 'jcd_tareas.tarea'
    _description = 'Tarea'

    name = fields.Char(string="Nombre", required=True)
    proyecto_id = fields.Many2one('jcd_tareas.jcd_proyecto', string="Proyecto", required=True)
    responsable_id = fields.Many2one('res.users', string="Responsable")
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('finalizada', 'Finalizada')
    ], string="Estado", default='pendiente')
    fecha_inicio = fields.Date(string="Fecha de Inicio")
    fecha_fin_estimada = fields.Date(string="Fecha de Fin Estimada", required=True)
    fecha_real_fin = fields.Date(string="Fecha de Finalización Real")
    descripcion = fields.Text(string="Descripción")
    notas = fields.Text(string="Notas")
    responsable_image = fields.Image(string="Imagen del Responsable", compute="_compute_responsable_image")
    comentario_ids = fields.One2many('jcd_tareas.tarea.comentario', 'tarea_id', string="Comentarios")
    etiqueta_ids = fields.Many2many('jcd_tareas.etiqueta', string='Etiquetas')

    @api.depends('responsable_id')
    def _compute_responsable_image(self):
        for tarea in self:
            tarea.responsable_image = tarea.responsable_id.image_1920 if tarea.responsable_id else False

