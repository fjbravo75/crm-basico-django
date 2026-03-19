# DECISIONS.md

## Propósito de este archivo

Este archivo contiene únicamente decisiones activas y vigentes que siguen condicionando el trabajo dentro del repo.

No es un histórico.

Cuando una decisión deje de estar vigente o sea sustituida, su trazabilidad debe moverse a `project_memory/decisions_archive/`.

---

## Decisiones activas vigentes

### 1. Naturaleza del sistema de memoria local

El sistema de memoria local del proyecto será documental.

No se convertirá en esta fase en una aplicación Python, base de datos formal ni subsistema técnico autónomo.

### 2. Estructura general del sistema

La arquitectura del sistema queda separada en estas capas:

- `AGENTS.md` como puerta de entrada conductual
- `project_memory/CURRENT_CONTEXT.md` como presente operativo
- `project_memory/DECISIONS.md` como criterios vigentes
- `project_memory/sessions/` como histórico modular de sesiones
- `project_memory/decisions_archive/` como histórico modular de decisiones superadas
- `project_memory/memory_system/` como gobierno del sistema de memoria

### 3. Criterio de lectura

El sistema debe priorizar siempre contexto mínimo útil.

No debe leerse de más por costumbre.

### 4. Criterio de actualización

La memoria local no se actualiza por rutina.

Solo se actualiza cuando existe un cambio real con impacto de continuidad.

### 5. Regla de funciones por capa

- `CURRENT_CONTEXT.md` = presente operativo
- `DECISIONS.md` = criterios vigentes
- `sessions/` = pasado útil por bloques
- `decisions_archive/` = trazabilidad de decisiones superadas
- `memory_system/` = reglas para mantener todo lo anterior

### 6. Política de histórico de sesiones

El histórico de sesiones no vivirá en un `SESSION_LOG.md` acumulativo único.

Vivirá en archivos independientes dentro de `project_memory/sessions/`, con índice.

### 7. Política de histórico de decisiones

Las decisiones superadas no permanecerán mezcladas dentro de `DECISIONS.md`.

Vivirán en `project_memory/decisions_archive/`, con índice.

### 8. Política de YAML

Se usará front matter YAML desde el inicio en:

- sesiones
- decisiones archivadas
- índices

No se usará por ahora en:

- `AGENTS.md`
- `CURRENT_CONTEXT.md`
- `DECISIONS.md`

### 9. Regla de salida explícita

La opción “no tocar nada” forma parte normal del sistema de decisión documental.

No es una excepción.

### 10. Prioridad funcional

Todas las decisiones del sistema deben favorecer que Codex:

- se sitúe rápido
- lea poco y bien
- no improvise
- no duplique
- no abra frentes laterales
- mantenga continuidad sin ruido

---

## Nota de uso

Si una nueva decisión cambia o sustituye alguna de las anteriores, esta debe actualizarse aquí y, si procede, la decisión superada debe archivarse en `project_memory/decisions_archive/`.
