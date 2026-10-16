from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.skills.models import Skill


User = get_user_model()


class SkillAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="skill_api_owner",
            password="TestPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="other_skill_api_owner",
            password="TestPassword123!",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.list_url = reverse("skill-list")

    def test_authenticated_user_can_create_skill(self):
        response = self.client.post(
            self.list_url,
            {
                "name": "Python",
                "proficiency": "intermediate",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Skill.objects.filter(
                owner=self.user,
                name="Python",
            ).exists()
        )

    def test_user_can_list_only_own_skills(self):
        Skill.objects.create(
            owner=self.user,
            name="Docker",
        )
        Skill.objects.create(
            owner=self.other_user,
            name="AWS",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Docker")

    def test_user_can_retrieve_own_skill(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="PostgreSQL",
        )

        response = self.client.get(
            reverse("skill-detail", args=[skill.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["name"],
            "PostgreSQL",
        )

    def test_user_cannot_retrieve_another_users_skill(self):
        skill = Skill.objects.create(
            owner=self.other_user,
            name="Kubernetes",
        )

        response = self.client.get(
            reverse("skill-detail", args=[skill.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_skill(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="Python",
        )

        response = self.client.patch(
            reverse("skill-detail", args=[skill.pk]),
            {"name": "Django"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        skill.refresh_from_db()
        self.assertEqual(skill.name, "Django")

    def test_user_cannot_update_another_users_skill(self):
        skill = Skill.objects.create(
            owner=self.other_user,
            name="AWS",
        )

        response = self.client.patch(
            reverse("skill-detail", args=[skill.pk]),
            {"name": "Azure"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        skill.refresh_from_db()
        self.assertEqual(skill.name, "AWS")

    def test_user_can_delete_own_skill(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="Docker",
        )

        response = self.client.delete(
            reverse("skill-detail", args=[skill.pk])
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Skill.objects.filter(pk=skill.pk).exists()
        )

    def test_user_cannot_delete_another_users_skill(self):
        skill = Skill.objects.create(
            owner=self.other_user,
            name="Docker",
        )

        response = self.client.delete(
            reverse("skill-detail", args=[skill.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Skill.objects.filter(pk=skill.pk).exists()
        )

    def test_anonymous_user_cannot_access_skills(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertIn(response.status_code, (401, 403))

    def test_api_client_cannot_set_owner(self):
        response = self.client.post(
            self.list_url,
            {
                "name": "Linux",
                "owner": self.other_user.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        skill = Skill.objects.get(name="Linux")
        self.assertEqual(skill.owner, self.user)
