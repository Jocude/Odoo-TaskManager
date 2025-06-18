# 📋 Odoo Task Manager

Módulo personalizado para **Odoo 17**, diseñado para gestionar tareas de forma eficiente dentro del ERP. Este proyecto se ejecuta completamente mediante **Docker**, sin necesidad de instalar Odoo manualmente.

---

## 🚀 ¿Qué incluye este módulo?

- Gestión de tareas con campos personalizados (asignado a, prioridad, fechas, descripción, etc.).
- Vistas tipo Kanban, Lista y Formulario.
- Registro y seguimiento del tiempo.
- Integración con dependencias entre tareas (activable).
- Totalmente integrado en el entorno de Odoo 17.

---

## 🐳 Instalación con Docker

> No es necesario instalar Odoo ni dependencias adicionales en tu sistema local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jocude/Odoo-TaskManager.git
cd Odoo-TaskManager
```
Iniciar odoo
```bash
docker-compose up -d
