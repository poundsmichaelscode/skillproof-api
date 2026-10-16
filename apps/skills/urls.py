from rest_framework.routers import DefaultRouter

from apps.skills.views import SkillViewSet


router = DefaultRouter()
router.register(
    "",
    SkillViewSet,
    basename="skill",
)

urlpatterns = router.urls
