# CONTENT_RULES.md

## Propósito de este archivo

Este archivo fija qué tipo de contenido entra y qué tipo de contenido no entra en cada capa documental del sistema.

---

## Reglas por archivo o capa

### `project_memory/CURRENT_CONTEXT.md`

Debe incluir:

- estado actual real
- fase vigente
- bloque actualmente abierto
- objetivo inmediato
- límites actuales
- siguiente paso exacto

No debe incluir:

- histórico largo
- decisiones antiguas ya superadas
- narrativa decorativa
- sesiones completas
- explicaciones que pertenecen a `memory_system/`

### `project_memory/DECISIONS.md`

Debe incluir:

- decisiones activas vigentes
- criterios que siguen condicionando trabajo futuro
- políticas en uso real

No debe incluir:

- decisiones antiguas superadas
- dudas abiertas
- hipótesis
- relato histórico
- notas decorativas

### `project_memory/sessions/`

Debe incluir:

- cierre útil de una sesión o bloque
- estado al cierre
- trabajo realizado
- decisiones fijadas o confirmadas
- pendiente inmediato
- siguiente paso exacto

No debe incluir:

- diarios narrativos
- microacciones irrelevantes
- duplicación entera de `CURRENT_CONTEXT.md`
- teoría del sistema

### `project_memory/decisions_archive/`

Debe incluir:

- una decisión que dejó de estar vigente
- contexto breve
- motivo de archivo
- sustitución o estado final
- trazabilidad mínima útil

No debe incluir:

- decisiones todavía vigentes
- ensayo histórico largo
- especulación
- material que pertenece a `DECISIONS.md`

### Índices

Deben incluir:

- propósito del índice
- criterio de orden
- lista de entradas

No deben incluir:

- resúmenes largos
- duplicación del contenido de las entradas
- narrativas explicativas extensas

### `project_memory/memory_system/`

Debe incluir:

- reglas del sistema
- criterios de selección
- reglas de redacción
- nomenclatura
- plantillas
- workflows

No debe incluir:

- descripción funcional del CRM
- decisiones activas del proyecto
- histórico del proyecto
- contenido ornamental

---

## Regla de frontera

Si un contenido habla del estado real del proyecto, no pertenece a `memory_system/`.

Si un contenido habla de cómo mantener la memoria, no pertenece a `CURRENT_CONTEXT.md` ni a `DECISIONS.md`.
