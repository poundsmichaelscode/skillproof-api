from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.skills.models import Skill


class Evidence(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evidence_records",
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="evidence_records",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    evidence_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def clean(self):
        super().clean()

        if (
            self.owner_id is not None
            and self.skill_id is not None
            and not Skill.objects.filter(
                pk=self.skill_id,
                owner_id=self.owner_id,
            ).exists()
        ):
            raise ValidationError({
                "skill": "The skill must belong to the evidence owner."
            })

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
