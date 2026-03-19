# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** arranque técnico del repo y cierre del sistema documental local para Codex
- **Estado técnico del repo:** repo inicializado con Git, sistema de memoria viva local creado y proyecto Django base creado en raíz con `config/` y `manage.py`
- **Estado funcional del CRM:** base Django recién creada, sin desarrollo funcional del producto todavía
- **Bloque actualmente abierto:** cierre limpio del arranque inicial y preparación de la siguiente sesión de desarrollo

---

## Objetivo inmediato

Retomar el proyecto desde una base ya preparada para empezar el desarrollo real con orden y continuidad, partiendo de:

- sistema documental local operativo
- proyecto Django base ya creado
- separación clara entre memoria viva, gobierno documental e histórico
- repo listo para seguir con configuración y siguientes bloques técnicos

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

- El CRM todavía no tiene apps propias, modelos ni vistas funcionales.
- No se ha empezado todavía el desarrollo del producto como tal.
- La siguiente sesión debe seguir en pasos pequeños y sin abrir complejidad innecesaria.

---

## Siguiente paso exacto

Definir y ejecutar el siguiente microbloque técnico del proyecto Django ya sobre la base creada, manteniendo sincronía limpia entre repo y memoria viva cuando haya un cambio real.
