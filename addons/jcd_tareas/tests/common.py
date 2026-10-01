from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase, new_test_user


class TareasCase(TransactionCase):
    """Datos comunes: un usuario normal, un administrador, un proyecto y helpers para crear tareas."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hoy = fields.Date.today()
        cls.usuario = new_test_user(cls.env, login="ana", groups="jcd_tareas.group_jcd_tareas_user")
        cls.otro_usuario = new_test_user(cls.env, login="luis", groups="jcd_tareas.group_jcd_tareas_user")
        cls.manager = new_test_user(cls.env, login="marta", groups="jcd_tareas.group_jcd_tareas_manager")
        cls.Tarea = cls.env["jcd_tareas.tarea"]
        cls.proyecto = cls.env["jcd_tareas.proyecto"].create({"name": "Proyecto de prueba"})

    @classmethod
    def crear_tarea(cls, nombre="Tarea", dias_fin=7, **valores):
        return cls.Tarea.create(
            {
                "name": nombre,
                "proyecto_id": cls.proyecto.id,
                "fecha_fin_estimada": cls.hoy + timedelta(days=dias_fin),
                **valores,
            }
        )
