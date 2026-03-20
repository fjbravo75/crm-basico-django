# CURRENT_CONTEXT.md

## Propósito de este archivo

Este archivo mantiene la foto operativa vigente del proyecto dentro del repo local.

Debe ser corto, claro y reescribirse cuando cambie el estado real del proyecto.

No es un histórico.

No debe crecer por acumulación.

---

## Estado actual

- **Proyecto:** CRM Básico
- **Fase actual:** base del dominio del CRM ya implementada y validada, lista para abrir el siguiente microbloque funcional
- **Estado técnico del repo:** proyecto Django operativo en raíz, app `crm` registrada, `DEFAULT_AUTO_FIELD` fijado en `config/settings.py`, modelos `Company`, `Client` e `Interaction` implementados, admin básico registrado y migración inicial del dominio creada y aplicada
- **Estado funcional del CRM:** ya existe el núcleo de datos del sistema sobre `User`, `Company`, `Client` e `Interaction`, pero siguen pendientes CRUDs, vistas, formularios, URLs y buscador
- **Bloque actualmente abierto:** preparar el siguiente microbloque corto sobre la capa funcional del CRM a partir del modelo de datos ya cerrado

---

## Objetivo inmediato

Retomar el proyecto desde una base de dominio ya cerrada y validada para abrir el siguiente microbloque técnico con orden y continuidad, partiendo de:

- sistema documental local operativo
- repo enlazado y sincronizado con GitHub desde `main`
- app `crm` con modelos reales de dominio y migración inicial aplicada
- validaciones de `makemigrations`, `migrate` y `check` ya resueltas sin incidencias
- commit de cierre del bloque registrado como `af47c0a` con mensaje `Implement CRM domain models and initial migration`

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

- El CRM ya tiene modelo de dominio base, pero todavía no tiene flujos funcionales ni vistas de producto.
- No se han abierto todavía CRUDs, formularios, URLs ni comportamiento real de uso.
- La siguiente sesión debe seguir en pasos pequeños y sin abrir complejidad innecesaria.

---

## Siguiente paso exacto

Abrir el siguiente microbloque corto para aterrizar el CRUD básico de clientes sobre la base de dominio ya implementada.
