from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Client, Company


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
