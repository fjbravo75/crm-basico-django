# CRM Básico con Django

Aplicación web construida con Django para gestionar clientes y actividad comercial de una forma clara y fácil de seguir.  
En la interfaz, la aplicación se muestra como **Gestor de clientes**.

## Resumen

**CRM Básico** es una aplicación web desarrollada con Django para trabajar un flujo comercial pequeño pero realista sin añadir más complejidad de la necesaria.

La idea del proyecto es sencilla: cada usuario puede gestionar sus propios clientes, asociarlos a una empresa cuando corresponde y registrar actividad comercial desde la propia ficha del cliente. La intención no ha sido construir un CRM grande, sino una aplicación pequeña, seria y fácil de explicar.

Este proyecto me ha servido para practicar una parte muy útil de Django: modelos relacionados, vistas, formularios, validaciones, control de acceso básico, pruebas y cierre más limpio de una entrega.

## Qué permite hacer

La aplicación permite:

- registrarse, iniciar sesión y cerrar sesión
- crear, editar y eliminar clientes
- asociar cada cliente a una empresa existente o crear una nueva desde el propio formulario
- registrar, editar y eliminar actividad desde la ficha del cliente
- buscar clientes por nombre, correo o empresa
- limitar el acceso para que cada usuario solo vea y modifique sus propios clientes y su actividad asociada
- exportar en CSV el conjunto filtrado del listado principal
- consultar un mini dashboard de estados dentro del listado
- cargar una demo reproducible con un comando manual

He intentado mantener un alcance razonable: suficiente para que la aplicación tenga sentido de verdad, pero sin añadir funciones que luego costaría justificar o mantener.

## Stack utilizado

El proyecto está construido con una base directa:

- Python
- Django
- SQLite en local
- configuración preparada por entorno para PostgreSQL mediante `DATABASE_URL`
- plantillas HTML renderizadas en servidor
- CSS propio
- Gunicorn como runtime de aplicación para un despliegue posterior
- pruebas con `Django TestCase`

He preferido mantener el proyecto como una aplicación renderizada con Django, sin separar frontend ni abrir más capas de las que realmente hacían falta en esta etapa.

## Cómo ejecutar el proyecto en local

### 1. Clonar el repositorio

    git clone <URL_DEL_REPOSITORIO>
    cd crm-basico

### 2. Crear y activar un entorno virtual

En Linux o WSL:

    python -m venv .venv
    source .venv/bin/activate

En Windows:

    python -m venv .venv
    .venv\Scripts\activate

### 3. Instalar dependencias

    pip install -r requirements.txt

### 4. Crear el archivo de entorno

Puedes partir del archivo de ejemplo:

    cp .env.example .env

Si no se define una base de datos externa, el proyecto usará SQLite en local por defecto.

### 5. Aplicar migraciones

    python manage.py migrate

### 6. Cargar la demo opcional

Si quieres revisar la aplicación con contenido de ejemplo desde el principio:

    python manage.py seed_demo_crm

### 7. Arrancar el servidor

    python manage.py runserver

La aplicación quedará disponible en la dirección local habitual de Django. El acceso principal queda en:

    http://127.0.0.1:8000/acceso/login/

## Variables de entorno

El proyecto incluye un archivo `.env.example` con las variables principales:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `SHOW_DEMO_ACCESS`
- `ALLOW_PUBLIC_REGISTRATION`

Si `DATABASE_URL` no se define, la aplicación funciona con SQLite en local. Si existe, el proyecto pasa a PostgreSQL.

### Comportamiento de acceso según entorno

En local o con `DEBUG=True`, el acceso demo visible y el registro público quedan abiertos por defecto.

Con `DEBUG=False`, ambos quedan cerrados por defecto. Si hiciera falta ajustar ese comportamiento en un despliegue concreto, puede hacerse con `SHOW_DEMO_ACCESS` y `ALLOW_PUBLIC_REGISTRATION`.

## Demo reproducible

La aplicación incorpora este comando:

    python manage.py seed_demo_crm

Este comando crea o actualiza un espacio demo pensado para poder revisar la aplicación con contenido desde el principio. La demo incluye:

- 1 usuario demo
- 3 empresas
- 12 clientes
- 29 actividades

Por defecto, las credenciales demo son:

- usuario: `maria.ortega`
- contraseña: `DemoCRM123!`

Estas credenciales visibles están pensadas para revisión local. Con `DEBUG=False`, el acceso demo visible no queda expuesto por defecto.

## Tests

El proyecto incluye una suite de pruebas para validar el comportamiento principal de la aplicación. En el cierre actual se cubren bloques como:

- autenticación y registro
- seed demo
- CRUD de clientes
- CRUD de actividad
- ownership
- búsqueda
- paginación
- exportación CSV
- dashboard

Para ejecutar los tests:

    python manage.py test

También se puede hacer una comprobación básica del proyecto con:

    python manage.py check

## Estado actual del proyecto

A día de hoy, el proyecto queda cerrado como una entrega funcional en local, con una demo reproducible y una configuración de entorno más limpia que depender simplemente de una base de datos ya rellenada a mano.

Todavía no incluye un despliegue real completamente cerrado, ni permisos avanzados, ni una capa más grande de gestión comercial, porque ese no era el objetivo de esta fase. Lo que sí deja es un CRM pequeño pero serio, con un núcleo funcional bien resuelto y fácil de enseñar en GitHub.

## Aprendizajes

Este proyecto me ha servido para practicar una parte bastante útil de Django: construir una aplicación web con entidades relacionadas, controlar un flujo de trabajo real sobre clientes, registrar actividad, limitar el acceso por usuario y acompañar todo eso con pruebas.

También me ha ayudado a pensar mejor el cierre de una entrega. No solo en hacer que una funcionalidad exista, sino en dejar el proyecto más fácil de revisar, más claro de levantar en local y mejor preparado para seguir trabajando sobre él después.

He intentado que el resultado final no se quede solo en una práctica de curso, sino en un proyecto pequeño, serio y explicable, que pueda enseñar con naturalidad y defender con honestidad.