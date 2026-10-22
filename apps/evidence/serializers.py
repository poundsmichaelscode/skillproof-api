from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.evidence.models import Evidence
from apps.skills.models import Skill


class EvidenceSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.none()
    )

    class Meta:
        model = Evidence
        fields = [
            "id",
            "skill",
            "title",
            "description",
            "evidence_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            fields["skill"].queryset = Skill.objects.filter(
                owner=request.user
            )

        return fields

    def validate_title(self, value):
        title = value.strip()

        if not title:
            raise serializers.ValidationError(
                "Evidence title cannot be empty."
            )

        return title

    def create(self, validated_data):
        request = self.context["request"]

        try:
            return Evidence.objects.create(
                owner=request.user,
                **validated_data,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict
            )

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        try:
            instance.save()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict
            )

        return instance
