from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClientForm, InteractionForm, RegisterForm
from .models import Client, Interaction


def register(request):
    if request.user.is_authenticated:
        return redirect("crm:client_list")

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
        return context


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
