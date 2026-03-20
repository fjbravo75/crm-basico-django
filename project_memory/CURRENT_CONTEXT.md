# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** CRUD visible básico de clientes ya operativo, con listado paginado, búsqueda simple validada y datos demo cargables de forma repetible
- **Estado técnico del repo:** proyecto Django operativo en raíz, app `crm` registrada, modelos `Company`, `Client` e `Interaction` implementados, listado de clientes activo en `/` con paginación de 5 elementos por página, formulario de alta disponible en `clientes/nuevo/`, detalle básico disponible en `clientes/<int:pk>/`, edición básica disponible en `clientes/<int:pk>/editar/`, borrado con confirmación disponible en `clientes/<int:pk>/eliminar/`, interfaz visible del flujo en español y management command `seed_demo_crm` disponible
- **Estado funcional del CRM:** el flujo visible de clientes queda compuesto por listado con búsqueda y paginación, alta básica, detalle básico, edición básica y borrado con confirmación previa; la búsqueda conserva `q` al paginar, el texto de resultados usa el total real y la confirmación de borrado permite cancelar o eliminar con redirección al listado
- **Bloque actualmente abierto:** cerrado el tramo de trabajo que completa el flujo visible básico de clientes y ajusta el listado y la confirmación de borrado

---

## Objetivo inmediato

Retomar el proyecto desde un flujo visible de clientes ya completo y estable, con base demo repetible y validaciones recientes, para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- app `crm` con dominio base y flujo visible básico de clientes ya resuelto: listado, alta, detalle, edición y borrado con confirmación
- comando `python manage.py seed_demo_crm` implementado y validado de forma repetible
- validaciones reales recientes ejecutadas sobre `manage.py check`, suite de tests completa y verificación visual manual del borrado con confirmación, la cancelación, el listado paginado, la navegación entre páginas, la conservación de búsqueda al paginar y el total real mostrado

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

- El CRM ya tiene el CRUD visible básico de clientes, pero todavía no tiene un flujo visible de interacciones asociado al cliente.
- La resolución automática de `owner` en el alta es una solución puente para sostener el flujo actual, no un diseño final de negocio.
- No se ha abierto todavía un flujo CRUD completo ni autenticación o permisos de producto.
- No se abrió todavía CRUD visible de interacciones, estadísticas ni exportaciones.
- La continuidad debe seguir en microbloques cortos y sin salir del eje principal de clientes.

---

## Siguiente paso exacto

Abrir el microbloque corto del primer flujo visible de interacciones asociado al cliente.
