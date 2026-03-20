from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from crm.models import Client, Company, Interaction


DEMO_USER = {
    "username": "maria.ortega",
    "email": "maria.ortega@demo-crm.example",
    "first_name": "Maria",
    "last_name": "Ortega",
}

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
    {
        "client_email": "diego.martin@auroratech.example",
        "interaction_type": Interaction.InteractionType.CALL,
        "interaction_date": "2026-03-03T10:00:00",
        "subject": "Primera llamada de diagnostico",
        "summary": "Se revisaron necesidades basicas del equipo y puntos de dolor del proceso comercial.",
        "next_step": "Preparar una demo corta centrada en pipeline y responsables.",
    },
    {
        "client_email": "marta.gil@auroratech.example",
        "interaction_type": Interaction.InteractionType.FOLLOW_UP,
        "interaction_date": "2026-03-05T09:30:00",
        "subject": "Seguimiento tras la propuesta inicial",
        "summary": "La cliente pidio ajustar el alcance para incluir solo el flujo comercial principal.",
        "next_step": "Enviar propuesta revisada con alcance reducido.",
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
        "client_email": "lucia.romero@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.MEETING,
        "interaction_date": "2026-03-10T12:00:00",
        "subject": "Reunion de descubrimiento",
        "summary": "Se identificaron oportunidades para ordenar seguimiento y proximos pasos del equipo.",
        "next_step": "Preparar ejemplo de seguimiento para clientes industriales.",
    },
    {
        "client_email": "ines.campos@nexoindustrial.example",
        "interaction_type": Interaction.InteractionType.NOTE,
        "interaction_date": "2026-03-14T18:00:00",
        "subject": "Validacion interna del presupuesto",
        "summary": "La directora financiera confirmo que el presupuesto encaja en el trimestre actual.",
        "next_step": "Coordinar arranque y recopilacion de requisitos iniciales.",
    },
]


class Command(BaseCommand):
    help = "Carga o actualiza un conjunto estable de datos demo del CRM."

    def handle(self, *args, **options):
        with transaction.atomic():
            owner, owner_created = self._get_or_create_owner()
            companies, company_counts = self._seed_companies()
            clients, client_counts = self._seed_clients(owner, companies)
            interaction_counts = self._seed_interactions(owner, clients)

        self.stdout.write(self.style.SUCCESS("Datos demo del CRM listos."))
        self.stdout.write(
            f"Responsable demo: {'creado' if owner_created else 'reutilizado'} ({owner.username})"
        )
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
        if created:
            owner.set_unusable_password()
            owner.save(update_fields=["password"])
        return owner, created

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

        for item in INTERACTIONS:
            interaction_date = timezone.make_aware(
                datetime.fromisoformat(item["interaction_date"]),
                timezone.get_current_timezone(),
            )
            _, created = Interaction.objects.update_or_create(
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
            counts["created" if created else "reused"] += 1

        return counts
