from odoo.exceptions import AccessError
from odoo.tests import tagged

from .common import TareasCase


@tagged("post_install", "-at_install")
class TestSeguridad(TareasCase):
    def test_usuario_no_borra_tareas_ni_proyectos(self):
        tarea = self.crear_tarea()
        with self.assertRaises(AccessError):
            tarea.with_user(self.usuario).unlink()
        with self.assertRaises(AccessError):
            self.proyecto.with_user(self.usuario).unlink()

    def test_administrador_borra_tareas(self):
        tarea = self.crear_tarea()
        tarea.with_user(self.manager).unlink()
        self.assertFalse(tarea.exists())

    def test_usuario_no_crea_etiquetas(self):
        with self.assertRaises(AccessError):
            self.env["jcd_tareas.etiqueta"].with_user(self.usuario).create({"name": "Nueva"})

    def test_comentarios_ajenos_no_se_modifican(self):
        tarea = self.crear_tarea()
        Comentario = self.env["jcd_tareas.comentario"]
        comentario = Comentario.with_user(self.usuario).create({"tarea_id": tarea.id, "comentario": "Hola"})
        self.assertEqual(comentario.autor_id, self.usuario)
        # Otro usuario lo puede leer, pero no cambiarlo ni borrarlo
        ajeno = comentario.with_user(self.otro_usuario)
        self.assertEqual(ajeno.comentario, "Hola")
        with self.assertRaises(AccessError):
            ajeno.write({"comentario": "Cambiado"})
        with self.assertRaises(AccessError):
            ajeno.unlink()
        # El administrador sí puede
        comentario.with_user(self.manager).unlink()
        self.assertFalse(comentario.exists())

    def test_registros_de_tiempo_ajenos(self):
        tarea = self.crear_tarea()
        Registro = self.env["jcd_tareas.registro_tiempo"]
        with self.assertRaises(AccessError):
            Registro.with_user(self.usuario).create(
                {"tarea_id": tarea.id, "horas": 1, "usuario_id": self.otro_usuario.id}
            )
        propio = Registro.with_user(self.usuario).create({"tarea_id": tarea.id, "horas": 2})
        self.assertEqual(propio.usuario_id, self.usuario)
        with self.assertRaises(AccessError):
            propio.with_user(self.otro_usuario).write({"horas": 8})
