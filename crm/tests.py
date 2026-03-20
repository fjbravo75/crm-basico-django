from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Client, Company, Interaction


class ClientCreateFlowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
        self.company = Company.objects.create(name="Empresa Demo")

    def test_client_list_shows_link_to_create_view(self):
        response = self.client.get(reverse("crm:client_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nuevo cliente")
        self.assertContains(response, reverse("crm:client_create"))

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


class ClientDetailFlowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
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
        self.assertContains(response, self.owner.get_username())


class ClientUpdateFlowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
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

    def test_client_detail_shows_link_to_update_view(self):
        response = self.client.get(reverse("crm:client_detail", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("crm:client_update", args=[self.client_record.pk]))
        self.assertContains(response, "Editar cliente")

    def test_update_view_loads_prepopulated_form(self):
        response = self.client.get(reverse("crm:client_update", args=[self.client_record.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Editar cliente")
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


class ClientDeleteFlowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
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


class ClientListPaginationTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
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


class InteractionCreateFlowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="responsable",
            password="testpass123",
        )
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
