from django.urls import path

from apps.accounts.views import RegisterView


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="auth-register",
    ),
]
