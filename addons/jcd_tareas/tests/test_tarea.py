from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import TareasCase


@tagged("post_install", "-at_install")
class TestTarea(TareasCase):
    # --- Estados y fecha de fin real ---

    def test_finalizar_rellena_fecha_real(self):
        tarea = self.crear_tarea()
        tarea.action_iniciar()
        self.assertEqual(tarea.estado, "en_progreso")
        self.assertFalse(tarea.fecha_real_fin)
        tarea.action_finalizar()
        self.assertEqual(tarea.estado, "finalizada")
        self.assertEqual(tarea.fecha_real_fin, self.hoy)

    def test_crear_finalizada_rellena_fecha_real(self):
        tarea = self.crear_tarea(estado="finalizada")
        self.assertEqual(tarea.fecha_real_fin, self.hoy)

    def test_reabrir_borra_fecha_real(self):
        tarea = self.crear_tarea(estado="finalizada")
        tarea.action_reabrir()
        self.assertEqual(tarea.estado, "en_progreso")
        self.assertFalse(tarea.fecha_real_fin)

    def test_finalizar_conserva_fecha_real_existente(self):
        ayer = self.hoy - timedelta(days=1)
        tarea = self.crear_tarea()
        tarea.write({"estado": "finalizada", "fecha_real_fin": ayer})
        self.assertEqual(tarea.fecha_real_fin, ayer)

    # --- Fechas ---

    def test_fin_anterior_al_inicio_no_se_permite(self):
        with self.assertRaises(ValidationError):
            self.crear_tarea(fecha_inicio=self.hoy + timedelta(days=10), dias_fin=5)

    def test_retrasada(self):
        vencida = self.crear_tarea("Vencida", dias_fin=-1)
        a_tiempo = self.crear_tarea("A tiempo", dias_fin=3)
        vencida_finalizada = self.crear_tarea("Vencida pero terminada", dias_fin=-1, estado="finalizada")
        self.assertTrue(vencida.retrasada)
        self.assertFalse(a_tiempo.retrasada)
        self.assertFalse(vencida_finalizada.retrasada)

    def test_buscar_retrasadas(self):
        vencida = self.crear_tarea("Vencida", dias_fin=-1)
        a_tiempo = self.crear_tarea("A tiempo", dias_fin=3)
        dominio = [("proyecto_id", "=", self.proyecto.id)]
        self.assertEqual(self.Tarea.search(dominio + [("retrasada", "=", True)]), vencida)
        self.assertEqual(self.Tarea.search(dominio + [("retrasada", "=", False)]), a_tiempo)

    # --- Tiempo ---

    def test_horas_dedicadas_y_progreso(self):
        tarea = self.crear_tarea(horas_estimadas=10)
        self.env["jcd_tareas.registro_tiempo"].create(
            [
                {"tarea_id": tarea.id, "horas": 3},
                {"tarea_id": tarea.id, "horas": 1.5},
            ]
        )
        self.assertAlmostEqual(tarea.horas_dedicadas, 4.5)
        self.assertAlmostEqual(tarea.progreso, 45.0)

    def test_progreso_no_pasa_de_100(self):
        tarea = self.crear_tarea(horas_estimadas=2)
        self.env["jcd_tareas.registro_tiempo"].create({"tarea_id": tarea.id, "horas": 5})
        self.assertEqual(tarea.progreso, 100.0)

    def test_horas_de_registro_validas(self):
        tarea = self.crear_tarea()
        for horas in (0, -1, 25):
            with self.assertRaises(ValidationError):
                self.env["jcd_tareas.registro_tiempo"].create({"tarea_id": tarea.id, "horas": horas})

    # --- Dependencias ---

    def test_tarea_bloqueada_no_se_puede_finalizar(self):
        base = self.crear_tarea("Base")
        dependiente = self.crear_tarea("Dependiente", depende_de_ids=[(6, 0, base.ids)])
        self.assertTrue(dependiente.bloqueada)
        with self.assertRaises(ValidationError):
            dependiente.action_finalizar()
        base.action_finalizar()
        self.assertFalse(dependiente.bloqueada)
        dependiente.action_finalizar()
        self.assertEqual(dependiente.estado, "finalizada")

    def test_dependencia_de_si_misma(self):
        tarea = self.crear_tarea()
        with self.assertRaises(ValidationError):
            tarea.depende_de_ids = [(4, tarea.id)]

    def test_ciclo_de_dependencias(self):
        a = self.crear_tarea("A")
        b = self.crear_tarea("B", depende_de_ids=[(6, 0, a.ids)])
        c = self.crear_tarea("C", depende_de_ids=[(6, 0, b.ids)])
        with self.assertRaises(ValidationError):
            a.depende_de_ids = [(4, c.id)]

    def test_bloquea_es_la_inversa(self):
        base = self.crear_tarea("Base")
        dependiente = self.crear_tarea("Dependiente", depende_de_ids=[(6, 0, base.ids)])
        self.assertEqual(base.bloquea_ids, dependiente)
