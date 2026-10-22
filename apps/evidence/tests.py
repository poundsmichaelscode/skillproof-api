from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.evidence.models import Evidence
from apps.skills.models import Skill


User = get_user_model()


class EvidenceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="evidence_owner",
            password="StrongTestPass#8492",
        )
        self.other_user = User.objects.create_user(
            username="other_evidence_owner",
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

    def test_create_evidence(self):
        evidence = Evidence.objects.create(
            owner=self.user,
            skill=self.skill,
            title="Django REST API Project",
            evidence_url="https://github.com/example/project",
        )

        self.assertEqual(evidence.owner, self.user)
        self.assertEqual(evidence.skill, self.skill)

    def test_title_is_trimmed(self):
        evidence = Evidence.objects.create(
            owner=self.user,
            skill=self.skill,
            title="  Backend Project  ",
            evidence_url="https://example.com/project",
        )

        self.assertEqual(evidence.title, "Backend Project")

    def test_other_users_skill_is_rejected(self):
        with self.assertRaises(ValidationError):
            Evidence.objects.create(
                owner=self.user,
                skill=self.other_skill,
                title="Invalid Evidence",
                evidence_url="https://example.com/project",
            )

    def test_invalid_url_is_rejected(self):
        with self.assertRaises(ValidationError):
            Evidence.objects.create(
                owner=self.user,
                skill=self.skill,
                title="Project",
                evidence_url="not-a-valid-url",
            )

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValidationError):
            Evidence.objects.create(
                owner=self.user,
                skill=self.skill,
                title="   ",
                evidence_url="https://example.com/project",
            )

    def test_deleting_skill_deletes_evidence(self):
        evidence = Evidence.objects.create(
            owner=self.user,
            skill=self.skill,
            title="Python Project",
            evidence_url="https://example.com/project",
        )

        evidence_id = evidence.pk
        self.skill.delete()

        self.assertFalse(
            Evidence.objects.filter(pk=evidence_id).exists()
        )

    def test_deleting_user_deletes_evidence(self):
        evidence = Evidence.objects.create(
            owner=self.user,
            skill=self.skill,
            title="Python Certificate",
            evidence_url="https://example.com/certificate",
        )

        evidence_id = evidence.pk
        self.user.delete()

        self.assertFalse(
            Evidence.objects.filter(pk=evidence_id).exists()
        )
