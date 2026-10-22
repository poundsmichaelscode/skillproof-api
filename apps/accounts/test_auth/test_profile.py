from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="StrongPassword#8492",
            first_name="Test",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="StrongPassword#8492",
        )

        self.client = APIClient()
        self.url = reverse("auth-me")

        token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )

    def test_user_can_read_own_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["username"],
            "profileuser",
        )
        self.assertEqual(
            response.data["email"],
            "profile@example.com",
        )

    def test_profile_does_not_expose_sensitive_fields(self):
        response = self.client.get(self.url)

        for field in [
            "password",
            "is_staff",
            "is_superuser",
            "is_active",
        ]:
            self.assertNotIn(field, response.data)

    def test_user_can_update_profile(self):
        response = self.client.patch(
            self.url,
            {
                "first_name": "Updated",
                "last_name": "Learner",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Learner")

    def test_email_is_normalized(self):
        response = self.client.patch(
            self.url,
            {"email": " NEW@EXAMPLE.COM "},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(
            self.user.email,
            "new@example.com",
        )

    def test_duplicate_email_is_rejected(self):
        response = self.client.patch(
            self.url,
            {"email": "other@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_client_cannot_change_admin_privileges(self):
        response = self.client.patch(
            self.url,
            {
                "is_staff": True,
                "is_superuser": True,
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

    def test_client_cannot_change_password(self):
        original_password = self.user.password

        response = self.client.patch(
            self.url,
            {"password": "NewPassword#8492"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(
            self.user.password,
            original_password,
        )

    def test_anonymous_user_is_rejected(self):
        self.client.credentials()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_put_method_is_not_allowed(self):
        response = self.client.put(
            self.url,
            {"first_name": "Changed"},
            format="json",
        )

        self.assertEqual(response.status_code, 405)
