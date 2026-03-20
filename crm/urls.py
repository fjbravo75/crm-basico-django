from django.urls import path

from .views import ClientCreateView, ClientDetailView, ClientListView, ClientUpdateView

app_name = "crm"

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("clientes/nuevo/", ClientCreateView.as_view(), name="client_create"),
    path("clientes/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clientes/<int:pk>/editar/", ClientUpdateView.as_view(), name="client_update"),
]
