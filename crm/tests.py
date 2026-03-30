import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .management.commands.seed_demo_crm import COMPANIES, CLIENTS, DEMO_PASSWORD, DEMO_USER, INTERACTIONS
from .models import Client, Company, Interaction


class CRMBaseTestCase(TestCase):
    password = "testpass123"

    def create_user(self, username="responsable", first_name="", last_name=""):
        return get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=self.password,
        )

    def login_user(self, user=None):
        self.client.force_login(user or self.owner)

    def assert_login_redirect(self, response, target_url):
        self.assertRedirects(response, f"{reverse('login')}?next={target_url}")


class AuthenticationAccessTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")

    def test_login_view_renders_form_in_spanish(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Iniciar sesión")
        self.assertContains(response, "Acceso de demostración")
        self.assertContains(response, "Usuario")
        self.assertContains(response, "Contraseña")
        self.assertContains(response, DEMO_USER["username"])
        self.assertContains(response, DEMO_PASSWORD)
        self.assertContains(response, reverse("register"))

    def test_anonymous_user_is_redirected_to_login_from_client_list(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assert_login_redirect(response, reverse("crm:client_list"))

    def test_anonymous_post_to_client_create_does_not_create_client(self):
        response = self.client.post(
            reverse("crm:client_create"),
            data={
                "first_name": "Ana",
                "last_name": "Torres",
                "email": "ana.torres@example.com",
                "phone": "+34 600 000 001",
                "position": "Gerente Comercial",
                "company": self.company.pk,
                "status": Client.Status.LEAD,
                "source": Client.Source.REFERRAL,
                "notes": "Alta bloqueada por falta de autenticación.",
            },
        )

        self.assert_login_redirect(response, reverse("crm:client_create"))
        self.assertFalse(Client.objects.filter(email="ana.torres@example.com").exists())

    def test_login_view_authenticates_and_redirects_to_client_list(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.owner.username,
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("crm:client_list"))

        list_response = self.client.get(reverse("crm:client_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Clientes")
        self.assertContains(list_response, self.owner.get_username())
        self.assertContains(list_response, "Cerrar sesión")

    def test_logout_closes_session_and_redirects_to_login(self):
        self.assertTrue(
            self.client.login(
                username=self.owner.username,
                password=self.password,
            )
        )

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))

        protected_response = self.client.get(reverse("crm:client_list"))
        self.assert_login_redirect(protected_response, reverse("crm:client_list"))


class DemoSeedCommandTests(CRMBaseTestCase):
    def run_seed(self):
        stdout = StringIO()
        call_command("seed_demo_crm", stdout=stdout)
        return stdout.getvalue()

    def test_seed_creates_demo_user_with_known_credentials_and_accessible_data(self):
        output = self.run_seed()
        demo_user = get_user_model().objects.get(username=DEMO_USER["username"])
        owned_clients = list(Client.objects.filter(owner=demo_user).order_by("last_name", "first_name"))
        first_client = owned_clients[0]

        self.assertTrue(demo_user.has_usable_password())
        self.assertTrue(demo_user.check_password(DEMO_PASSWORD))
        self.assertEqual(demo_user.get_full_name(), "María Ortega")
        self.assertEqual(Company.objects.count(), len(COMPANIES))
        self.assertEqual(Client.objects.filter(owner=demo_user).count(), len(CLIENTS))
        self.assertEqual(Interaction.objects.filter(created_by=demo_user).count(), len(INTERACTIONS))
        self.assertEqual(len(owned_clients), len(CLIENTS))
        self.assertTrue(all(client.interactions.exists() for client in owned_clients))
        self.assertEqual(first_client.email, "ana.beltran@costaretail.example")
        self.assertGreaterEqual(first_client.interactions.count(), 5)
        self.assertIn(DEMO_USER["username"], output)
        self.assertIn(DEMO_PASSWORD, output)
        self.assertIn("/acceso/login/", output)

        login_response = self.client.post(
            reverse("login"),
            data={
                "username": DEMO_USER["username"],
                "password": DEMO_PASSWORD,
            },
        )

        self.assertRedirects(login_response, reverse("crm:client_list"))

        list_response = self.client.get(reverse("crm:client_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, demo_user.get_full_name())
        self.assertNotContains(list_response, demo_user.get_username())
        self.assertContains(list_response, "Diego")

    def test_seed_repairs_existing_demo_user_with_unusable_password_and_keeps_counts_stable(self):
        demo_user = get_user_model().objects.create_user(
            username=DEMO_USER["username"],
            email=DEMO_USER["email"],
            first_name=DEMO_USER["first_name"],
            last_name=DEMO_USER["last_name"],
            password="temporal-invalida-123",
        )
        demo_user.set_unusable_password()
        demo_user.save(update_fields=["password"])

        self.run_seed()
        demo_user.refresh_from_db()

        self.assertTrue(demo_user.has_usable_password())
        self.assertTrue(demo_user.check_password(DEMO_PASSWORD))
        self.assertEqual(Company.objects.count(), len(COMPANIES))
        self.assertEqual(Client.objects.count(), len(CLIENTS))
        self.assertEqual(Interaction.objects.count(), len(INTERACTIONS))

        stray_client = Client.objects.get(email="ana.beltran@costaretail.example")
        Interaction.objects.create(
            client=stray_client,
            created_by=demo_user,
            interaction_type=Interaction.InteractionType.NOTE,
            subject="Actividad temporal fuera del seed",
            summary="Esta actividad extra debe desaparecer al resembrar la demo.",
        )
        self.assertEqual(Interaction.objects.count(), len(INTERACTIONS) + 1)

        second_output = self.run_seed()

        self.assertEqual(Company.objects.count(), len(COMPANIES))
        self.assertEqual(Client.objects.count(), len(CLIENTS))
        self.assertEqual(Interaction.objects.count(), len(INTERACTIONS))
        self.assertIn("reutilizado", second_output)
        self.assertIn(DEMO_PASSWORD, second_output)

    def test_seed_keeps_initial_state_coherent_with_visible_activity(self):
        self.run_seed()
        demo_user = get_user_model().objects.get(username=DEMO_USER["username"])

        self.assertEqual(
            Client.objects.get(email="laura.suarez@auroratech.example").status,
            Client.Status.CONTACTED,
        )
        self.assertEqual(
            Client.objects.get(email="ana.beltran@costaretail.example").status,
            Client.Status.FOLLOW_UP,
        )
        self.assertEqual(
            Client.objects.get(email="carlos.vega@nexoindustrial.example").status,
            Client.Status.CONTACTED,
        )
        self.assertFalse(
            Client.objects.filter(owner=demo_user, status=Client.Status.LEAD)
            .filter(interactions__isnull=False)
            .exists()
        )


class RegistrationFlowTests(CRMBaseTestCase):
    registration_password = "ClaveTemporal123"

    def test_register_view_renders_form_for_anonymous_user(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "Crear cuenta")
        self.assertContains(response, "Crea tu cuenta")
        self.assertContains(response, "Nombre")
        self.assertContains(response, "Apellidos")
        self.assertContains(response, reverse("login"))

    def test_register_valid_post_creates_user_logs_them_in_and_redirects(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "Laura",
                "last_name": "Serrano",
                "username": "nuevo-comercial",
                "password1": self.registration_password,
                "password2": self.registration_password,
            },
        )

        self.assertRedirects(response, reverse("crm:client_list"))

        user = get_user_model().objects.get(username="nuevo-comercial")
        self.assertEqual(user.first_name, "Laura")
        self.assertEqual(user.last_name, "Serrano")
        self.assertEqual(str(user.pk), self.client.session.get("_auth_user_id"))

        list_response = self.client.get(reverse("crm:client_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, user.get_full_name())
        self.assertContains(list_response, "Cerrar sesión")

    def test_register_requires_first_name_and_last_name(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "",
                "last_name": "",
                "username": "nuevo-comercial",
                "password1": self.registration_password,
                "password2": self.registration_password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Escribe tu nombre para crear la cuenta.")
        self.assertContains(response, "Escribe tus apellidos para crear la cuenta.")
        self.assertFalse(get_user_model().objects.filter(username="nuevo-comercial").exists())

    def test_register_invalid_post_shows_errors_and_does_not_create_user(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "Laura",
                "last_name": "Serrano",
                "username": "nuevo-comercial",
                "password1": self.registration_password,
                "password2": "otra-clave-123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Las contraseñas no coinciden")
        self.assertFalse(get_user_model().objects.filter(username="nuevo-comercial").exists())

    def test_register_rejects_username_longer_than_thirty_characters(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "Laura",
                "last_name": "Serrano",
                "username": "usuario-demo-demasiado-largo-31",
                "password1": self.registration_password,
                "password2": self.registration_password,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "El usuario no puede superar los 30 caracteres.")
        self.assertFalse(get_user_model().objects.filter(username="usuario-demo-demasiado-largo-31").exists())

    def test_authenticated_user_is_redirected_from_register_to_client_list(self):
        self.owner = self.create_user()
        self.login_user()

        response = self.client.get(reverse("register"))

        self.assertRedirects(response, reverse("crm:client_list"))


class ClientCreateFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.login_user()

    def test_client_list_shows_link_to_create_view(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nuevo cliente")
        self.assertContains(response, reverse("crm:client_create"))

    def test_client_create_form_shows_initial_status_label(self):
        response = self.client.get(reverse("crm:client_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inicial")
        self.assertContains(response, "Empresa existente")
        self.assertContains(response, "Nueva empresa")
        self.assertNotContains(response, "Prospecto")
        self.assertNotContains(response, "Sin contactar")

    def test_create_client_redirects_to_list_and_shows_new_entry(self):
        response = self.client.post(
            reverse("crm:client_create"),
            data={
                "first_name": "Ana",
                "last_name": "Torres",
                "email": "ana.torres@example.com",
                "phone": "+34 600 000 001",
                "position": "Gerente Comercial",
                "company": self.company.pk,
                "status": Client.Status.LEAD,
                "source": Client.Source.REFERRAL,
                "notes": "Alta basica desde el formulario.",
            },
        )

        self.assertRedirects(response, reverse("crm:client_list"))

        client = Client.objects.get(email="ana.torres@example.com")
        self.assertEqual(client.owner, self.owner)
        self.assertEqual(client.company, self.company)

        list_response = self.client.get(reverse("crm:client_list"))
        self.assertContains(list_response, "Ana")
        self.assertContains(list_response, "Torres")

    def test_create_client_with_new_company_creates_and_assigns_company(self):
        response = self.client.post(
            reverse("crm:client_create"),
            data={
                "first_name": "Nora",
                "last_name": "Sanz",
                "email": "nora.sanz@example.com",
                "phone": "+34 600 000 010",
                "position": "Comercial",
                "company": "",
                "new_company_name": "Nueva Empresa CRM",
                "status": Client.Status.LEAD,
                "source": "",
                "notes": "",
            },
        )

        self.assertRedirects(response, reverse("crm:client_list"))

        company = Company.objects.get(name="Nueva Empresa CRM")
        client = Client.objects.get(email="nora.sanz@example.com")
        self.assertEqual(client.company, company)

    def test_create_client_reuses_existing_company_when_new_company_matches(self):
        response = self.client.post(
            reverse("crm:client_create"),
            data={
                "first_name": "Eva",
                "last_name": "Lopez",
                "email": "eva.lopez@example.com",
                "phone": "+34 600 000 011",
                "position": "Comercial",
                "company": "",
                "new_company_name": "  Empresa Demo  ",
                "status": Client.Status.CONTACTED,
                "source": "",
                "notes": "",
            },
        )

        self.assertRedirects(response, reverse("crm:client_list"))
        self.assertEqual(Company.objects.filter(name__iexact="Empresa Demo").count(), 1)
        self.assertEqual(
            Client.objects.get(email="eva.lopez@example.com").company,
            self.company,
        )

    def test_create_client_form_rejects_existing_and_new_company_at_same_time(self):
        response = self.client.post(
            reverse("crm:client_create"),
            data={
                "first_name": "Sara",
                "last_name": "Mora",
                "email": "sara.mora@example.com",
                "phone": "+34 600 000 012",
                "position": "Comercial",
                "company": self.company.pk,
                "new_company_name": "Otra Empresa",
                "status": Client.Status.LEAD,
                "source": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usa solo una de las dos opciones de empresa.")
        self.assertFalse(Client.objects.filter(email="sara.mora@example.com").exists())


class ClientDetailFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
            source=Client.Source.REFERRAL,
            notes="Quiere revisar una demo corta antes de tomar una decisión.",
        )
        self.login_user()

    def test_client_list_shows_link_to_detail_view(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("crm:client_detail", args=[self.client_record.pk]))
        self.assertContains(response, "Ver detalle")

    def test_client_detail_view_shows_main_client_information(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lucia")
        self.assertContains(response, "Martinez")
        self.assertContains(response, "lucia.martinez@example.com")
        self.assertContains(response, "+34 600 000 002")
        self.assertContains(response, "Empresa Demo")
        self.assertContains(response, "Directora Comercial")
        self.assertContains(response, "Contactado")
        self.assertContains(response, "Origen")
        self.assertContains(response, "Referencia")
        self.assertContains(response, "Notas")
        self.assertContains(response, "Quiere revisar una demo corta antes de tomar una decisión.")
        self.assertContains(response, self.owner.get_username())

    def test_client_list_and_detail_render_initial_label_for_lead_status(self):
        self.client_record.status = Client.Status.LEAD
        self.client_record.save(update_fields=["status"])

        list_response = self.client.get(reverse("crm:client_list"))
        detail_response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertContains(list_response, "Inicial")
        self.assertNotContains(list_response, "Prospecto")
        self.assertNotContains(list_response, "Sin contactar")
        self.assertContains(detail_response, "Inicial")
        self.assertNotContains(detail_response, "Prospecto")
        self.assertNotContains(detail_response, "Sin contactar")

    def test_client_detail_shows_discrete_empty_state_for_source_and_notes(self):
        self.client_record.source = ""
        self.client_record.notes = ""
        self.client_record.save(update_fields=["source", "notes"])

        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Origen")
        self.assertContains(response, "Sin especificar")
        self.assertContains(response, "Notas")
        self.assertContains(response, "Sin notas registradas.")


class HumanDisplayTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user(
            username="maria.ortega",
            first_name="María",
            last_name="Ortega",
        )
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Ana",
            last_name="Torres",
            email="ana.torres@example.com",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.interaction = Interaction.objects.create(
            client=self.client_record,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="Correo demo",
            summary="Actividad registrada para validar nombre visible.",
        )
        self.login_user()

    def test_client_list_shows_human_name_in_header_and_responsible_field(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sesión iniciada como María Ortega")
        self.assertContains(response, "María Ortega")
        self.assertNotContains(response, self.owner.username)

    def test_client_detail_shows_human_name_for_owner_and_activity_author(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "María Ortega")
        self.assertContains(response, "Registrada por María Ortega")
        self.assertNotContains(response, self.owner.username)


class ClientUpdateFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.other_company = Company.objects.create(name="Empresa Actualizada")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.login_user()

    def test_client_detail_shows_link_to_update_view(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("crm:client_update", args=[self.client_record.pk]))
        self.assertContains(response, "Editar cliente")

    def test_update_view_loads_prepopulated_form(self):
        response = self.client.get(reverse("crm:client_update", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar cliente")
        self.assertContains(response, "Empresa existente")
        self.assertContains(response, "Nueva empresa")
        self.assertContains(response, 'value="Lucia"')
        self.assertContains(response, 'value="Martinez"')
        self.assertContains(response, 'value="lucia.martinez@example.com"')

    def test_update_view_saves_changes_and_redirects_to_detail(self):
        response = self.client.post(
            reverse("crm:client_update", args=[self.client_record.pk]),
            data={
                "first_name": "Lucia",
                "last_name": "Serrano",
                "email": "lucia.serrano@example.com",
                "phone": "+34 600 000 099",
                "position": "Directora de Ventas",
                "company": self.other_company.pk,
                "status": Client.Status.PROPOSAL,
                "source": Client.Source.REFERRAL,
                "notes": "Cliente actualizado desde el formulario de edición.",
            },
        )

        self.assertRedirects(response, reverse("crm:client_detail", args=[self.client_record.pk]))

        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.last_name, "Serrano")
        self.assertEqual(self.client_record.email, "lucia.serrano@example.com")
        self.assertEqual(self.client_record.phone, "+34 600 000 099")
        self.assertEqual(self.client_record.position, "Directora de Ventas")
        self.assertEqual(self.client_record.company, self.other_company)
        self.assertEqual(self.client_record.status, Client.Status.PROPOSAL)

    def test_update_view_rerenders_form_with_errors(self):
        response = self.client.post(
            reverse("crm:client_update", args=[self.client_record.pk]),
            data={
                "first_name": "",
                "last_name": "Martinez",
                "email": "lucia.martinez@example.com",
                "phone": "+34 600 000 002",
                "position": "Directora Comercial",
                "company": self.company.pk,
                "status": Client.Status.CONTACTED,
                "source": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.first_name, "Lucia")

    def test_update_view_can_replace_company_with_new_company_name(self):
        response = self.client.post(
            reverse("crm:client_update", args=[self.client_record.pk]),
            data={
                "first_name": "Lucia",
                "last_name": "Martinez",
                "email": "lucia.martinez@example.com",
                "phone": "+34 600 000 002",
                "position": "Directora Comercial",
                "company": "",
                "new_company_name": "Empresa Nueva Editada",
                "status": Client.Status.CONTACTED,
                "source": "",
                "notes": "",
            },
        )

        self.assertRedirects(response, reverse("crm:client_detail", args=[self.client_record.pk]))

        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.company.name, "Empresa Nueva Editada")


class ClientDeleteFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.interaction = Interaction.objects.create(
            client=self.client_record,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.CALL,
            subject="Llamada inicial",
            summary="Seguimiento básico asociado al cliente.",
        )
        self.login_user()

    def test_client_detail_shows_link_to_delete_view(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("crm:client_delete", args=[self.client_record.pk]))
        self.assertContains(response, "Eliminar cliente")

    def test_delete_confirmation_view_shows_client_and_cancel_link(self):
        response = self.client.get(reverse("crm:client_delete", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eliminar cliente")
        self.assertContains(response, "Lucia Martinez")
        self.assertContains(response, reverse("crm:client_detail", args=[self.client_record.pk]))
        self.assertEqual(Client.objects.count(), 1)

    def test_delete_view_removes_client_and_redirects_to_list(self):
        response = self.client.post(reverse("crm:client_delete", args=[self.client_record.pk]))

        self.assertRedirects(response, reverse("crm:client_list"))
        self.assertFalse(Client.objects.filter(pk=self.client_record.pk).exists())
        self.assertFalse(Interaction.objects.filter(pk=self.interaction.pk).exists())


class OwnershipAccessTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.other_user = self.create_user(username="otro-responsable")
        self.company = Company.objects.create(name="Empresa Demo")
        self.owned_client = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.foreign_client = Client.objects.create(
            first_name="Carlos",
            last_name="Vega",
            email="carlos.vega@example.com",
            company=self.company,
            owner=self.other_user,
            status=Client.Status.LEAD,
        )
        self.owned_interaction = Interaction.objects.create(
            client=self.owned_client,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="Correo propio",
            summary="Resumen propio.",
        )
        self.foreign_interaction = Interaction.objects.create(
            client=self.foreign_client,
            created_by=self.other_user,
            interaction_type=Interaction.InteractionType.CALL,
            subject="Llamada ajena",
            summary="Resumen ajeno.",
        )
        self.login_user()

    def test_client_list_only_shows_clients_owned_by_authenticated_user(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["clients"]), [self.owned_client])
        self.assertContains(response, "Lucia")
        self.assertNotContains(response, "Carlos")
        self.assertContains(response, "1 cliente disponible")

    def test_user_cannot_access_detail_of_foreign_client(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.foreign_client.pk]))

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_access_update_view_of_foreign_client(self):
        response = self.client.get(reverse("crm:client_update", args=[self.foreign_client.pk]))

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_access_delete_view_of_foreign_client(self):
        response = self.client.get(reverse("crm:client_delete", args=[self.foreign_client.pk]))

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_foreign_client(self):
        response = self.client.post(reverse("crm:client_delete", args=[self.foreign_client.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Client.objects.filter(pk=self.foreign_client.pk).exists())

    def test_user_cannot_create_activity_for_foreign_client(self):
        response = self.client.post(
            reverse("crm:interaction_create", args=[self.foreign_client.pk]),
            data={
                "interaction_type": Interaction.InteractionType.NOTE,
                "subject": "Intento ajeno",
                "summary": "No debería guardarse.",
                "next_step": "",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            Interaction.objects.filter(client=self.foreign_client).count(),
            1,
        )

    def test_user_cannot_access_update_view_for_activity_of_foreign_client(self):
        response = self.client.get(
            reverse("crm:interaction_update", args=[self.foreign_client.pk, self.foreign_interaction.pk]),
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_activity_of_foreign_client(self):
        response = self.client.post(
            reverse("crm:interaction_delete", args=[self.foreign_client.pk, self.foreign_interaction.pk]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Interaction.objects.filter(pk=self.foreign_interaction.pk).exists())


class ClientListPaginationTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")

        for index in range(7):
            Client.objects.create(
                first_name=f"Cliente{index}",
                last_name=f"Apellido{index}",
                email=f"cliente{index}@example.com",
                company=self.company,
                owner=self.owner,
                status=Client.Status.LEAD,
            )

        for index in range(6):
            Client.objects.create(
                first_name=f"Filtro{index}",
                last_name=f"Busqueda{index}",
                email=f"filtro{index}@example.com",
                company=self.company,
                owner=self.owner,
                status=Client.Status.CONTACTED,
            )

        Client.objects.create(
            first_name="Otro",
            last_name="Registro",
            email="otro@example.com",
            company=self.company,
            owner=self.owner,
            status=Client.Status.WON,
        )
        self.login_user()

    def test_client_list_paginates_to_five_items_per_page(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 5)
        self.assertEqual(response.context["paginator"].per_page, 5)
        self.assertContains(response, "14 clientes disponibles")

    def test_second_page_shows_remaining_results(self):
        response = self.client.get(reverse("crm:client_list"), {"page": 3})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 4)
        self.assertContains(response, "Página 3 de 3")

    def test_search_keeps_working_with_pagination(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 5)
        self.assertEqual(response.context["paginator"].count, 6)
        self.assertContains(response, '6 clientes encontrados para "Filtro"')

    def test_pagination_links_keep_search_query(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?q=Filtro&page=2")

    def test_results_text_uses_total_count_not_page_length(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '6 clientes encontrados para "Filtro"')
        self.assertNotContains(response, '5 clientes encontrados para "Filtro"')


class ClientListCsvExportTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user(
            username="maria.ortega",
            first_name="María",
            last_name="Ortega",
        )
        self.other_user = self.create_user(
            username="otro-responsable",
            first_name="Carlos",
            last_name="López",
        )
        self.company = Company.objects.create(name="Empresa Demo")
        self.other_company = Company.objects.create(name="Otra Empresa")

        for index in range(6):
            Client.objects.create(
                first_name=f"Filtro{index}",
                last_name="Busqueda",
                email=f"filtro{index}@example.com",
                phone=f"+34 600 000 10{index}",
                position="Comercial",
                company=self.company,
                owner=self.owner,
                status=Client.Status.CONTACTED,
                source=Client.Source.REFERRAL,
            )

        self.special_client = Client.objects.create(
            first_name="Laura",
            last_name="Torres",
            email="laura.torres@example.com",
            phone="+34 600 000 200",
            position="Directora Comercial",
            company=self.other_company,
            owner=self.owner,
            status=Client.Status.PROPOSAL,
            source=Client.Source.SOCIAL_MEDIA,
        )
        self.foreign_client = Client.objects.create(
            first_name="Carlos",
            last_name="Ajeno",
            email="carlos.ajeno@example.com",
            phone="+34 600 999 999",
            position="Gerente",
            company=self.other_company,
            owner=self.other_user,
            status=Client.Status.WON,
            source=Client.Source.WEBSITE,
        )
        self.login_user()

    def parse_csv_rows(self, response):
        content = response.content.decode("utf-8")
        return list(csv.reader(StringIO(content)))

    def test_client_list_shows_csv_export_link_in_results_row(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Exportar resultados en CSV")
        self.assertContains(response, "?q=Filtro&amp;export=csv")

    def test_csv_export_downloads_owned_clients_with_expected_columns(self):
        response = self.client.get(reverse("crm:client_list"), {"export": "csv"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn('attachment; filename="clientes.csv"', response["Content-Disposition"])

        rows = self.parse_csv_rows(response)

        self.assertEqual(
            rows[0],
            [
                "Nombre",
                "Apellidos",
                "Correo",
                "Teléfono",
                "Empresa",
                "Cargo",
                "Estado",
                "Origen",
                "Responsable",
                "Fecha de creación",
                "Última actualización",
            ],
        )
        self.assertEqual(len(rows) - 1, 7)
        exported_emails = [row[2] for row in rows[1:]]
        self.assertIn("laura.torres@example.com", exported_emails)
        self.assertNotIn("carlos.ajeno@example.com", exported_emails)

        special_row = next(row for row in rows[1:] if row[2] == "laura.torres@example.com")
        self.assertEqual(special_row[4], "Otra Empresa")
        self.assertEqual(special_row[5], "Directora Comercial")
        self.assertEqual(special_row[6], "Propuesta")
        self.assertEqual(special_row[7], "Redes sociales")
        self.assertEqual(special_row[8], "María Ortega")

    def test_csv_export_respects_search_query_filter(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro", "export": "csv"})

        self.assertEqual(response.status_code, 200)
        rows = self.parse_csv_rows(response)
        exported_emails = [row[2] for row in rows[1:]]

        self.assertEqual(len(rows) - 1, 6)
        self.assertTrue(all(email.startswith("filtro") for email in exported_emails))
        self.assertNotIn("laura.torres@example.com", exported_emails)

    def test_csv_export_ignores_current_page_and_exports_full_filtered_set(self):
        response = self.client.get(
            reverse("crm:client_list"),
            {"q": "Filtro", "page": 2, "export": "csv"},
        )

        self.assertEqual(response.status_code, 200)
        rows = self.parse_csv_rows(response)

        self.assertEqual(len(rows) - 1, 6)

    def test_csv_export_uses_initial_label_for_lead_status(self):
        Client.objects.create(
            first_name="Nora",
            last_name="Inicial",
            email="nora.inicial@example.com",
            phone="+34 600 123 123",
            position="Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.LEAD,
            source=Client.Source.WEBSITE,
        )

        response = self.client.get(reverse("crm:client_list"), {"export": "csv"})
        rows = self.parse_csv_rows(response)

        lead_row = next(row for row in rows[1:] if row[2] == "nora.inicial@example.com")
        self.assertEqual(lead_row[6], "Inicial")


class ClientListDashboardStatsTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user(
            username="maria.ortega",
            first_name="María",
            last_name="Ortega",
        )
        self.other_user = self.create_user(
            username="otro-responsable",
            first_name="Carlos",
            last_name="López",
        )
        self.base_company = Company.objects.create(name="Empresa General")
        self.filter_company = Company.objects.create(name="Empresa Filtro")

        for first_name, status in (
            ("Alicia", Client.Status.LEAD),
            ("Bruno", Client.Status.WON),
            ("Celia", Client.Status.LOST),
        ):
            Client.objects.create(
                first_name=first_name,
                last_name="Base",
                email=f"{first_name.lower()}@example.com",
                company=self.base_company,
                owner=self.owner,
                status=status,
            )

        for first_name, status in (
            ("Laura", Client.Status.LEAD),
            ("Marta", Client.Status.CONTACTED),
            ("Noa", Client.Status.FOLLOW_UP),
            ("Olga", Client.Status.PROPOSAL),
            ("Paula", Client.Status.PROPOSAL),
            ("Rocio", Client.Status.WON),
        ):
            Client.objects.create(
                first_name=first_name,
                last_name="Filtro",
                email=f"{first_name.lower()}.filtro@example.com",
                company=self.filter_company,
                owner=self.owner,
                status=status,
            )

        Client.objects.create(
            first_name="Xavier",
            last_name="Ajeno",
            email="xavier.ajeno@example.com",
            company=self.filter_company,
            owner=self.other_user,
            status=Client.Status.LOST,
        )
        self.login_user()

    def get_dashboard_kpis(self, response):
        return {item["label"]: item["value"] for item in response.context["dashboard_kpis"]}

    def get_status_distribution(self, response):
        return {
            item["status"]: item
            for item in response.context["dashboard_status_distribution"]
        }

    def test_client_list_renders_dashboard_with_expected_texts(self):
        response = self.client.get(reverse("crm:client_list"))
        distribution = self.get_status_distribution(response)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["show_client_dashboard"])
        self.assertEqual(
            [item["label"] for item in response.context["dashboard_kpis"]],
            ["Total fichas", "Abiertas", "Ganadas", "Perdidas"],
        )
        self.assertEqual(distribution["lead"]["label"], "Inicial")
        self.assertContains(response, "Total fichas")
        self.assertContains(response, "Abiertas")
        self.assertContains(response, "Ganadas")
        self.assertContains(response, "Perdidas")
        self.assertContains(response, "Inicial")
        self.assertContains(response, "Clientes por estado")

    def test_dashboard_kpis_use_exact_counts_for_current_queryset(self):
        response = self.client.get(reverse("crm:client_list"))
        kpis = self.get_dashboard_kpis(response)

        self.assertEqual(kpis["Total fichas"], 9)
        self.assertEqual(kpis["Abiertas"], 6)
        self.assertEqual(kpis["Ganadas"], 2)
        self.assertEqual(kpis["Perdidas"], 1)
        self.assertEqual(
            kpis["Abiertas"] + kpis["Ganadas"] + kpis["Perdidas"],
            kpis["Total fichas"],
        )

    def test_dashboard_distribution_respects_ownership(self):
        response = self.client.get(reverse("crm:client_list"))
        distribution = self.get_status_distribution(response)

        self.assertEqual(distribution["lead"]["count"], 2)
        self.assertEqual(distribution["contacted"]["count"], 1)
        self.assertEqual(distribution["follow_up"]["count"], 1)
        self.assertEqual(distribution["proposal"]["count"], 2)
        self.assertEqual(distribution["won"]["count"], 2)
        self.assertEqual(distribution["lost"]["count"], 1)
        self.assertEqual(distribution["proposal"]["bar_width"], 100)
        self.assertEqual(distribution["lost"]["bar_width"], 50)

    def test_dashboard_distribution_follows_search_query(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro"})
        kpis = self.get_dashboard_kpis(response)
        distribution = self.get_status_distribution(response)

        self.assertEqual(kpis["Total fichas"], 6)
        self.assertEqual(kpis["Abiertas"], 5)
        self.assertEqual(kpis["Ganadas"], 1)
        self.assertEqual(kpis["Perdidas"], 0)
        self.assertEqual(
            kpis["Abiertas"] + kpis["Ganadas"] + kpis["Perdidas"],
            kpis["Total fichas"],
        )
        self.assertEqual(distribution["lead"]["count"], 1)
        self.assertEqual(distribution["contacted"]["count"], 1)
        self.assertEqual(distribution["follow_up"]["count"], 1)
        self.assertEqual(distribution["proposal"]["count"], 2)
        self.assertEqual(distribution["won"]["count"], 1)
        self.assertEqual(distribution["lost"]["count"], 0)
        self.assertEqual(distribution["proposal"]["bar_width"], 100)
        self.assertEqual(distribution["lead"]["bar_width"], 50)

    def test_dashboard_uses_full_filtered_queryset_not_current_page(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Filtro", "page": 2})
        kpis = self.get_dashboard_kpis(response)
        distribution = self.get_status_distribution(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clients"]), 1)
        self.assertEqual(kpis["Total fichas"], 6)
        self.assertEqual(kpis["Abiertas"], 5)
        self.assertEqual(kpis["Ganadas"], 1)
        self.assertEqual(kpis["Perdidas"], 0)
        self.assertEqual(distribution["proposal"]["count"], 2)
        self.assertEqual(distribution["lost"]["count"], 0)

    def test_dashboard_is_hidden_when_filtered_queryset_is_empty(self):
        response = self.client.get(reverse("crm:client_list"), {"q": "Sin coincidencias"})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["show_client_dashboard"])
        self.assertEqual(response.context["dashboard_kpis"], [])
        self.assertEqual(response.context["dashboard_status_distribution"], [])
        self.assertNotContains(response, "Total fichas")
        self.assertNotContains(response, "Abiertas")
        self.assertNotContains(response, "Ganadas")
        self.assertNotContains(response, "Perdidas")
        self.assertNotContains(response, "Clientes por estado")


class InteractionCreateFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.login_user()

    def test_client_detail_shows_empty_state_and_register_link(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Actividad")
        self.assertContains(response, "Todavía no hay actividad registrada.")
        self.assertContains(response, reverse("crm:interaction_create", args=[self.client_record.pk]))

    def test_client_detail_lists_existing_interactions(self):
        Interaction.objects.create(
            client=self.client_record,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.CALL,
            subject="Llamada inicial",
            summary="Se revisaron los próximos pasos del cliente.",
            next_step="Enviar resumen por correo.",
        )

        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Llamada")
        self.assertContains(response, "Llamada inicial")
        self.assertContains(response, "Se revisaron los próximos pasos del cliente.")
        self.assertContains(response, "Próximo paso:")
        self.assertContains(response, "Enviar resumen por correo.")

    def test_interaction_create_view_creates_record_and_redirects_to_client_detail(self):
        response = self.client.post(
            reverse("crm:interaction_create", args=[self.client_record.pk]),
            data={
                "interaction_type": Interaction.InteractionType.EMAIL,
                "subject": "Correo de seguimiento",
                "summary": "Se confirmó el interés en continuar con la propuesta.",
                "next_step": "Preparar una demo corta.",
            },
        )

        self.assertRedirects(response, reverse("crm:client_detail", args=[self.client_record.pk]))

        interaction = Interaction.objects.get(subject="Correo de seguimiento")
        self.assertEqual(interaction.client, self.client_record)
        self.assertEqual(interaction.created_by, self.owner)

        detail_response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))
        self.assertContains(detail_response, "Correo de seguimiento")

    def test_interaction_create_view_rerenders_form_with_errors(self):
        response = self.client.post(
            reverse("crm:interaction_create", args=[self.client_record.pk]),
            data={
                "interaction_type": Interaction.InteractionType.NOTE,
                "subject": "",
                "summary": "",
                "next_step": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Interaction.objects.count(), 0)

    def test_client_detail_paginates_activity_to_three_items(self):
        for index in range(4):
            Interaction.objects.create(
                client=self.client_record,
                created_by=self.owner,
                interaction_type=Interaction.InteractionType.NOTE,
                subject=f"Actividad {index + 1}",
                summary=f"Resumen {index + 1}",
                interaction_date=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["activity_page_obj"].object_list), 3)
        self.assertEqual(response.context["activity_page_obj"].paginator.per_page, 3)
        self.assertContains(response, "Página 1 de 2")
        self.assertContains(response, "Actividad 4")
        self.assertContains(response, "Actividad 3")
        self.assertContains(response, "Actividad 2")
        self.assertNotContains(response, "Actividad 1")

    def test_client_detail_second_activity_page_shows_remaining_records(self):
        for index in range(4):
            Interaction.objects.create(
                client=self.client_record,
                created_by=self.owner,
                interaction_type=Interaction.InteractionType.NOTE,
                subject=f"Seguimiento {index + 1}",
                summary=f"Resumen {index + 1}",
                interaction_date=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(
            reverse("crm:client_detail", args=[self.client_record.pk]),
            {"activity_page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["activity_page_obj"].number, 2)
        self.assertContains(response, "Página 2 de 2")
        self.assertContains(response, "Seguimiento 1")
        self.assertNotContains(response, "Seguimiento 4")

    def test_activity_pagination_keeps_other_query_parameters(self):
        for index in range(4):
            Interaction.objects.create(
                client=self.client_record,
                created_by=self.owner,
                interaction_type=Interaction.InteractionType.EMAIL,
                subject=f"Correo {index + 1}",
                summary=f"Resumen {index + 1}",
                interaction_date=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(
            reverse("crm:client_detail", args=[self.client_record.pk]),
            {"source": "demo"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?source=demo&amp;activity_page=2")


class InteractionUpdateFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.interaction = Interaction.objects.create(
            client=self.client_record,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="Correo inicial",
            summary="Resumen inicial de la actividad.",
            next_step="Enviar documentación actualizada.",
        )
        self.login_user()

    def test_client_detail_shows_link_to_update_view_for_each_interaction(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("crm:interaction_update", args=[self.client_record.pk, self.interaction.pk]),
        )
        self.assertContains(response, "Editar actividad")

    def test_update_view_loads_prepopulated_form(self):
        response = self.client.get(
            reverse("crm:interaction_update", args=[self.client_record.pk, self.interaction.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestor de clientes")
        self.assertContains(response, "Editar actividad")
        self.assertContains(response, 'value="Correo inicial"')
        self.assertContains(response, "Resumen inicial de la actividad.")
        self.assertContains(response, "Enviar documentación actualizada.")

    def test_update_view_saves_changes_and_redirects_to_client_detail(self):
        response = self.client.post(
            reverse("crm:interaction_update", args=[self.client_record.pk, self.interaction.pk]),
            data={
                "interaction_type": Interaction.InteractionType.MEETING,
                "subject": "Reunión de seguimiento",
                "summary": "Se revisaron cambios sobre la propuesta comercial.",
                "next_step": "Preparar versión final para validación.",
            },
        )

        self.assertRedirects(response, reverse("crm:client_detail", args=[self.client_record.pk]))

        self.interaction.refresh_from_db()
        self.assertEqual(self.interaction.interaction_type, Interaction.InteractionType.MEETING)
        self.assertEqual(self.interaction.subject, "Reunión de seguimiento")
        self.assertEqual(self.interaction.summary, "Se revisaron cambios sobre la propuesta comercial.")
        self.assertEqual(self.interaction.next_step, "Preparar versión final para validación.")
        self.assertEqual(self.interaction.client, self.client_record)
        self.assertEqual(self.interaction.created_by, self.owner)

    def test_update_view_rerenders_form_with_errors(self):
        response = self.client.post(
            reverse("crm:interaction_update", args=[self.client_record.pk, self.interaction.pk]),
            data={
                "interaction_type": Interaction.InteractionType.NOTE,
                "subject": "",
                "summary": "",
                "next_step": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Gestor de clientes")
        self.assertContains(response, "Editar actividad")
        self.assertContains(response, "Guardar cambios")

        self.interaction.refresh_from_db()
        self.assertEqual(self.interaction.subject, "Correo inicial")
        self.assertEqual(self.interaction.summary, "Resumen inicial de la actividad.")

    def test_update_view_only_accepts_interactions_for_the_given_client(self):
        other_client = Client.objects.create(
            first_name="Carlos",
            last_name="Vega",
            email="carlos.vega@example.com",
            owner=self.owner,
            status=Client.Status.LEAD,
        )

        response = self.client.get(
            reverse("crm:interaction_update", args=[other_client.pk, self.interaction.pk]),
        )

        self.assertEqual(response.status_code, 404)


class InteractionDeleteFlowTests(CRMBaseTestCase):
    def setUp(self):
        self.owner = self.create_user()
        self.company = Company.objects.create(name="Empresa Demo")
        self.client_record = Client.objects.create(
            first_name="Lucia",
            last_name="Martinez",
            email="lucia.martinez@example.com",
            phone="+34 600 000 002",
            position="Directora Comercial",
            company=self.company,
            owner=self.owner,
            status=Client.Status.CONTACTED,
        )
        self.interaction = Interaction.objects.create(
            client=self.client_record,
            created_by=self.owner,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="Correo inicial",
            summary="Resumen inicial de la actividad.",
            next_step="Enviar documentación actualizada.",
        )
        self.login_user()

    def test_client_detail_shows_link_to_delete_view_for_each_interaction(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("crm:interaction_delete", args=[self.client_record.pk, self.interaction.pk]),
        )
        self.assertContains(response, "Eliminar actividad")

    def test_delete_confirmation_view_shows_interaction_and_cancel_link(self):
        response = self.client.get(
            reverse("crm:interaction_delete", args=[self.client_record.pk, self.interaction.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eliminar actividad")
        self.assertContains(response, "Correo inicial")
        self.assertContains(response, "Lucia Martinez")
        self.assertContains(response, reverse("crm:client_detail", args=[self.client_record.pk]))
        self.assertTrue(Interaction.objects.filter(pk=self.interaction.pk).exists())

    def test_delete_confirmation_cancel_keeps_interaction_and_returns_to_detail(self):
        delete_url = reverse("crm:interaction_delete", args=[self.client_record.pk, self.interaction.pk])
        detail_url = reverse("crm:client_detail", args=[self.client_record.pk])

        response = self.client.get(delete_url)
        self.assertContains(response, detail_url)

        cancel_response = self.client.get(detail_url)
        self.assertEqual(cancel_response.status_code, 200)
        self.assertTrue(Interaction.objects.filter(pk=self.interaction.pk).exists())
        self.assertContains(cancel_response, "Correo inicial")

    def test_delete_view_removes_interaction_and_redirects_to_client_detail(self):
        response = self.client.post(
            reverse("crm:interaction_delete", args=[self.client_record.pk, self.interaction.pk]),
        )

        self.assertRedirects(response, reverse("crm:client_detail", args=[self.client_record.pk]))
        self.assertFalse(Interaction.objects.filter(pk=self.interaction.pk).exists())
        self.assertTrue(Client.objects.filter(pk=self.client_record.pk).exists())

    def test_delete_view_only_accepts_interactions_for_the_given_client(self):
        other_client = Client.objects.create(
            first_name="Carlos",
            last_name="Vega",
            email="carlos.vega@example.com",
            owner=self.owner,
            status=Client.Status.LEAD,
        )

        response = self.client.get(
            reverse("crm:interaction_delete", args=[other_client.pk, self.interaction.pk]),
        )

        self.assertEqual(response.status_code, 404)
