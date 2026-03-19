# AGENTS.md

## Propósito de este archivo

Este archivo es la puerta de entrada operativa para trabajar dentro de este repositorio.

Su función es situar a Codex al entrar, imponer una forma correcta de leer el contexto local y reducir improvisación, sobrelectura y cambios fuera de foco.

Este archivo no sustituye:

- `project_memory/CURRENT_CONTEXT.md`
- `project_memory/DECISIONS.md`
- `project_memory/memory_system/`
- las fuentes estratégicas del proyecto que viven fuera del repo

---

## Principios de comportamiento obligatorios

- Trabaja siempre con el contexto mínimo útil.
- No inventes contexto no escrito.
- No abras frentes fuera de la tarea pedida.
- No tomes decisiones estructurales no solicitadas.
- No conviertas una tarea concreta en una reorganización general.
- El estado real del repo manda sobre recuerdos incompletos, inferencias o contexto externo no pegado en el prompt.
- Si falta un dato crítico, no lo rellenes con intuición.
- No actualices memoria local por rutina.
- No registres hipótesis como si fueran hechos.
- No dupliques la misma información entre capas documentales.

---

## Orden de lectura por defecto

### Para trabajo técnico normal

Lee en este orden:

1. `AGENTS.md`
2. `project_memory/CURRENT_CONTEXT.md`
3. los archivos del repo directamente implicados en la tarea
4. `project_memory/DECISIONS.md` solo si afecta al criterio técnico, documental o de convenciones
5. una sesión concreta solo si la continuidad reciente importa de verdad

### Para mantenimiento documental

Lee en este orden:

1. `AGENTS.md`
2. `project_memory/CURRENT_CONTEXT.md`
3. `project_memory/memory_system/README.md`
4. `project_memory/memory_system/FILE_SELECTION_GUIDE.md`
5. el workflow correspondiente dentro de `project_memory/memory_system/workflows/`
6. `project_memory/memory_system/CONTENT_RULES.md`
7. `project_memory/memory_system/WRITING_RULES.md`
8. la plantilla correspondiente dentro de `project_memory/memory_system/templates/`
9. el índice correspondiente solo al final, si toca actualizarlo

---

## Qué no debe leerse por defecto

No leas por costumbre:

- históricos completos
- varias sesiones antiguas “por si acaso”
- índices si no necesitas localizar o registrar algo
- toda la carpeta `memory_system/` si la tarea no es documental
- `DECISIONS.md` si la tarea no depende de una decisión activa vigente

---

## Cuándo leer `DECISIONS.md`

Lee `project_memory/DECISIONS.md` solo cuando:

- la tarea dependa de una convención vigente
- la tarea pueda chocar con una decisión técnica o documental activa
- la tarea afecte a estructura, nomenclatura, reglas o criterios ya fijados

No lo leas si la tarea es pequeña, local y autocontenida y no depende de ninguna decisión activa relevante.

---

## Cuándo consultar `memory_system/`

Consulta `project_memory/memory_system/` solo cuando:

- haya que decidir qué archivo de memoria tocar
- haya que crear o actualizar una entrada documental
- haya que archivar una decisión superada
- haya que aplicar una plantilla documental
- haya que seguir un procedimiento de mantenimiento documental
- haya duda real sobre inclusión, exclusión, redacción o nomenclatura documental

No consultes `memory_system/` para trabajo técnico normal como:

- crear vistas
- editar templates
- tocar modelos
- revisar formularios
- arreglar rutas
- corregir bugs locales
- validar comportamiento ordinario del CRM

---

## Reglas cortas de mantenimiento de memoria local

- Si no hubo cambio real con impacto de continuidad, no toques nada.
- Si cambió la foto operativa vigente del proyecto, revisa `project_memory/CURRENT_CONTEXT.md`.
- Si nació, cambió o quedó fijada una decisión activa relevante, revisa `project_memory/DECISIONS.md`.
- Si una decisión activa fue sustituida o dejó de estar vigente, crea su trazabilidad en `project_memory/decisions_archive/`.
- Si una sesión o bloque tuvo entidad histórica propia, crea una entrada en `project_memory/sessions/`.
- Si se crea una nueva pieza histórica, actualiza el índice correspondiente.
- Antes de tocar memoria, usa `project_memory/memory_system/FILE_SELECTION_GUIDE.md`.

---

## Restricciones explícitas

- No inventes hechos, decisiones ni validaciones.
- No asumas acceso a fuentes de ChatGPT que no estén dentro del repo o resumidas en el prompt.
- No uses el histórico como fuente primaria si el presente ya está claro.
- No modifiques `AGENTS.md` salvo cambio real del sistema de trabajo.
- No registres microavances sin impacto real de continuidad.
- No conviertas el cierre documental en un diario largo.
- No trates hipótesis o deseos como estado real del proyecto.

---

## Regla final de prioridad operativa

Primero sitúate.

Después lee solo lo necesario.

Luego ejecuta únicamente el bloque pedido.

Y solo al final actualiza memoria local si corresponde de verdad.
