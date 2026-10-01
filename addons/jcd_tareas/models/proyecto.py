from odoo import api, fields, models


class Proyecto(models.Model):
    _name = "jcd_tareas.proyecto"
    _description = "Proyecto"
    _order = "prioridad desc, fecha_vencimiento, name"

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(string="Activo", default=True)
    prioridad = fields.Selection(
        [("0", "Normal"), ("1", "Alta"), ("2", "Muy alta"), ("3", "Urgente")],
        string="Prioridad",
        default="0",
    )
    color = fields.Integer(string="Color")
    coste = fields.Float(string="Coste estimado")
    fecha_vencimiento = fields.Date(string="Fecha de vencimiento")
    descripcion = fields.Text(string="Descripción")
    image = fields.Image(string="Imagen", max_width=512, max_height=512)
    tarea_ids = fields.One2many("jcd_tareas.tarea", "proyecto_id", string="Tareas")

    tarea_count = fields.Integer(string="Nº de tareas", compute="_compute_resumen")
    progreso = fields.Float(string="Progreso", compute="_compute_resumen", help="Porcentaje de tareas finalizadas.")
    horas_estimadas = fields.Float(string="Horas estimadas", compute="_compute_resumen")
    horas_dedicadas = fields.Float(string="Horas dedicadas", compute="_compute_resumen")

    @api.depends("tarea_ids.estado", "tarea_ids.horas_estimadas", "tarea_ids.horas_dedicadas")
    def _compute_resumen(self):
        for proyecto in self:
            tareas = proyecto.tarea_ids
            finalizadas = tareas.filtered(lambda t: t.estado == "finalizada")
            proyecto.tarea_count = len(tareas)
            proyecto.progreso = 100.0 * len(finalizadas) / len(tareas) if tareas else 0.0
            proyecto.horas_estimadas = sum(tareas.mapped("horas_estimadas"))
            proyecto.horas_dedicadas = sum(tareas.mapped("horas_dedicadas"))

    def action_ver_tareas(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Tareas de {self.name}",
            "res_model": "jcd_tareas.tarea",
            "view_mode": "kanban,tree,form,calendar",
            "domain": [("proyecto_id", "=", self.id)],
            "context": {"default_proyecto_id": self.id},
        }
