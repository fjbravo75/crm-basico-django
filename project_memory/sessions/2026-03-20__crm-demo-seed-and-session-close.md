---
id: session-2026-03-20-02
date: 2026-03-20
type: session
status: closed
focus: "seed demo repetible del CRM, validacion real del flujo de listado y cierre documental local"
next_step: "abrir el microbloque corto del alta basica de clientes sobre el listado ya operativo"
---

# Seed demo del CRM y cierre documental local

## Estado al cierre

El repo queda con un management command de desarrollo para cargar datos demo del CRM de forma repetible y con el listado de clientes validado sobre datos reales cargados.

La base local queda con 3 empresas demo, 12 clientes demo, 5 interacciones demo y un usuario responsable reutilizable para el seed.

## Trabajo realizado

- Se creo `crm/management/commands/seed_demo_crm.py`.
- Se anadieron las carpetas de management command necesarias dentro de `crm`.
- Se definio un dataset estable con 3 empresas, 12 clientes y 5 interacciones.
- Se implemento reutilizacion de registros para evitar duplicados masivos al repetir el seed.
- Se creo o reutilizo el usuario demo `maria.ortega` como responsable de clientes e interacciones.
- Se ejecuto `./.venv/bin/python manage.py check` con resultado limpio.
- Se ejecuto `./.venv/bin/python manage.py seed_demo_crm` dos veces y la segunda ejecucion reutilizo todos los registros.
- Se verificaron por consola los conteos finales del bloque: 3 empresas, 12 clientes, 5 interacciones y 1 usuario demo.
- Se comprobo por HTTP real que `/` responde con clientes cargados y que `/?q=aurora` devuelve coincidencias existentes.

## Decisiones fijadas o confirmadas

- La carga de datos demo del CRM queda fijada mediante un management command especifico de desarrollo.
- El seed debe mantenerse pequeno, estable y repetible para apoyar validacion manual y continuidad tecnica.
- No se depende del admin para poblar datos demo base de este flujo.

## Pendiente inmediato

- No abrir todavia detalle de cliente ni CRUD completo.
- Mantener el siguiente bloque en alcance corto y centrado en clientes.
- Apoyar la continuidad sobre el listado ya operativo y la base demo disponible.

## Siguiente paso exacto

- Abrir el microbloque corto del alta basica de clientes sobre el listado ya operativo.
