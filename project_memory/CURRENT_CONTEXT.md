# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** listado, alta básica, detalle básico y edición básica de clientes ya operativos, con búsqueda simple validada y datos demo cargables de forma repetible
- **Estado técnico del repo:** proyecto Django operativo en raíz, app `crm` registrada, modelos `Company`, `Client` e `Interaction` implementados, listado de clientes activo en `/`, formulario de alta disponible en `clientes/nuevo/`, detalle básico disponible en `clientes/<int:pk>/`, edición básica disponible en `clientes/<int:pk>/editar/`, interfaz visible del flujo en español, management command `seed_demo_crm` disponible, y validaciones reales recientes ejecutadas sobre `check` y tests específicos de alta, detalle y edición
- **Estado funcional del CRM:** existe un flujo visible de clientes compuesto por listado con búsqueda por nombre, correo o empresa, alta básica con formulario server-rendered, detalle básico enlazado desde el listado y edición básica accesible desde el detalle, con guardado válido y retorno al detalle actualizado
- **Bloque actualmente abierto:** cerrado el microbloque corto de edición básica de cliente sobre el flujo ya compuesto por listado, alta y detalle

---

## Objetivo inmediato

Retomar el proyecto desde un flujo base de clientes ya compuesto por listado, alta básica, detalle básico y edición básica, con base demo repetible y validaciones recientes, para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- app `crm` con dominio base, listado, búsqueda simple, alta básica, detalle básico y edición básica ya resueltos
- comando `python manage.py seed_demo_crm` implementado y validado de forma repetible
- validaciones reales recientes ejecutadas sobre `.venv/bin/python manage.py check`, `.venv/bin/python manage.py test crm.tests.ClientCreateFlowTests`, `.venv/bin/python manage.py test crm.tests.ClientDetailFlowTests` y `.venv/bin/python manage.py test crm.tests.ClientUpdateFlowTests -v 2`

---

## Decisiones vigentes que condicionan el trabajo actual

- El eje del sistema será documental, no una mini aplicación de memoria.
- La solución será híbrida y sobria: Markdown como fuente principal de verdad, con disciplina interna y YAML ligero solo donde se ha decidido.
- `CURRENT_CONTEXT.md` debe ser corto, operativo y reescribible.
- `DECISIONS.md` debe contener solo decisiones activas y vigentes.
- El histórico de sesiones vivirá en `project_memory/sessions/` con índice.
- El histórico de decisiones superadas vivirá en `project_memory/decisions_archive/` con índice.
- `AGENTS.md` actuará como puerta de entrada conductual y operativa.
- `project_memory/memory_system/` será la capa de gobierno del sistema de memoria.
- La salida “no tocar nada” es una decisión válida del sistema.
- La prioridad general es contexto mínimo útil, no lectura exhaustiva.
- Los datos demo del CRM se cargarán con un management command específico de desarrollo y no desde el admin como flujo principal.

---

## Límites actuales

- El CRM ya tiene listado, búsqueda simple, alta básica, detalle básico y edición básica de clientes, pero todavía no tiene borrado de cliente.
- La resolución automática de `owner` en el alta es una solución puente para sostener el flujo actual, no un diseño final de negocio.
- No se ha abierto todavía un flujo CRUD completo ni autenticación o permisos de producto.
- No se abrió todavía CRUD visible de interacciones, estadísticas ni exportaciones.
- La continuidad debe seguir en microbloques cortos y sin salir del eje principal de clientes.

---

## Siguiente paso exacto

Abrir el microbloque corto de borrado básico de cliente sobre el flujo ya compuesto por listado, alta, detalle y edición.
