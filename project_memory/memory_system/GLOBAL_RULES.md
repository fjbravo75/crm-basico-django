# GLOBAL_RULES.md

## Propósito de este archivo

Este archivo fija las reglas transversales del sistema de memoria local.

Estas reglas se aplican a todas las capas documentales del sistema.

---

## Reglas globales

### 1. Regla de veracidad

No registres como hecho nada que no haya ocurrido realmente.

No registres como validado nada que no haya sido validado.

No registres como decidido nada que siga abierto.

### 2. Regla de no improvisación

No rellenes huecos con suposiciones.

Si falta un dato crítico, no lo inventes.

### 3. Regla de contexto mínimo útil

Lee y escribe solo lo necesario para ejecutar bien la tarea o mantener continuidad real.

### 4. Regla de no duplicación

No repitas la misma información entre `CURRENT_CONTEXT.md`, `DECISIONS.md`, sesiones, archivos archivados e índices.

Cada capa debe conservar su función propia.

### 5. Regla de actualización no rutinaria

La memoria local no se actualiza por costumbre.

Solo se actualiza cuando el cambio tiene impacto real de continuidad.

### 6. Regla de salida válida “no tocar nada”

Si no hubo cambio real con impacto documental, la decisión correcta es no tocar ningún archivo.

### 7. Regla de foco

No conviertas una tarea técnica pequeña en una actualización documental amplia.

No conviertas una actualización documental concreta en una reorganización general del sistema.

### 8. Regla de trazabilidad

Cuando una decisión activa deje de estar vigente y siga importando su rastro, debe archivarse fuera de `DECISIONS.md`.

### 9. Regla de separación de capas

- presente operativo en `CURRENT_CONTEXT.md`
- decisiones vigentes en `DECISIONS.md`
- pasado útil por bloques en `sessions/`
- decisiones superadas en `decisions_archive/`
- reglas del sistema en `memory_system/`

### 10. Regla de cierre útil

Toda actualización documental debe dejar claro, cuando aplique:

- estado actual
- qué cambió realmente
- qué sigue vigente
- qué queda pendiente
- cuál es el siguiente paso exacto

---

## Nota final

Si una acción documental rompe alguna de estas reglas, debe revisarse antes de ejecutarse.
