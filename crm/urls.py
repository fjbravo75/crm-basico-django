from django.urls import path

from .views import ClientCreateView, ClientDetailView, ClientListView

app_name = "crm"

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("clientes/nuevo/", ClientCreateView.as_view(), name="client_create"),
    path("clientes/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
]
