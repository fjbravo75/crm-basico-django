# README.md

## Propósito de esta carpeta

Esta carpeta contiene el sistema de gobierno de la memoria local del proyecto.

Su función es enseñar a Codex cómo decidir:

- qué archivo de memoria consultar
- qué archivo de memoria actualizar
- qué contenido debe entrar o no entrar
- cómo redactarlo
- cómo nombrarlo
- qué procedimiento seguir según el caso

Esta carpeta no es memoria viva del proyecto.

Esta carpeta no describe el CRM.

Describe cómo se mantiene la memoria local del CRM.

---

## Mapa del sistema

### Entrada conductual

- `AGENTS.md`
  - puerta de entrada operativa del repo
  - fija comportamiento y orden de lectura mínimo

### Memoria viva del proyecto

- `project_memory/CURRENT_CONTEXT.md`
  - presente operativo
- `project_memory/DECISIONS.md`
  - decisiones activas y vigentes

### Histórico modular

- `project_memory/sessions/`
  - sesiones o bloques cerrados con entidad histórica útil
- `project_memory/decisions_archive/`
  - decisiones superadas con trazabilidad

### Gobierno del sistema de memoria

- `project_memory/memory_system/GLOBAL_RULES.md`
- `project_memory/memory_system/FILE_SELECTION_GUIDE.md`
- `project_memory/memory_system/CONTENT_RULES.md`
- `project_memory/memory_system/WRITING_RULES.md`
- `project_memory/memory_system/NAMING_CONVENTIONS.md`
- `project_memory/memory_system/templates/`
- `project_memory/memory_system/workflows/`

---

## Orden de consulta recomendado

### Si la tarea es técnica y normal

No empieces por esta carpeta.

Empieza por:

1. `AGENTS.md`
2. `project_memory/CURRENT_CONTEXT.md`
3. archivos directamente implicados
4. `project_memory/DECISIONS.md` solo si afecta

### Si la tarea es documental

Consulta esta carpeta en este orden:

1. `README.md`
2. `FILE_SELECTION_GUIDE.md`
3. el workflow correspondiente
4. `CONTENT_RULES.md`
5. `WRITING_RULES.md`
6. la plantilla correspondiente
7. el índice correspondiente solo al final, si toca

---

## Regla principal de esta carpeta

Cada archivo de esta carpeta debe responder a una sola pregunta operativa.

Si una duda puede resolverse en un archivo más específico, no se duplique en otro.

---

## Resultado esperado

El sistema debe permitir que Codex:

- no improvise
- no toque memoria por rutina
- no mezcle presente, decisiones vigentes e histórico
- no duplique información
- sepa cuándo no documentar nada
- mantenga continuidad clara con el menor consumo de contexto posible
