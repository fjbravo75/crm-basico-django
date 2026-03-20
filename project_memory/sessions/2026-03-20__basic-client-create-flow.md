---
id: session-2026-03-20-03
date: 2026-03-20
type: session
status: closed
focus: "alta básica de clientes operativa sobre el listado existente, validación real del flujo y cierre documental local"
next_step: "abrir el microbloque corto del detalle básico de cliente sobre el flujo ya compuesto por listado y alta"
---

# Alta básica de clientes sobre listado existente

## Estado al cierre

El CRM queda con un flujo base de clientes compuesto por listado con búsqueda simple y alta básica operativa desde la interfaz, con validación real del guardado, la redirección al listado y la visibilidad del nuevo cliente en el flujo normal.

## Trabajo realizado

- Se creó `crm/forms.py` con `ClientForm` para el alta básica de `Client`.
- Se creó `crm/templates/crm/client_form.html` con formulario server-rendered en español y se añadió el acceso visible “Nuevo cliente” desde el listado.
- Se ajustaron `crm/views.py`, `crm/urls.py` y `crm/templates/crm/client_list.html` para abrir `clientes/nuevo/`, guardar correctamente y redirigir al listado.
- Se añadieron tests del flujo en `crm/tests.py` y se ejecutaron `.venv/bin/python manage.py check` y `.venv/bin/python manage.py test crm.tests.ClientCreateFlowTests`, ambos con resultado correcto.
- El cierre técnico del bloque quedó registrado en el commit `b06aa3b` con mensaje `Add basic client creation flow`.

## Decisiones fijadas o confirmadas

- La interfaz visible del flujo de clientes se mantiene en español y con una implementación sobria server-rendered.
- La resolución automática de `owner` queda como solución puente del bloque actual: usar usuario autenticado si existe, reutilizar el primer usuario disponible si no lo hay, y crear `maria.ortega` solo si el sistema no tiene ninguno.
- No se abrió todavía detalle, edición ni borrado de cliente.

## Pendiente inmediato

- Abrir el siguiente microbloque sobre el detalle básico de cliente.
- Revisar más adelante la asignación de `owner` cuando exista un diseño de autenticación y negocio más estable.

## Siguiente paso exacto

- Abrir el microbloque corto del detalle básico de cliente sobre el flujo ya compuesto por listado y alta.
