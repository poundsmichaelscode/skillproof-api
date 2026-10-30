from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.skills.models import Skill


User = get_user_model()


class JWTSkillOwnershipTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice",
            password="StrongTestPass#8492",
        )
        self.bob = User.objects.create_user(
            username="bob",
            password="StrongTestPass#8492",
        )

        self.alice_skill = Skill.objects.create(
            owner=self.alice,
            name="Python",
        )
        self.bob_skill = Skill.objects.create(
            owner=self.bob,
            name="Docker",
        )

        self.client = APIClient()
        self.list_url = reverse("skill-list")

    def authenticate(self, user):
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )

    def test_valid_jwt_allows_skill_listing(self):
        self.authenticate(self.alice)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["name"], "Python"
        )

    def test_user_cannot_view_another_users_skill(self):
        self.authenticate(self.alice)

        response = self.client.get(
            reverse("skill-detail", args=[self.bob_skill.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_modify_another_users_skill(self):
        self.authenticate(self.alice)

        response = self.client.patch(
            reverse("skill-detail", args=[self.bob_skill.pk]),
            {"name": "Changed by Alice"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        self.bob_skill.refresh_from_db()
        self.assertEqual(self.bob_skill.name, "Docker")

    def test_user_cannot_delete_another_users_skill(self):
        self.authenticate(self.alice)

        response = self.client.delete(
            reverse("skill-detail", args=[self.bob_skill.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Skill.objects.filter(pk=self.bob_skill.pk).exists()
        )

    def test_owner_cannot_be_spoofed(self):
        self.authenticate(self.alice)

        response = self.client.post(
            self.list_url,
            {
                "name": "Kubernetes",
                "owner": self.bob.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        created = Skill.objects.get(name="Kubernetes")
        self.assertEqual(created.owner, self.alice)

    def test_missing_token_is_rejected(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 401)

    def test_jwt_cannot_access_another_users_profile(self):
        self.authenticate(self.alice)

        response = self.client.get(reverse("auth-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["username"], "alice"
        )
        self.assertNotEqual(
            response.data["username"], "bob"
        )
