from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class AuthenticationThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def tearDown(self):
        cache.clear()

    def test_registration_limit(self):
        url = reverse("auth-register")

        for _ in range(5):
            response = self.client.post(url, {}, format="json")
            self.assertEqual(response.status_code, 400)

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.data["error"]["code"],
            "RATE_LIMITED",
        )

    def test_login_limit(self):
        url = reverse("token_obtain_pair")
        payload = {
            "username": "missing_user",
            "password": "InvalidPassword123!",
        }

        for _ in range(10):
            response = self.client.post(url, payload, format="json")
            self.assertEqual(response.status_code, 401)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.data["error"]["code"],
            "RATE_LIMITED",
        )

    def test_refresh_limit(self):
        url = reverse("token_refresh")
        payload = {"refresh": "invalid-token"}

        for _ in range(20):
            response = self.client.post(url, payload, format="json")
            self.assertEqual(response.status_code, 401)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.data["error"]["code"],
            "RATE_LIMITED",
        )
