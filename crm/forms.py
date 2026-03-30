from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import override

from .models import Client, Company, Interaction


STATUS_CHOICES_ES = [
    (Client.Status.LEAD, "Inicial"),
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

INTERACTION_TYPE_CHOICES_ES = [
    (Interaction.InteractionType.CALL, "Llamada"),
    (Interaction.InteractionType.EMAIL, "Correo"),
    (Interaction.InteractionType.MEETING, "Reunión"),
    (Interaction.InteractionType.NOTE, "Nota"),
    (Interaction.InteractionType.FOLLOW_UP, "Seguimiento"),
]


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Las contraseñas no coinciden. Revisa ambos campos y vuelve a intentarlo.",
    }

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "Nombre"
        self.fields["last_name"].label = "Apellidos"
        self.fields["username"].label = "Usuario"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["username"].max_length = 30
        self.fields["username"].widget.attrs["maxlength"] = 30
        self.fields["username"].help_text = "Lo usarás para entrar. Mejor si es corto y fácil de recordar."
        self.fields["password1"].help_text = "Usa una contraseña de al menos 8 caracteres y evita las demasiado simples."
        self.fields["password2"].help_text = "Repítela para confirmar el acceso."
        self.fields["first_name"].error_messages["required"] = "Escribe tu nombre para crear la cuenta."
        self.fields["last_name"].error_messages["required"] = "Escribe tus apellidos para crear la cuenta."
        self.fields["username"].error_messages["required"] = "Escribe un nombre de usuario para crear la cuenta."
        self.fields["username"].error_messages["max_length"] = "El usuario no puede superar los 30 caracteres."
        self.fields["password1"].error_messages["required"] = "Escribe una contraseña para continuar."
        self.fields["password2"].error_messages["required"] = "Confirma la contraseña para continuar."

        for validator in self.fields["username"].validators:
            if hasattr(validator, "message"):
                validator.message = "Introduce un nombre de usuario válido. Puedes usar letras, números y @/./+/-/_."

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and len(username) > 30:
            raise forms.ValidationError("El usuario no puede superar los 30 caracteres.")
        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese nombre de usuario. Prueba con otro.")
        return username

    def validate_password_for_user(self, user, password_field_name="password2"):
        with override("es"):
            super().validate_password_for_user(user, password_field_name=password_field_name)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ClientForm(forms.ModelForm):
    new_company_name = forms.CharField(
        label="Nueva empresa",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

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
            "company": "Empresa existente",
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
        self.order_fields(
            [
                "first_name",
                "last_name",
                "email",
                "phone",
                "position",
                "company",
                "new_company_name",
                "status",
                "source",
                "notes",
            ]
        )

    def clean_new_company_name(self):
        return self.cleaned_data.get("new_company_name", "").strip()

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get("company")
        new_company_name = cleaned_data.get("new_company_name", "")

        if company and new_company_name:
            message = "Usa solo una de las dos opciones de empresa."
            self.add_error("company", message)
            self.add_error("new_company_name", message)

        return cleaned_data

    def save(self, commit=True):
        company = self.cleaned_data.get("company")
        new_company_name = self.cleaned_data.get("new_company_name", "")

        if new_company_name:
            company = Company.objects.filter(name__iexact=new_company_name).first()
            if company is None:
                company = Company.objects.create(name=new_company_name)

        self.instance.company = company
        return super().save(commit=commit)


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = [
            "interaction_type",
            "subject",
            "summary",
            "next_step",
        ]
        labels = {
            "interaction_type": "Tipo de actividad",
            "subject": "Asunto",
            "summary": "Resumen",
            "next_step": "Próximo paso",
        }
        widgets = {
            "interaction_type": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "next_step": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["interaction_type"].choices = INTERACTION_TYPE_CHOICES_ES
