from apps.accounts.throttles import SafeScopedRateThrottle

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [SafeScopedRateThrottle]
    throttle_scope = "auth_login"


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [SafeScopedRateThrottle]
    throttle_scope = "auth_refresh"
