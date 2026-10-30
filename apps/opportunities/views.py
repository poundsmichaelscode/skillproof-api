from config.pagination import StandardResultsPagination
from rest_framework import viewsets

from apps.opportunities.models import Opportunity
from apps.opportunities.permissions import IsOpportunityOwnerOrAdmin
from apps.opportunities.serializers import OpportunitySerializer


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    pagination_class = StandardResultsPagination
    serializer_class = OpportunitySerializer
    permission_classes = [IsOpportunityOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
