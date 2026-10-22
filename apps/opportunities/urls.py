from rest_framework.routers import DefaultRouter

from apps.opportunities.views import OpportunityViewSet


router = DefaultRouter()
router.register(
    "",
    OpportunityViewSet,
    basename="opportunity",
)

urlpatterns = router.urls
