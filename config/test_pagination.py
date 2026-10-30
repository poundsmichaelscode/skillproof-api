from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.skills.models import Skill


User = get_user_model()


class PaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="pagination_user",
            password="ExampleTestPassword#123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("skill-list")

        for number in range(25):
            Skill.objects.create(
                owner=self.user,
                name=f"Skill {number:03d}",
            )

    def test_default_page_size(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 25)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertIsNotNone(response.data["next"])

    def test_second_page(self):
        response = self.client.get(self.url, {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 5)

    def test_custom_page_size(self):
        response = self.client.get(
            self.url,
            {"page_size": 5},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 5)

    def test_page_size_cannot_exceed_100(self):
        response = self.client.get(
            self.url,
            {"page_size": 500},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 25)

    def test_invalid_page_returns_404(self):
        response = self.client.get(
            self.url,
            {"page": 999},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"]["code"],
            "NOT_FOUND",
        )
