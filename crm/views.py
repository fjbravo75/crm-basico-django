from django.db.models import Q
from django.views.generic import ListView

from .models import Client


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
