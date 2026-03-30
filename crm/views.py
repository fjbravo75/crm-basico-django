import csv
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClientForm, InteractionForm, RegisterForm
from .management.commands.seed_demo_crm import DEMO_PASSWORD, DEMO_USER
from .models import Client, Interaction


CLIENT_STATUS_LABELS_ES = {
    Client.Status.LEAD: "Inicial",
    Client.Status.CONTACTED: "Contactado",
    Client.Status.FOLLOW_UP: "Seguimiento",
    Client.Status.PROPOSAL: "Propuesta",
    Client.Status.WON: "Ganado",
    Client.Status.LOST: "Perdido",
}

CLIENT_SOURCE_LABELS_ES = {
    Client.Source.WEBSITE: "Web",
    Client.Source.REFERRAL: "Referencia",
    Client.Source.SOCIAL_MEDIA: "Redes sociales",
    Client.Source.EMAIL_CAMPAIGN: "Campaña de correo",
    Client.Source.OTHER: "Otro",
}


def get_display_user_name(user):
    return user.get_full_name() or user.get_username()


def get_client_status_label(client):
    return CLIENT_STATUS_LABELS_ES.get(client.status, client.get_status_display())


def get_client_source_label(client):
    if not client.source:
        return "Sin especificar"
    return CLIENT_SOURCE_LABELS_ES.get(client.source, client.get_source_display())


class CRMLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_demo_access"] = settings.SHOW_DEMO_ACCESS
        context["allow_public_registration"] = settings.ALLOW_PUBLIC_REGISTRATION

        if settings.SHOW_DEMO_ACCESS:
            context["demo_username"] = DEMO_USER["username"]
            context["demo_password"] = DEMO_PASSWORD

        return context


def register(request):
    if request.user.is_authenticated:
        return redirect("crm:client_list")

    if not settings.ALLOW_PUBLIC_REGISTRATION:
        return redirect("login")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("crm:client_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def get_owned_clients_queryset(user):
    return Client.objects.select_related("company", "owner").filter(owner=user)


def get_owned_interactions_queryset(user):
    return Interaction.objects.select_related(
        "client",
        "client__company",
        "client__owner",
        "created_by",
    ).filter(client__owner=user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"
    paginate_by = 5
    csv_export_param = "export"
    csv_export_value = "csv"
    dashboard_status_order = (
        Client.Status.LEAD,
        Client.Status.CONTACTED,
        Client.Status.FOLLOW_UP,
        Client.Status.PROPOSAL,
        Client.Status.WON,
        Client.Status.LOST,
    )
    dashboard_in_progress_statuses = {
        Client.Status.LEAD,
        Client.Status.CONTACTED,
        Client.Status.FOLLOW_UP,
        Client.Status.PROPOSAL,
    }

    def get(self, request, *args, **kwargs):
        if request.GET.get(self.csv_export_param) == self.csv_export_value:
            return self.render_to_csv_response(self.get_queryset())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = get_owned_clients_queryset(self.request.user)
        search_query = self.request.GET.get("q", "").strip()

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(company__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["total_clients"] = context["paginator"].count
        export_params = []
        if context["search_query"]:
            export_params.append(("q", context["search_query"]))
        export_params.append((self.csv_export_param, self.csv_export_value))
        context["export_query_string"] = urlencode(export_params)
        context.update(self.get_dashboard_context(self.object_list))
        return context

    def get_dashboard_context(self, queryset):
        total_clients = queryset.count()

        if total_clients == 0:
            return {
                "show_client_dashboard": False,
                "dashboard_kpis": [],
                "dashboard_status_distribution": [],
            }

        status_counts = {
            item["status"]: item["count"]
            for item in queryset.values("status").annotate(count=Count("pk"))
        }
        max_status_count = max(status_counts.values(), default=0)
        dashboard_status_distribution = []

        for status in self.dashboard_status_order:
            count = status_counts.get(status, 0)
            dashboard_status_distribution.append(
                {
                    "status": status,
                    "label": CLIENT_STATUS_LABELS_ES[status],
                    "count": count,
                    "bar_width": round((count * 100) / max_status_count) if max_status_count else 0,
                }
            )

        dashboard_kpis = [
            {"label": "Total fichas", "value": total_clients},
            {
                "label": "Abiertas",
                "value": sum(
                    status_counts.get(status, 0)
                    for status in self.dashboard_in_progress_statuses
                ),
            },
            {"label": "Ganadas", "value": status_counts.get(Client.Status.WON, 0)},
            {"label": "Perdidas", "value": status_counts.get(Client.Status.LOST, 0)},
        ]

        return {
            "show_client_dashboard": True,
            "dashboard_kpis": dashboard_kpis,
            "dashboard_status_distribution": dashboard_status_distribution,
        }

    def render_to_csv_response(self, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="clientes.csv"'
        writer = csv.writer(response)
        writer.writerow(
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
            ]
        )

        for client in queryset:
            writer.writerow(
                [
                    client.first_name,
                    client.last_name,
                    client.email,
                    client.phone,
                    client.company.name if client.company else "",
                    client.position,
                    get_client_status_label(client),
                    get_client_source_label(client),
                    get_display_user_name(client.owner),
                    client.created_at.strftime("%d/%m/%Y %H:%M"),
                    client.updated_at.strftime("%d/%m/%Y %H:%M"),
                ]
            )

        return response


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("crm:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        return get_owned_clients_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interactions = self.object.interactions.select_related("created_by").order_by(
            "-interaction_date",
            "-pk",
        )
        paginator = Paginator(interactions, 3)
        activity_page = self.request.GET.get("activity_page")
        query_params = self.request.GET.copy()
        query_params.pop("activity_page", None)

        context["activity_page_obj"] = paginator.get_page(activity_page)
        context["activity_query_string"] = query_params.urlencode()
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    context_object_name = "client"

    def get_queryset(self):
        return get_owned_clients_queryset(self.request.user)

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "crm/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("crm:client_list")

    def get_queryset(self):
        return get_owned_clients_queryset(self.request.user)


class InteractionCreateView(LoginRequiredMixin, CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "crm/interaction_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.get_client()
        return context

    def form_valid(self, form):
        form.instance.client = self.get_client()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.get_client().pk})

    def get_client(self):
        return get_object_or_404(
            get_owned_clients_queryset(self.request.user),
            pk=self.kwargs["client_pk"],
        )


class InteractionUpdateView(LoginRequiredMixin, UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "crm/interaction_form.html"
    context_object_name = "interaction"

    def get_queryset(self):
        return get_owned_interactions_queryset(self.request.user).filter(
            client_id=self.kwargs["client_pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.object.client
        return context

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.client_id})


class InteractionDeleteView(LoginRequiredMixin, DeleteView):
    model = Interaction
    template_name = "crm/interaction_confirm_delete.html"
    context_object_name = "interaction"

    def get_queryset(self):
        return get_owned_interactions_queryset(self.request.user).filter(
            client_id=self.kwargs["client_pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.object.client
        return context

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.client_id})
