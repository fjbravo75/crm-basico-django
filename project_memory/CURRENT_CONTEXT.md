# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** diseño y cierre del sistema documental local para Codex antes del arranque técnico del repo
- **Estado técnico del repo:** estructura documental pendiente de implementación real en archivos locales
- **Estado funcional del CRM:** todavía no iniciado dentro del repo
- **Bloque actualmente abierto:** creación del sistema base de memoria viva local y gobierno documental para trabajo con Codex

---

## Objetivo inmediato

Dejar cerrado e implementable el sistema documental local mínimo para que Codex pueda trabajar con:

- contexto presente claro
- decisiones activas separadas del histórico
- histórico modular de sesiones
- histórico modular de decisiones superadas
- reglas explícitas para decidir qué leer y qué actualizar

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

- No se ha arrancado todavía el desarrollo técnico del CRM dentro del repo.
- No deben abrirse todavía bloques de implementación funcional del producto.
- No deben añadirse complejidades fuera del sistema documental base.

---

## Siguiente paso exacto

Implementar en el repo local la estructura base ya cerrada de estos archivos:

- `AGENTS.md`
- `project_memory/CURRENT_CONTEXT.md`
- `project_memory/DECISIONS.md`
- `project_memory/sessions/sessions_index.md`
- `project_memory/decisions_archive/decisions_archive_index.md`
- `project_memory/memory_system/` con sus reglas, plantillas y workflows base
