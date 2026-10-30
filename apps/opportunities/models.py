from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Opportunity(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )

    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    application_url = models.URLField()

    closing_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(
                fields=["-created_at", "-id"],
                name="opportunity_recent_idx",
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        if not self.title or not self.title.strip():
            errors["title"] = "Opportunity title cannot be empty."

        if not self.organization or not self.organization.strip():
            errors["organization"] = "Organization cannot be empty."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        self.organization = self.organization.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.organization}"
