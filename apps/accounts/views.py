from rest_framework.throttling import ScopedRateThrottle
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.accounts.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_register"

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


from rest_framework.permissions import IsAuthenticated

from apps.accounts.serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user
