from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


User = get_user_model()


class RegistrationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.url = reverse("auth-register")
        self.payload = {
            "username": "learner1",
            "email": "learner@example.com",
            "password": "ExampleOnly#8472",
            "password_confirm": "ExampleOnly#8472",
        }

    def test_successful_registration(self):
        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="learner1").exists()
        )
        self.assertNotIn("password", response.data)
        self.assertNotIn("password_confirm", response.data)

    def test_password_is_hashed(self):
        self.client.post(
            self.url, self.payload, format="json"
        )

        user = User.objects.get(username="learner1")

        self.assertNotEqual(
            user.password, self.payload["password"]
        )
        self.assertTrue(
            user.check_password(self.payload["password"])
        )

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            username="existing",
            email="learner@example.com",
            password="AnotherStrong#8492",
        )

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_duplicate_username_rejected(self):
        User.objects.create_user(
            username="learner1",
            email="existing@example.com",
            password="AnotherStrong#8492",
        )

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_password_mismatch_rejected(self):
        payload = {
            **self.payload,
            "password_confirm": "DifferentStrong#8492",
        }

        response = self.client.post(
            self.url, payload, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_weak_password_rejected(self):
        payload = {
            **self.payload,
            "password": "123",
            "password_confirm": "123",
        }

        response = self.client.post(
            self.url, payload, format="json"
        )

        self.assertEqual(response.status_code, 400)
