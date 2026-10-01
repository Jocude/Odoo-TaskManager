from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

ESTADOS = [
    ("pendiente", "Pendiente"),
    ("en_progreso", "En progreso"),
    ("finalizada", "Finalizada"),
]


class Tarea(models.Model):
    _name = "jcd_tareas.tarea"
    _description = "Tarea"
    _order = "prioridad desc, fecha_fin_estimada, id"

    name = fields.Char(string="Nombre", required=True)
    active = fields.Boolean(string="Activa", default=True)
    proyecto_id = fields.Many2one(
        "jcd_tareas.proyecto", string="Proyecto", required=True, ondelete="cascade", index=True
    )
    responsable_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user, index=True)
    prioridad = fields.Selection(
        [("0", "Normal"), ("1", "Alta"), ("2", "Muy alta"), ("3", "Urgente")],
        string="Prioridad",
        default="0",
    )
    estado = fields.Selection(
        ESTADOS, string="Estado", default="pendiente", required=True, group_expand="_expand_estados"
    )
    etiqueta_ids = fields.Many2many("jcd_tareas.etiqueta", string="Etiquetas")
    color = fields.Integer(string="Color")

    # Fechas
    fecha_inicio = fields.Date(string="Fecha de inicio")
    fecha_fin_estimada = fields.Date(string="Fecha de fin estimada", required=True)
    fecha_real_fin = fields.Date(
        string="Fecha de fin real", readonly=True, help="Se rellena sola al finalizar la tarea."
    )
    retrasada = fields.Boolean(string="Retrasada", compute="_compute_retrasada", search="_search_retrasada")

    descripcion = fields.Text(string="Descripción")
    notas = fields.Text(string="Notas")
    comentario_ids = fields.One2many("jcd_tareas.comentario", "tarea_id", string="Comentarios")

    # Tiempo
    horas_estimadas = fields.Float(string="Horas estimadas")
    registro_ids = fields.One2many("jcd_tareas.registro_tiempo", "tarea_id", string="Registros de tiempo")
    horas_dedicadas = fields.Float(string="Horas dedicadas", compute="_compute_horas", store=True)
    progreso = fields.Float(
        string="Progreso",
        compute="_compute_horas",
        store=True,
        help="Horas dedicadas respecto a las estimadas (máximo 100 %).",
    )

    # Dependencias
    depende_de_ids = fields.Many2many(
        "jcd_tareas.tarea",
        "jcd_tareas_tarea_dependencia_rel",
        "tarea_id",
        "depende_de_id",
        string="Depende de",
        help="Tareas que tienen que estar finalizadas antes de poder finalizar esta.",
    )
    bloquea_ids = fields.Many2many(
        "jcd_tareas.tarea",
        "jcd_tareas_tarea_dependencia_rel",
        "depende_de_id",
        "tarea_id",
        string="Bloquea a",
    )
    bloqueada = fields.Boolean(
        string="Bloqueada",
        compute="_compute_bloqueada",
        help="Alguna de las tareas de las que depende aún no está finalizada.",
    )

    # --- Cálculos ---

    @api.model
    def _expand_estados(self, estados, domain, order):
        """Muestra siempre las tres columnas en el kanban, aunque alguna esté vacía."""
        return [clave for clave, _ in ESTADOS]

    @api.depends("fecha_fin_estimada", "estado")
    def _compute_retrasada(self):
        hoy = fields.Date.context_today(self)
        for tarea in self:
            tarea.retrasada = (
                tarea.estado != "finalizada" and bool(tarea.fecha_fin_estimada) and tarea.fecha_fin_estimada < hoy
            )

    def _search_retrasada(self, operator, value):
        if operator not in ("=", "!="):
            raise UserError("Operación no soportada para el campo «Retrasada».")
        hoy = fields.Date.context_today(self)
        dominio = [("estado", "!=", "finalizada"), ("fecha_fin_estimada", "<", hoy)]
        buscar_retrasadas = (operator == "=") == bool(value)
        return dominio if buscar_retrasadas else ["!", "&", *dominio]

    @api.depends("registro_ids.horas", "horas_estimadas")
    def _compute_horas(self):
        for tarea in self:
            tarea.horas_dedicadas = sum(tarea.registro_ids.mapped("horas"))
            if tarea.horas_estimadas:
                tarea.progreso = min(100.0, 100.0 * tarea.horas_dedicadas / tarea.horas_estimadas)
            else:
                tarea.progreso = 0.0

    @api.depends("depende_de_ids.estado")
    def _compute_bloqueada(self):
        for tarea in self:
            tarea.bloqueada = any(d.estado != "finalizada" for d in tarea.depende_de_ids)

    # --- Validaciones ---

    @api.constrains("fecha_inicio", "fecha_fin_estimada")
    def _check_fechas(self):
        for tarea in self:
            if tarea.fecha_inicio and tarea.fecha_fin_estimada and tarea.fecha_fin_estimada < tarea.fecha_inicio:
                raise ValidationError("La fecha de fin estimada no puede ser anterior a la de inicio.")

    @api.constrains("horas_estimadas")
    def _check_horas_estimadas(self):
        if any(tarea.horas_estimadas < 0 for tarea in self):
            raise ValidationError("Las horas estimadas no pueden ser negativas.")

    @api.constrains("depende_de_ids")
    def _check_dependencias(self):
        for tarea in self:
            if tarea in tarea.depende_de_ids:
                raise ValidationError("Una tarea no puede depender de sí misma.")
        if not self._check_m2m_recursion("depende_de_ids"):
            raise ValidationError("Las dependencias forman un ciclo: ninguna de esas tareas podría finalizarse.")

    @api.constrains("estado", "depende_de_ids")
    def _check_finalizar_bloqueada(self):
        for tarea in self:
            if tarea.estado == "finalizada" and tarea.bloqueada:
                pendientes = ", ".join(tarea.depende_de_ids.filtered(lambda d: d.estado != "finalizada").mapped("name"))
                raise ValidationError(f"No se puede finalizar «{tarea.name}»: antes hay que terminar {pendientes}.")

    # --- Fecha de fin real automática ---

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("estado") == "finalizada" and not vals.get("fecha_real_fin"):
                vals["fecha_real_fin"] = fields.Date.context_today(self)
        return super().create(vals_list)

    def write(self, vals):
        if "estado" in vals and "fecha_real_fin" not in vals:
            if vals["estado"] == "finalizada":
                hoy = fields.Date.context_today(self)
                pendientes_de_fecha = self.filtered(lambda t: not t.fecha_real_fin)
                res = super().write(vals)
                if pendientes_de_fecha:
                    pendientes_de_fecha.write({"fecha_real_fin": hoy})
                return res
            vals = dict(vals, fecha_real_fin=False)
        return super().write(vals)

    # --- Botones ---

    def action_iniciar(self):
        self.write({"estado": "en_progreso"})

    def action_finalizar(self):
        self.write({"estado": "finalizada"})

    def action_reabrir(self):
        self.write({"estado": "en_progreso"})
