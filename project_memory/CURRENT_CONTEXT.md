# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** arranque inicial cerrado y base mínima del proyecto lista para el siguiente microbloque técnico
- **Estado técnico del repo:** remoto GitHub creado y enlazado como `origin`, último cierre técnico validado con `main` sincronizada con `origin/main`, `.gitignore` reforzado, `README.md` inicial creado y proyecto Django base operativo en raíz con app `crm` ya creada y registrada
- **Estado funcional del CRM:** existe la app principal `crm`, pero todavía no se han definido modelos reales ni comportamiento funcional del producto
- **Bloque actualmente abierto:** preparar la planificación corta del modelo conceptual técnico del CRM antes de crear modelos y migraciones

---

## Objetivo inmediato

Retomar el proyecto desde una base ya saneada y sincronizada para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- saneamiento básico inicial del repo ya resuelto con `.gitignore` y `README.md`
- app `crm` creada, registrada y validada con `python manage.py check`

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

---

## Límites actuales

- El CRM todavía no tiene modelos de dominio, flujos funcionales ni vistas de producto.
- No se ha abierto todavía la implementación real del modelo del negocio.
- La siguiente sesión debe seguir en pasos pequeños y sin abrir complejidad innecesaria.

---

## Siguiente paso exacto

Planificar en corto el modelo conceptual técnico del CRM y cerrar esa definición mínima antes de crear modelos reales y migraciones.
