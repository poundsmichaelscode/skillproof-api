from django.urls import path
from apps.accounts.token_views import (
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
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
        ThrottledTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        ThrottledTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
