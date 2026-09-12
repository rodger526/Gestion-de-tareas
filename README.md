# Gestor de Tareas

Aplicación de gestión de tareas desarrollada en Python.

El proyecto comenzó como un programa básico ejecutado desde consola
y está evolucionando progresivamente hacia una aplicación full stack.

## Estado del proyecto

🚧 En desarrollo

Actualmente se encuentra en la versión V3.

## Funcionalidades

- Crear tareas
- Listar tareas
- Editar tareas
- Eliminar tareas
- Cambiar estado de una tarea
- Prioridades
  - Baja
  - Media
  - Alta
  - Urgente
- Estados
  - Pendiente
  - En progreso
  - Completada
- Categorías
- Fechas límite
- Búsqueda de tareas
- Filtro por estado
- Filtro por prioridad
- Detección de tareas vencidas
- Ordenamiento por fecha límite
- Persistencia mediante SQLite

## Arquitectura

El proyecto está dividido en diferentes capas:

```text
app/
├── base_datos/
│   └── conexion.py
├── modelos/
│   └── tarea.py
├── servicios/
│   └── servicio_tareas.py
└── main.py