from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.evidence.models import Evidence
from apps.skills.models import Skill


User = get_user_model()


class EvidenceAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="evidenceapiuser",
            password="StrongTestPass#8492",
        )
        self.other_user = User.objects.create_user(
            username="otherevidenceapiuser",
            password="StrongTestPass#8492",
        )

        self.skill = Skill.objects.create(
            owner=self.user,
            name="Python",
        )
        self.other_skill = Skill.objects.create(
            owner=self.other_user,
            name="Docker",
        )

        self.evidence = Evidence.objects.create(
            owner=self.user,
            skill=self.skill,
            title="Python Project",
            evidence_url="https://example.com/python",
        )
        self.other_evidence = Evidence.objects.create(
            owner=self.other_user,
            skill=self.other_skill,
            title="Docker Project",
            evidence_url="https://example.com/docker",
        )

        self.client = APIClient()
        self.list_url = reverse("evidence-list")

        token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )

    def test_user_can_list_only_own_evidence(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["title"],
            "Python Project",
        )

    def test_user_can_create_evidence(self):
        response = self.client.post(
            self.list_url,
            {
                "skill": self.skill.pk,
                "title": "Python Certificate",
                "evidence_url": "https://example.com/certificate",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        created = Evidence.objects.get(
            title="Python Certificate"
        )
        self.assertEqual(created.owner, self.user)
        self.assertEqual(created.skill, self.skill)

    def test_cannot_create_for_another_users_skill(self):
        response = self.client.post(
            self.list_url,
            {
                "skill": self.other_skill.pk,
                "title": "Unauthorized Evidence",
                "evidence_url": "https://example.com/project",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            Evidence.objects.filter(
                title="Unauthorized Evidence"
            ).exists()
        )

    def test_user_can_retrieve_own_evidence(self):
        response = self.client.get(
            reverse(
                "evidence-detail",
                args=[self.evidence.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Python Project",
        )

    def test_cannot_retrieve_another_users_evidence(self):
        response = self.client.get(
            reverse(
                "evidence-detail",
                args=[self.other_evidence.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_evidence(self):
        response = self.client.patch(
            reverse(
                "evidence-detail",
                args=[self.evidence.pk],
            ),
            {"title": "Updated Python Project"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.evidence.refresh_from_db()
        self.assertEqual(
            self.evidence.title,
            "Updated Python Project",
        )

    def test_cannot_link_to_another_users_skill(self):
        response = self.client.patch(
            reverse(
                "evidence-detail",
                args=[self.evidence.pk],
            ),
            {"skill": self.other_skill.pk},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        self.evidence.refresh_from_db()
        self.assertEqual(
            self.evidence.skill,
            self.skill,
        )

    def test_cannot_modify_another_users_evidence(self):
        response = self.client.patch(
            reverse(
                "evidence-detail",
                args=[self.other_evidence.pk],
            ),
            {"title": "Unauthorized Change"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_evidence(self):
        response = self.client.delete(
            reverse(
                "evidence-detail",
                args=[self.evidence.pk],
            )
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Evidence.objects.filter(
                pk=self.evidence.pk
            ).exists()
        )

    def test_cannot_delete_another_users_evidence(self):
        response = self.client.delete(
            reverse(
                "evidence-detail",
                args=[self.other_evidence.pk],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Evidence.objects.filter(
                pk=self.other_evidence.pk
            ).exists()
        )

    def test_owner_cannot_be_spoofed(self):
        response = self.client.post(
            self.list_url,
            {
                "skill": self.skill.pk,
                "owner": self.other_user.pk,
                "title": "Secure Evidence",
                "evidence_url": "https://example.com/secure",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        created = Evidence.objects.get(
            title="Secure Evidence"
        )
        self.assertEqual(created.owner, self.user)

    def test_invalid_url_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {
                "skill": self.skill.pk,
                "title": "Invalid URL",
                "evidence_url": "not-a-url",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_title_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {
                "skill": self.skill.pk,
                "title": "   ",
                "evidence_url": "https://example.com/project",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_anonymous_user_is_rejected(self):
        self.client.credentials()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 401)
