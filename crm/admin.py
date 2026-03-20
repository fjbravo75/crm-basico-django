from django.contrib import admin

from .models import Client, Company, Interaction


admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Interaction)
