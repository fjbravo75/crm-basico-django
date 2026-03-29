from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClientForm, InteractionForm
from .models import Client, Interaction


DEFAULT_OWNER = {
    "username": "maria.ortega",
    "email": "maria.ortega@demo-crm.example",
    "first_name": "Maria",
    "last_name": "Ortega",
    "is_active": True,
}


def get_current_or_default_user(request):
    if request.user.is_authenticated:
        return request.user

    user_model = get_user_model()
    existing_user = user_model.objects.order_by("id").first()
    if existing_user:
        return existing_user

    owner, created = user_model.objects.get_or_create(
        username=DEFAULT_OWNER["username"],
        defaults={
            "email": DEFAULT_OWNER["email"],
            "first_name": DEFAULT_OWNER["first_name"],
            "last_name": DEFAULT_OWNER["last_name"],
            "is_active": DEFAULT_OWNER["is_active"],
        },
    )
    if created:
        owner.set_unusable_password()
        owner.save(update_fields=["password"])

    return owner


class ClientListView(ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"
    paginate_by = 5

    def get_queryset(self):
        queryset = (
            Client.objects.select_related("company", "owner")
            .all()
        )
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
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("crm:client_list")

    def form_valid(self, form):
        form.instance.owner = self._get_owner()
        return super().form_valid(form)

    def _get_owner(self):
        return get_current_or_default_user(self.request)


class ClientDetailView(DetailView):
    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        return Client.objects.select_related("company", "owner")

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


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/client_form.html"
    context_object_name = "client"

    def get_queryset(self):
        return Client.objects.select_related("company", "owner")

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "crm/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("crm:client_list")

    def get_queryset(self):
        return Client.objects.select_related("company", "owner")


class InteractionCreateView(CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "crm/interaction_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.client = get_object_or_404(
            Client.objects.select_related("company", "owner"),
            pk=kwargs["client_pk"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.client
        return context

    def form_valid(self, form):
        form.instance.client = self.client
        form.instance.created_by = get_current_or_default_user(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.client.pk})


class InteractionUpdateView(UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "crm/interaction_form.html"
    context_object_name = "interaction"

    def get_queryset(self):
        return (
            Interaction.objects.select_related(
                "client",
                "client__company",
                "client__owner",
                "created_by",
            )
            .filter(client_id=self.kwargs["client_pk"])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.object.client
        return context

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.client_id})


class InteractionDeleteView(DeleteView):
    model = Interaction
    template_name = "crm/interaction_confirm_delete.html"
    context_object_name = "interaction"

    def get_queryset(self):
        return (
            Interaction.objects.select_related(
                "client",
                "client__company",
                "client__owner",
                "created_by",
            )
            .filter(client_id=self.kwargs["client_pk"])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.object.client
        return context

    def get_success_url(self):
        return reverse("crm:client_detail", kwargs={"pk": self.object.client_id})
