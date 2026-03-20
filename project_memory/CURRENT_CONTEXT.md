# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** listado básico de clientes ya operativo, con búsqueda simple validada y datos demo cargables de forma repetible
- **Estado técnico del repo:** proyecto Django operativo en raíz, app `crm` registrada, modelos `Company`, `Client` e `Interaction` implementados, listado de clientes activo en `/`, interfaz visible del flujo en español, y management command `seed_demo_crm` ya disponible para sembrar datos demo de desarrollo sin depender del admin
- **Estado funcional del CRM:** existe un flujo básico de listado de clientes con búsqueda por nombre, correo o empresa; la base local queda preparada con 3 empresas demo, 12 clientes demo y 5 interacciones demo tras ejecutar el seed
- **Bloque actualmente abierto:** listo para abrir el siguiente microbloque corto del alta básica de clientes sobre el listado ya operativo

---

## Objetivo inmediato

Retomar el proyecto desde un listado de clientes ya funcional y una base demo repetible para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- app `crm` con dominio base, listado de clientes y búsqueda simple ya resueltos
- comando `python manage.py seed_demo_crm` implementado y validado de forma repetible
- validaciones reales del bloque ejecutadas sobre `check`, seed, conteos y respuesta HTTP del listado y la búsqueda

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

- El CRM ya tiene listado de clientes y búsqueda simple, pero todavía no tiene alta, edición, borrado ni detalle de cliente.
- No se ha abierto todavía un flujo CRUD completo ni formularios funcionales de producto.
- La continuidad debe seguir en microbloques cortos y sin salir del eje principal de clientes.
- La siguiente sesión debe seguir en pasos pequeños y sin abrir complejidad innecesaria.

---

## Siguiente paso exacto

Abrir el siguiente microbloque corto para implementar el alta básica de clientes sobre el listado ya operativo y la base demo disponible.
