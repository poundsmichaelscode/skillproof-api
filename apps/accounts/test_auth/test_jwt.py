from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


User = get_user_model()


class JWTAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jwtuser",
            email="jwtuser@example.com",
            password="StrongPassword#8492",
        )

        self.client = APIClient()
        self.token_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.skills_url = reverse("skill-list")

    def obtain_tokens(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "jwtuser",
                "password": "StrongPassword#8492",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_valid_login_returns_tokens(self):
        tokens = self.obtain_tokens()

        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

    def test_invalid_password_rejected(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "jwtuser",
                "password": "WrongPassword#8492",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access", response.data)

    def test_refresh_token_returns_new_access_token(self):
        tokens = self.obtain_tokens()

        response = self.client.post(
            self.refresh_url,
            {"refresh": tokens["refresh"]},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_access_token_allows_skills_request(self):
        tokens = self.obtain_tokens()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {tokens['access']}"
        )

        response = self.client.get(self.skills_url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_skills(self):
        response = self.client.get(self.skills_url)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        response = self.client.get(self.skills_url)

        self.assertEqual(response.status_code, 401)

    def test_expired_token_rejected(self):
        token = AccessToken.for_user(self.user)
        token.set_exp(lifetime=timedelta(seconds=-1))

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

        response = self.client.get(self.skills_url)

        self.assertEqual(response.status_code, 401)

    def test_refresh_token_cannot_access_skills(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh}"
        )

        response = self.client.get(self.skills_url)

        self.assertEqual(response.status_code, 401)
