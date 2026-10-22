from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.views import RegisterView, UserProfileView


urlpatterns = [
    path(
        "me/",
        UserProfileView.as_view(),
        name="auth-me",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="auth-register",
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
