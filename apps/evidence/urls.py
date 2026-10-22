from rest_framework.routers import DefaultRouter

from apps.evidence.views import EvidenceViewSet


router = DefaultRouter()
router.register(
    "",
    EvidenceViewSet,
    basename="evidence",
)

urlpatterns = router.urls
