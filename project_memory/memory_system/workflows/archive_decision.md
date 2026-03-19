# archive_decision.md

## Cuándo usar este workflow

Usa este workflow cuando una decisión activa deje de estar vigente, sea sustituida o necesite salir de `DECISIONS.md` sin perder trazabilidad.

---

## Pasos

1. Lee `AGENTS.md`.
2. Lee `project_memory/DECISIONS.md`.
3. Confirma qué decisión deja de estar vigente.
4. Usa `project_memory/memory_system/templates/archived_decision_template.md`.
5. Crea el archivo dentro de `project_memory/decisions_archive/` con el nombre correcto.
6. Completa el front matter YAML mínimo.
7. Redacta:
   - decisión archivada
   - contexto breve
   - motivo de archivo
   - sustituida por o estado final
   - notas de trazabilidad
8. Actualiza `project_memory/DECISIONS.md` para que solo queden decisiones vigentes.
9. Actualiza `project_memory/decisions_archive/decisions_archive_index.md`.

---

## No hagas esto

- no archives una decisión que sigue vigente
- no dejes la decisión activa y archivada compitiendo en paralelo sin aclaración
- no conviertas el archivo archivado en un ensayo histórico largo
