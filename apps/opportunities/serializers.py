from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.opportunities.models import Opportunity


class OpportunitySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "owner",
            "title",
            "organization",
            "description",
            "application_url",
            "closing_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        title = value.strip()
        if not title:
            raise serializers.ValidationError(
                "Opportunity title cannot be empty."
            )
        return title

    def validate_organization(self, value):
        organization = value.strip()
        if not organization:
            raise serializers.ValidationError(
                "Organization cannot be empty."
            )
        return organization

    def create(self, validated_data):
        try:
            return Opportunity.objects.create(**validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        try:
            instance.save()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

        return instance
