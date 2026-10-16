from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APIClient


class HealthCheckTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_check_allows_anonymous_access(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)

    def test_health_check_rejects_post(self):
        response = self.client.post("/api/v1/health/")

        self.assertEqual(response.status_code, 405)
