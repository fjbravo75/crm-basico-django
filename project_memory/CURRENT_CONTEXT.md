# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** CRUD visible básico de clientes cerrado y primer flujo visible de actividad asociado al cliente ya operativo, con paginación local y datos demo ampliados para pruebas
- **Estado técnico del repo:** proyecto Django operativo en raíz, app `crm` registrada, modelos `Company`, `Client` e `Interaction` implementados, listado de clientes activo en `/` con paginación de 5 elementos por página, formulario de alta disponible en `clientes/nuevo/`, detalle básico disponible en `clientes/<int:pk>/`, edición básica disponible en `clientes/<int:pk>/editar/`, borrado con confirmación disponible en `clientes/<int:pk>/eliminar/`, alta básica de actividad disponible en `clientes/<int:client_pk>/interacciones/nueva/`, bloque de actividad visible dentro del detalle de cliente con paginación local de 3 registros por página, interfaz visible del flujo en español y management command `seed_demo_crm` disponible
- **Estado funcional del CRM:** el flujo visible de clientes queda compuesto por listado con búsqueda y paginación, alta básica, detalle básico, edición básica y borrado con confirmación previa; el detalle del cliente muestra ya un bloque de actividad con estado vacío o listado cronológico descendente, botón visible `Registrar actividad`, paginación local a 3 registros por página y resúmenes con render en párrafos; la búsqueda conserva `q` al paginar, el texto de resultados usa el total real y la confirmación de borrado permite cancelar o eliminar con redirección al listado
- **Bloque actualmente abierto:** cerrado el microbloque del primer flujo visible de actividad asociado al cliente, incluyendo pulido visual local y ampliación del seed demo para pruebas reales

---

## Objetivo inmediato

Retomar el proyecto desde un flujo visible de clientes ya completo y un primer flujo visible de actividad ya operativo y presentable, con base demo repetible y validaciones recientes, para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- app `crm` con dominio base y flujo visible básico de clientes ya resuelto: listado, alta, detalle, edición y borrado con confirmación
- primer flujo visible de actividad ya resuelto dentro del detalle de cliente, con alta ligada al cliente por URL, copy visible en español natural y paginación local del bloque
- comando `python manage.py seed_demo_crm` implementado y ampliado con actividad demo suficiente para probar paginación, orden descendente y resúmenes con uno o dos párrafos
- validaciones reales recientes ejecutadas sobre `manage.py check`, suite de tests completa y comprobaciones visuales manuales del bloque de actividad con datos demo reales

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
- Los flujos visibles nuevos deben seguir entrando en microbloques cortos, server-rendered y sin abrir complejidad innecesaria.
- La sección visible asociada a `Interaction` se presenta al usuario como `Actividad`, no como `Interacciones`.
- La paginación del bloque Actividad debe mantenerse local al detalle de cliente, con parámetro GET específico y sin scroll interno de tarjeta.

---

## Límites actuales

- El CRM ya tiene el CRUD visible básico de clientes y un primer flujo visible de actividad asociado al cliente, pero todavía no tiene CRUD completo de actividad.
- La resolución automática de `owner` en el alta de clientes y de `created_by` en actividad es una solución puente para sostener el flujo actual, no un diseño final de negocio.
- No se ha abierto todavía autenticación o permisos de producto.
- No se abrió todavía edición o borrado visible de actividad, estadísticas ni exportaciones.
- La continuidad debe seguir en microbloques cortos y sin salir del eje principal de clientes y actividad.

---

## Siguiente paso exacto

Abrir el siguiente microbloque corto del flujo visible de actividad asociado al cliente, previsiblemente edición básica o borrado básico de actividad según convenga más al recorrido visible.
