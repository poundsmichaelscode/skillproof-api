from rest_framework import permissions, viewsets

from apps.evidence.models import Evidence
from apps.evidence.serializers import EvidenceSerializer


class EvidenceViewSet(viewsets.ModelViewSet):
    serializer_class = EvidenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Evidence.objects.filter(
            owner=self.request.user
        ).select_related("skill")
