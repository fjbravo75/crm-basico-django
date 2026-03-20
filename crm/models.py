from django.conf import settings
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Client(models.Model):
    class Status(models.TextChoices):
        LEAD = "lead", "Lead"
        CONTACTED = "contacted", "Contacted"
        FOLLOW_UP = "follow_up", "Follow up"
        PROPOSAL = "proposal", "Proposal"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    class Source(models.TextChoices):
        WEBSITE = "website", "Website"
        REFERRAL = "referral", "Referral"
        SOCIAL_MEDIA = "social_media", "Social media"
        EMAIL_CAMPAIGN = "email_campaign", "Email campaign"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=120, blank=True)
    company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_clients",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.LEAD,
        db_index=True,
    )
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        blank=True,
        default="",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Interaction(models.Model):
    class InteractionType(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        MEETING = "meeting", "Meeting"
        NOTE = "note", "Note"
        FOLLOW_UP = "follow_up", "Follow up"

    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_interactions",
    )
    interaction_type = models.CharField(max_length=20, choices=InteractionType.choices)
    interaction_date = models.DateTimeField(default=timezone.now, db_index=True)
    subject = models.CharField(max_length=200)
    summary = models.TextField()
    next_step = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-interaction_date", "-created_at"]

    def __str__(self):
        return (
            f"{self.get_interaction_type_display()} - "
            f"{self.client} - "
            f"{self.interaction_date:%Y-%m-%d %H:%M}"
        )
