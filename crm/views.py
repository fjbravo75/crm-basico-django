from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import ClientForm
from .models import Client


DEFAULT_OWNER = {
    "username": "maria.ortega",
    "email": "maria.ortega@demo-crm.example",
    "first_name": "Maria",
    "last_name": "Ortega",
    "is_active": True,
}


class ClientListView(ListView):
    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"

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
        if self.request.user.is_authenticated:
            return self.request.user

        user_model = get_user_model()
        existing_owner = user_model.objects.order_by("id").first()
        if existing_owner:
            return existing_owner

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
