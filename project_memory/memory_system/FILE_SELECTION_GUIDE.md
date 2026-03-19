# FILE_SELECTION_GUIDE.md

## Propósito de este archivo

Este archivo sirve para decidir qué archivo de memoria debe tocarse en cada caso.

Su función principal es reducir ambigüedad y evitar duplicación.

---

## Árbol de decisión documental

### Paso 1. ¿Hubo cambio real con impacto de continuidad?

- Si no, no toques nada.
- Si sí, continúa.

### Paso 2. ¿Cambió la foto operativa vigente del proyecto?

Ejemplos típicos:

- cambió la fase actual
- cambió el bloque abierto
- cambió el objetivo inmediato
- cambió el siguiente paso exacto
- cambió el estado general del repo o del proyecto

- Si sí, revisa `project_memory/CURRENT_CONTEXT.md`.
- Si no, continúa.

### Paso 3. ¿Nació, cambió o quedó fijada una decisión activa relevante?

Ejemplos típicos:

- se fijó una convención estructural
- se confirmó un criterio que condiciona trabajo futuro
- se sustituyó una regla vigente
- se adoptó una política técnica o documental nueva

- Si sí, revisa `project_memory/DECISIONS.md`.
- Si no, continúa.

### Paso 4. ¿Una decisión activa anterior ha dejado de estar vigente o ha sido sustituida?

- Si sí, crea un archivo en `project_memory/decisions_archive/` y actualiza `project_memory/decisions_archive/decisions_archive_index.md`.
- Si no, continúa.

### Paso 5. ¿La sesión o bloque tiene entidad histórica propia?

Una sesión o bloque tiene entidad histórica propia cuando deja un cierre útil para retomar después, por ejemplo:

- cierre de un microbloque importante
- cierre de una decisión estructural
- final de una sesión con impacto real
- validación de un bloque que conviene dejar trazado

- Si sí, crea un archivo en `project_memory/sessions/` y actualiza `project_memory/sessions/sessions_index.md`.
- Si no, continúa.

### Paso 6. ¿Después de evaluar todo lo anterior no aplica ninguna capa?

Entonces no toques nada.

---

## Prioridades de decisión

Si aplica más de una capa, usa esta lógica:

1. `CURRENT_CONTEXT.md` si cambió el presente operativo
2. `DECISIONS.md` si cambió una decisión vigente
3. `decisions_archive/` si una decisión activa fue sustituida
4. `sessions/` si el bloque merece trazabilidad histórica útil
5. índices solo al final, si se creó una pieza histórica nueva

---

## Regla clave

No uses sesiones para guardar lo que debe vivir en `CURRENT_CONTEXT.md`.

No uses `DECISIONS.md` como histórico.

No uses índices para explicar contenido.

No documentes por reflejo.

---

## Resultado normal válido

La salida correcta del sistema puede ser:

- actualizar un solo archivo
- actualizar varios archivos coordinados
- o no tocar nada
