from odoo.tests import tagged

from .common import TareasCase


@tagged("post_install", "-at_install")
class TestProyecto(TareasCase):
    def test_proyecto_vacio(self):
        self.assertEqual(self.proyecto.tarea_count, 0)
        self.assertEqual(self.proyecto.progreso, 0.0)

    def test_progreso_y_horas(self):
        t1 = self.crear_tarea("Uno", horas_estimadas=4, estado="finalizada")
        self.crear_tarea("Dos", horas_estimadas=6)
        self.crear_tarea("Tres", horas_estimadas=10)
        self.crear_tarea("Cuatro")
        self.env["jcd_tareas.registro_tiempo"].create({"tarea_id": t1.id, "horas": 3.5})
        self.assertEqual(self.proyecto.tarea_count, 4)
        self.assertAlmostEqual(self.proyecto.progreso, 25.0)
        self.assertAlmostEqual(self.proyecto.horas_estimadas, 20.0)
        self.assertAlmostEqual(self.proyecto.horas_dedicadas, 3.5)

    def test_accion_ver_tareas(self):
        accion = self.proyecto.action_ver_tareas()
        self.assertEqual(accion["res_model"], "jcd_tareas.tarea")
        self.assertIn(("proyecto_id", "=", self.proyecto.id), accion["domain"])
        self.assertEqual(accion["context"]["default_proyecto_id"], self.proyecto.id)

    def test_borrar_proyecto_borra_sus_tareas(self):
        tarea = self.crear_tarea()
        self.proyecto.unlink()
        self.assertFalse(tarea.exists())
