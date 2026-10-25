"""Tests for consistent API errors without altering HTTP semantics."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.opportunities.models import Opportunity

User = get_user_model()


class ErrorContractTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="error_owner", password="SampleStrong#2026")
        self.other = User.objects.create_user(username="error_other", password="SampleStrong#2026")
        self.client = APIClient()
        self.record = Opportunity.objects.create(
            owner=self.owner, title="Backend Engineer", organization="Example Co",
            application_url="https://example.com/jobs/1",
        )

    def authenticate(self, user):
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def assert_api_error(self, response, status, code):
        self.assertEqual(response.status_code, status)
        self.assertEqual(list(response.data), ["error"])
        self.assertEqual(response.data["error"]["code"], code)
        self.assertTrue(response.data["error"]["message"])

    def test_validation_error(self):
        self.authenticate(self.owner)
        response = self.client.post(reverse("opportunity-list"), {"title": " "}, format="json")
        self.assert_api_error(response, 400, "VALIDATION_ERROR")
        self.assertIn("organization", response.data["error"]["details"])

    def test_missing_authentication(self):
        response = self.client.get(reverse("opportunity-list"))
        self.assert_api_error(response, 401, "AUTHENTICATION_FAILED")

    def test_invalid_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token")
        response = self.client.get(reverse("skill-list"))
        self.assert_api_error(response, 401, "AUTHENTICATION_FAILED")

    def test_permission_denied(self):
        self.authenticate(self.other)
        response = self.client.patch(reverse("opportunity-detail", args=[self.record.pk]), {"title": "No"}, format="json")
        self.assert_api_error(response, 403, "PERMISSION_DENIED")

    def test_not_found(self):
        self.authenticate(self.other)
        response = self.client.get(reverse("skill-detail", args=[9999999]))
        self.assert_api_error(response, 404, "NOT_FOUND")

    def test_method_not_allowed(self):
        self.authenticate(self.owner)
        response = self.client.put(reverse("auth-me"), {"first_name": "No"}, format="json")
        self.assert_api_error(response, 405, "METHOD_NOT_ALLOWED")

    def test_success_shape_is_unchanged(self):
        self.authenticate(self.owner)
        response = self.client.get(reverse("auth-me"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.data)
        self.assertNotIn("error", response.data)
