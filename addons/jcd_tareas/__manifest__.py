{
    "name": "Tareas JCD",
    "summary": "Proyectos y tareas con prioridades, dependencias y registro de tiempo",
    "description": """
Gestión de proyectos y tareas para Odoo 17:

- Proyectos con progreso, horas estimadas y dedicadas.
- Tareas con prioridad, estado, responsable, etiquetas y fechas.
- Dependencias entre tareas: no se puede finalizar una tarea bloqueada.
- Registro de tiempo (partes de horas) con análisis por proyecto y usuario.
- Vistas kanban, lista, formulario, calendario, pivot y gráfico.
""",
    "author": "Jorge Cuevas Delgado",
    "website": "https://github.com/Jocude/Odoo-TaskManager",
    "category": "Services/Project",
    "version": "17.0.2.0.0",
    "license": "GPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/tarea.xml",
        "views/proyecto.xml",
        "views/etiqueta.xml",
        "views/registro_tiempo.xml",
        "views/menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "images": ["static/description/icon.png"],
    "post_init_hook": "post_init_hook",
    "application": True,
    "installable": True,
}
