from django.urls import path

from .views import ClientCreateView, ClientListView

app_name = "crm"

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("clientes/nuevo/", ClientCreateView.as_view(), name="client_create"),
]
