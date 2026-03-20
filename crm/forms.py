from django import forms

from .models import Client


STATUS_CHOICES_ES = [
    (Client.Status.LEAD, "Prospecto"),
    (Client.Status.CONTACTED, "Contactado"),
    (Client.Status.FOLLOW_UP, "Seguimiento"),
    (Client.Status.PROPOSAL, "Propuesta"),
    (Client.Status.WON, "Ganado"),
    (Client.Status.LOST, "Perdido"),
]

SOURCE_CHOICES_ES = [
    ("", "Sin especificar"),
    (Client.Source.WEBSITE, "Web"),
    (Client.Source.REFERRAL, "Referencia"),
    (Client.Source.SOCIAL_MEDIA, "Redes sociales"),
    (Client.Source.EMAIL_CAMPAIGN, "Campaña de correo"),
    (Client.Source.OTHER, "Otro"),
]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "position",
            "company",
            "status",
            "source",
            "notes",
        ]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
            "phone": "Teléfono",
            "position": "Cargo",
            "company": "Empresa",
            "status": "Estado",
            "source": "Origen",
            "notes": "Notas",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "source": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].empty_label = "Sin empresa"
        self.fields["status"].choices = STATUS_CHOICES_ES
        self.fields["source"].choices = SOURCE_CHOICES_ES
