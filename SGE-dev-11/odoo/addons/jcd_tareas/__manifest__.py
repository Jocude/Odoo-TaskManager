{
    'name': "Gestión de Proyectos (JCD Tareas)",
    'summary': "Módulo para la gestión de proyectos y tareas",
    'description': """
        Módulo de Odoo para gestionar proyectos y tareas, permitiendo:
        - Crear nuevos proyectos.
        - Agregar tareas específicas a cada proyecto.
        - Establecer fechas de finalización para las tareas.
        - Asignar responsables a las tareas.
        - Seguimiento del estado de las tareas.
    """,
    'author': "Jorge Cuevas Delgado",
    'website': "https://www.google.com",   
    'category': 'Project', 
    'version': '1.0',
    'depends': ['base'], 
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/proyecto.xml',    
        'views/etiqueta.xml',  
        'views/tarea.xml',
        'views/tareaComentario.xml',
        'views/menus.xml',      
    ],
    'demo': [                         
         'demo/demo.xml', 
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',    
    'icon': '/jcd_tareas/static/description/Logo.jpg'          
}