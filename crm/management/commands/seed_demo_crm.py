from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from crm.models import Client, Company, Interaction


DEMO_USER = {
    "username": "maria.ortega",
    "email": "maria.ortega@demo-crm.example",
    "first_name": "María",
    "last_name": "Ortega",
}
DEMO_PASSWORD = "DemoCRM123!"

COMPANIES = [
    {
        "name": "Aurora Tech Solutions",
        "industry": "Tecnologia",
        "website": "https://www.auroratech.example",
        "phone": "+34 910 100 200",
        "email": "contacto@auroratech.example",
        "city": "Madrid",
        "notes": "Empresa demo con foco en operaciones y tecnologia empresarial.",
    },
    {
        "name": "Costa Retail Group",
        "industry": "Retail",
        "website": "https://www.costaretail.example",
        "phone": "+34 960 200 300",
        "email": "hola@costaretail.example",
        "city": "Valencia",
        "notes": "Cadena comercial demo con equipos de expansion y marketing.",
    },
    {
        "name": "Nexo Industrial",
        "industry": "Industria",
        "website": "https://www.nexoindustrial.example",
        "phone": "+34 944 300 400",
        "email": "info@nexoindustrial.example",
        "city": "Bilbao",
        "notes": "Grupo industrial demo interesado en seguimiento comercial ordenado.",
    },
]

CLIENTS = [
    {
        "first_name": "Laura",
        "last_name": "Suarez",
        "email": "laura.suarez@auroratech.example",
        "phone": "+34 600 101 201",
        "position": "Directora de Operaciones",
        "company": "Aurora Tech Solutions",
        "status": Client.Status.LEAD,
        "source": Client.Source.WEBSITE,
        "notes": "Quiere mejorar la visibilidad del pipeline comercial.",
    },
    {
        "first_name": "Diego",
        "last_name": "Martin",
        "email": "diego.martin@auroratech.example",
        "phone": "+34 600 101 202",
        "position": "Responsable de TI",
        "company": "Aurora Tech Solutions",
        "status": Client.Status.CONTACTED,
        "source": Client.Source.REFERRAL,
        "notes": "Busca una herramienta simple para coordinar al equipo comercial.",
    },
    {
        "first_name": "Marta",
        "last_name": "Gil",
        "email": "marta.gil@auroratech.example",
        "phone": "+34 600 101 203",
        "position": "Gerente de Compras",
        "company": "Aurora Tech Solutions",
        "status": Client.Status.PROPOSAL,
        "source": Client.Source.EMAIL_CAMPAIGN,
        "notes": "Ha revisado una propuesta inicial y espera ajustes de alcance.",
    },
    {
        "first_name": "Pablo",
        "last_name": "Rios",
        "email": "pablo.rios@auroratech.example",
        "phone": "+34 600 101 204",
        "position": "Director General",
        "company": "Aurora Tech Solutions",
        "status": Client.Status.WON,
        "source": Client.Source.REFERRAL,
        "notes": "Cuenta demo cerrada como referencia positiva del pipeline.",
    },
    {
        "first_name": "Elena",
        "last_name": "Navarro",
        "email": "elena.navarro@costaretail.example",
        "phone": "+34 600 202 301",
        "position": "Responsable de Expansion",
        "company": "Costa Retail Group",
        "status": Client.Status.FOLLOW_UP,
        "source": Client.Source.SOCIAL_MEDIA,
        "notes": "Quiere ordenar el seguimiento de nuevas aperturas.",
    },
    {
        "first_name": "Sergio",
        "last_name": "Pena",
        "email": "sergio.pena@costaretail.example",
        "phone": "+34 600 202 302",
        "position": "Director Comercial",
        "company": "Costa Retail Group",
        "status": Client.Status.CONTACTED,
        "source": Client.Source.WEBSITE,
        "notes": "Comparando varias opciones antes de avanzar a demo interna.",
    },
    {
        "first_name": "Ana",
        "last_name": "Beltran",
        "email": "ana.beltran@costaretail.example",
        "phone": "+34 600 202 303",
        "position": "Coordinadora de Marketing",
        "company": "Costa Retail Group",
        "status": Client.Status.LEAD,
        "source": Client.Source.SOCIAL_MEDIA,
        "notes": "Interesada en centralizar leads de campanas digitales.",
    },
    {
        "first_name": "Victor",
        "last_name": "Lara",
        "email": "victor.lara@costaretail.example",
        "phone": "+34 600 202 304",
        "position": "Responsable de Operaciones",
        "company": "Costa Retail Group",
        "status": Client.Status.LOST,
        "source": Client.Source.REFERRAL,
        "notes": "Proyecto detenido por prioridad presupuestaria.",
    },
    {
        "first_name": "Lucia",
        "last_name": "Romero",
        "email": "lucia.romero@nexoindustrial.example",
        "phone": "+34 600 303 401",
        "position": "Jefa de Planta",
        "company": "Nexo Industrial",
        "status": Client.Status.PROPOSAL,
        "source": Client.Source.WEBSITE,
        "notes": "Quiere mejorar el seguimiento de oportunidades B2B.",
    },
    {
        "first_name": "Javier",
        "last_name": "Torres",
        "email": "javier.torres@nexoindustrial.example",
        "phone": "+34 600 303 402",
        "position": "Responsable de Calidad",
        "company": "Nexo Industrial",
        "status": Client.Status.FOLLOW_UP,
        "source": Client.Source.OTHER,
        "notes": "Recibio una recomendacion interna y pide una prueba guiada.",
    },
    {
        "first_name": "Ines",
        "last_name": "Campos",
        "email": "ines.campos@nexoindustrial.example",
        "phone": "+34 600 303 403",
        "position": "Directora Financiera",
        "company": "Nexo Industrial",
        "status": Client.Status.WON,
        "source": Client.Source.REFERRAL,
        "notes": "Cuenta demo ganada para representar cierres con decisores financieros.",
    },
    {
        "first_name": "Carlos",
        "last_name": "Vega",
        "email": "carlos.vega@nexoindustrial.example",
        "phone": "+34 600 303 404",
        "position": "Responsable de Logistica",
        "company": "Nexo Industrial",
        "status": Client.Status.LEAD,
        "source": Client.Source.EMAIL_CAMPAIGN,
        "notes": "Valora automatizar el seguimiento de contactos de ferias.",
    },
]

INTERACTIONS = [
    # Cliente principal para probar paginacion del bloque de actividad.
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-19T11:15:00",
        "subject": "Correo con informacion comercial resumida",
        "summary": (
            "Se envio un resumen claro de la propuesta comercial y del alcance inicial planteado para el equipo.\n\n"
            "Diego confirmo que el enfoque encaja mejor si se prioriza visibilidad del pipeline y seguimiento de proximos pasos."
        ),
        "next_step": "Preparar una demo corta con el flujo comercial principal.",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-18T16:30:00",
        "subject": "Llamada para revisar alcance inicial",
        "summary": "Se aclararon dudas sobre usuarios, responsables y nivel de detalle esperado en el seguimiento diario.",
        "next_step": "Enviar ejemplo simple de tablero comercial para la siguiente revision.",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.MEETING,
        "interaction_date": "2026-03-17T09:00:00",
        "subject": "Reunion breve de exploracion",
        "summary": (
            "El equipo compartio como registra hoy contactos, propuestas y seguimientos pendientes.\n\n"
            "Se vio una necesidad clara de centralizar notas y evitar que proximos pasos queden repartidos entre correo y hojas sueltas."
        ),
        "next_step": "Recoger dos casos reales para incluirlos en la demo guiada.",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-16T13:45:00",
        "subject": "Nota interna sobre objeciones del cliente",
        "summary": "La principal objecion sigue siendo el tiempo de adopcion del equipo y la carga inicial de datos.",
        "next_step": "",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.FOLLOW_UP,
        "interaction_date": "2026-03-14T10:20:00",
        "subject": "Seguimiento tras varios dias sin respuesta",
        "summary": (
            "Se contacto de nuevo para confirmar si el material enviado habia llegado al equipo responsable.\n\n"
            "Diego indico que necesitaba cerrar primero una revision interna antes de mover la conversacion a una demo mas formal."
        ),
        "next_step": "Retomar contacto a principios de la semana siguiente.",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-12T17:10:00",
        "subject": "Envio pendiente de propuesta ajustada",
        "summary": "Se compartio una version mas breve de la propuesta para facilitar una revision interna rapida.",
        "next_step": "Confirmar recepcion y resolver comentarios de alcance.",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-09T12:05:00",
        "subject": "Llamada inicial de presentacion",
        "summary": (
            "Se presento el CRM con foco en simplicidad, seguimiento y visibilidad comercial.\n\n"
            "El cliente comento que ahora mismo trabaja con correos, notas sueltas y una hoja compartida poco mantenible."
        ),
        "next_step": "",
    },
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-03T10:00:00",
        "subject": "Registro inicial de necesidades detectadas",
        "summary": (
            "Se dejaron anotadas las prioridades del equipo para no perder contexto antes de la primera demo.\n\n"
            "Las necesidades principales son orden, trazabilidad del contacto y seguimiento claro de responsables."
        ),
        "next_step": "Preparar guion comercial para la primera llamada de diagnostico.",
    },
    # Primer cliente visible del listado con historial suficiente para una demo rapida.
    {
        "client_email": "ana.beltran@costaretail.example",
        "interaction_type": Interaction.InteractionType.MEETING,
        "interaction_date": "2026-03-20T10:00:00",
        "subject": "Revision de leads activos de campanas recientes",
        "summary": (
            "Ana compartio como gestionan hoy los leads procedentes de redes y acciones promocionales.\n\n"
            "Se vio valor en tener historial y proximos pasos visibles sin salir del detalle del cliente."
        ),
        "next_step": "Preparar un recorrido de demo centrado en seguimiento de leads digitales.",
    },
    {
        "client_email": "ana.beltran@costaretail.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-18T17:20:00",
        "subject": "Correo con propuesta resumida para marketing",
        "summary": "Se envio una propuesta breve enfocada en ordenar contactos, actividad y responsables visibles.",
        "next_step": "Resolver dudas del equipo sobre la carga inicial de datos.",
    },
    {
        "client_email": "ana.beltran@costaretail.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-13T12:30:00",
        "subject": "Llamada sobre seguimiento de leads digitales",
        "summary": "Se reviso la necesidad de no perder contexto entre primera respuesta, seguimiento y cierre comercial.",
        "next_step": "Recoger dos ejemplos reales para la demo guiada.",
    },
    {
        "client_email": "ana.beltran@costaretail.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-10T09:10:00",
        "subject": "Nota interna sobre volumen irregular de captacion",
        "summary": "El volumen de leads cambia mucho segun la campana y complica priorizar bien cada oportunidad.",
        "next_step": "",
    },
    {
        "client_email": "ana.beltran@costaretail.example",
        "interaction_type": Interaction.InteractionType.FOLLOW_UP,
        "interaction_date": "2026-03-04T16:05:00",
        "subject": "Seguimiento tras compartir el enfoque inicial",
        "summary": "Se confirmo interes en una herramienta sobria, sin complejidad extra y util para equipo pequeno.",
        "next_step": "Retomar con una demo corta al inicio de la semana siguiente.",
    },
    # Segundo cliente demo con volumen suficiente para una paginacion corta.
    {
        "client_email": "lucia.romero@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.MEETING,
        "interaction_date": "2026-03-18T15:00:00",
        "subject": "Reunion de exploracion del proceso actual",
        "summary": (
            "Lucia describio un proceso comercial largo, con varios interlocutores y seguimiento irregular entre reuniones.\n\n"
            "Se acordo que la demo debe centrarse en como registrar actividad y proximos pasos sin complejidad adicional."
        ),
        "next_step": "Preparar ejemplo orientado a seguimiento industrial B2B.",
    },
    {
        "client_email": "lucia.romero@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-15T10:40:00",
        "subject": "Correo con casos de uso industriales",
        "summary": "Se compartieron ejemplos breves de seguimiento comercial aplicados a oportunidades con ciclo largo.",
        "next_step": "Verificar que los casos elegidos encajan con su operativa real.",
    },
    {
        "client_email": "lucia.romero@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.FOLLOW_UP,
        "interaction_date": "2026-03-11T18:20:00",
        "subject": "Seguimiento tras revisar la propuesta",
        "summary": "La cliente confirmo interes, pero pidio unos dias para revisar internamente prioridades del trimestre.",
        "next_step": "",
    },
    {
        "client_email": "lucia.romero@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-06T09:15:00",
        "subject": "Nota interna sobre prioridades del trimestre",
        "summary": "Se registro que el equipo valora rapidez de adopcion y una vista simple del historial de contacto.",
        "next_step": "Ajustar el discurso de demo a implantacion rapida y seguimiento claro.",
    },
    # Actividad ligera adicional para otros clientes demo ya presentes.
    {
        "client_email": "marta.gil@auroratech.example",
        "interaction_type": Interaction.InteractionType.FOLLOW_UP,
        "interaction_date": "2026-03-05T09:30:00",
        "subject": "Seguimiento tras la propuesta inicial",
        "summary": "La cliente pidio ajustar el alcance para incluir solo el flujo comercial principal.",
        "next_step": "Enviar propuesta revisada con alcance reducido.",
    },
    {
        "client_email": "marta.gil@auroratech.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-08T12:15:00",
        "subject": "Correo con cambios de alcance solicitados",
        "summary": "Se enviaron alternativas mas simples para facilitar una aprobacion interna rapida.",
        "next_step": "Confirmar si la propuesta revisada pasa a validacion final.",
    },
    {
        "client_email": "elena.navarro@costaretail.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-07T16:00:00",
        "subject": "Envio de propuesta inicial",
        "summary": "Se compartio un resumen del flujo de trabajo y casos de uso para expansion comercial.",
        "next_step": "Confirmar si el equipo quiere una demo con dos responsables de tienda.",
    },
    {
        "client_email": "elena.navarro@costaretail.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-12T11:10:00",
        "subject": "Llamada sobre nuevas aperturas y seguimiento",
        "summary": "Se reviso como registrar contactos de nuevos locales sin perder decisiones ni proximos pasos.",
        "next_step": "Compartir un ejemplo de seguimiento semanal por apertura.",
    },
    {
        "client_email": "ines.campos@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-14T18:00:00",
        "subject": "Validacion interna del presupuesto",
        "summary": "La directora financiera confirmo que el presupuesto encaja en el trimestre actual.",
        "next_step": "Coordinar arranque y recopilacion de requisitos iniciales.",
    },
    {
        "client_email": "ines.campos@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-10T13:10:00",
        "subject": "Correo con resumen ejecutivo para direccion",
        "summary": "Se compartio un resumen breve con coste, alcance y valor esperado para facilitar la aprobacion interna.",
        "next_step": "Resolver comentarios financieros antes del cierre.",
    },
    {
        "client_email": "laura.suarez@auroratech.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-06T10:25:00",
        "subject": "Correo inicial sobre visibilidad del pipeline",
        "summary": "Laura pidio una forma simple de seguir oportunidades activas sin depender de notas dispersas.",
        "next_step": "Preparar un ejemplo con responsables y estados visibles.",
    },
    {
        "client_email": "pablo.rios@auroratech.example",
        "interaction_type": Interaction.InteractionType.MEETING,
        "interaction_date": "2026-03-21T09:45:00",
        "subject": "Reunion de cierre y adopcion inicial",
        "summary": "Se repaso el valor esperado para direccion y una implantacion ligera orientada al flujo comercial principal.",
        "next_step": "Coordinar el arranque con un responsable operativo.",
    },
    {
        "client_email": "sergio.pena@costaretail.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-13T17:30:00",
        "subject": "Llamada comparativa entre opciones",
        "summary": "Sergio comparo varias herramientas y valoro especialmente la simplicidad de uso para el equipo comercial.",
        "next_step": "Enviar una demo resumida centrada en seguimiento diario.",
    },
    {
        "client_email": "victor.lara@costaretail.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-02T09:20:00",
        "subject": "Nota sobre parada temporal del proyecto",
        "summary": "La oportunidad quedo pausada por presupuesto, pero se mantuvo el contexto para una posible reactivacion.",
        "next_step": "Revisar de nuevo al inicio del siguiente trimestre.",
    },
    {
        "client_email": "javier.torres@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.EMAIL,
        "interaction_date": "2026-03-16T08:50:00",
        "subject": "Correo con propuesta de prueba guiada",
        "summary": "Se compartio una propuesta centrada en trazabilidad comercial y seguimiento ordenado para equipos pequenos.",
        "next_step": "Confirmar disponibilidad para una demo con dos responsables.",
    },
    {
        "client_email": "carlos.vega@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-07T12:40:00",
        "subject": "Llamada sobre seguimiento tras ferias",
        "summary": "Carlos explico la dificultad de mantener visibles los contactos captados en eventos y su seguimiento posterior.",
        "next_step": "Preparar ejemplo con origen, estado y proximos pasos.",
    },
]


class Command(BaseCommand):
    help = "Carga o actualiza un conjunto estable de datos demo del CRM."

    def handle(self, *args, **options):
        with transaction.atomic():
            owner, owner_created, password_ready = self._get_or_create_owner()
            companies, company_counts = self._seed_companies()
            clients, client_counts = self._seed_clients(owner, companies)
            interaction_counts = self._seed_interactions(owner, clients)

        self.stdout.write(self.style.SUCCESS("Datos demo del CRM listos."))
        self.stdout.write(
            f"Responsable demo: {'creado' if owner_created else 'reutilizado'} ({owner.username})"
        )
        self.stdout.write(
            "Acceso demo: "
            f"usuario {owner.username} | "
            f"contrasena {DEMO_PASSWORD} | "
            "ruta /acceso/login/"
        )
        if password_ready:
            self.stdout.write("La credencial demo ha quedado lista para iniciar sesion.")
        self.stdout.write(
            f"Empresas: {company_counts['created']} creadas, {company_counts['reused']} reutilizadas"
        )
        self.stdout.write(
            f"Clientes: {client_counts['created']} creados, {client_counts['reused']} reutilizados"
        )
        self.stdout.write(
            "Interacciones: "
            f"{interaction_counts['created']} creadas, "
            f"{interaction_counts['reused']} reutilizadas"
        )

    def _get_or_create_owner(self):
        user_model = get_user_model()
        owner, created = user_model.objects.get_or_create(
            username=DEMO_USER["username"],
            defaults={
                "email": DEMO_USER["email"],
                "first_name": DEMO_USER["first_name"],
                "last_name": DEMO_USER["last_name"],
                "is_active": True,
            },
        )
        updated_fields = []

        if owner.email != DEMO_USER["email"]:
            owner.email = DEMO_USER["email"]
            updated_fields.append("email")
        if owner.first_name != DEMO_USER["first_name"]:
            owner.first_name = DEMO_USER["first_name"]
            updated_fields.append("first_name")
        if owner.last_name != DEMO_USER["last_name"]:
            owner.last_name = DEMO_USER["last_name"]
            updated_fields.append("last_name")
        if not owner.is_active:
            owner.is_active = True
            updated_fields.append("is_active")
        if not owner.check_password(DEMO_PASSWORD):
            owner.set_password(DEMO_PASSWORD)
            updated_fields.append("password")

        if updated_fields:
            owner.save(update_fields=updated_fields)

        return owner, created, owner.check_password(DEMO_PASSWORD)

    def _seed_companies(self):
        companies = {}
        counts = {"created": 0, "reused": 0}

        for item in COMPANIES:
            company, created = Company.objects.update_or_create(
                name=item["name"],
                defaults={
                    "industry": item["industry"],
                    "website": item["website"],
                    "phone": item["phone"],
                    "email": item["email"],
                    "city": item["city"],
                    "notes": item["notes"],
                },
            )
            companies[item["name"]] = company
            counts["created" if created else "reused"] += 1

        return companies, counts

    def _seed_clients(self, owner, companies):
        clients = {}
        counts = {"created": 0, "reused": 0}

        for item in CLIENTS:
            client, created = Client.objects.update_or_create(
                email=item["email"],
                defaults={
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "phone": item["phone"],
                    "position": item["position"],
                    "company": companies[item["company"]],
                    "owner": owner,
                    "status": item["status"],
                    "source": item["source"],
                    "notes": item["notes"],
                },
            )
            clients[item["email"]] = client
            counts["created" if created else "reused"] += 1

        return clients, counts

    def _seed_interactions(self, owner, clients):
        counts = {"created": 0, "reused": 0}
        seeded_ids_by_client = {client_email: set() for client_email in clients}

        for item in INTERACTIONS:
            interaction_date = timezone.make_aware(
                datetime.fromisoformat(item["interaction_date"]),
                timezone.get_current_timezone(),
            )
            interaction, created = Interaction.objects.update_or_create(
                client=clients[item["client_email"]],
                interaction_type=item["interaction_type"],
                interaction_date=interaction_date,
                subject=item["subject"],
                defaults={
                    "created_by": owner,
                    "summary": item["summary"],
                    "next_step": item["next_step"],
                },
            )
            seeded_ids_by_client.setdefault(item["client_email"], set()).add(interaction.pk)
            counts["created" if created else "reused"] += 1

        for client_email, interaction_ids in seeded_ids_by_client.items():
            Interaction.objects.filter(client=clients[client_email]).exclude(pk__in=interaction_ids).delete()

        return counts
