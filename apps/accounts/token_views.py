from rest_framework.throttling import ScopedRateThrottle

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_login"


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_refresh"
