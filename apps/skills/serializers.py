from rest_framework import serializers

from apps.skills.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "description",
            "proficiency",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        name = value.strip()

        if not name:
            raise serializers.ValidationError(
                "Skill name cannot be empty."
            )

        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        existing = Skill.objects.filter(
            owner=request.user,
            name__iexact=name,
        )

        if self.instance is not None:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError(
                "You already have a skill with this name."
            )

        return name
