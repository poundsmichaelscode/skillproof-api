from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.skills.models import Skill


User = get_user_model()


class SkillModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="skillowner",
            password="TestPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="otherowner",
            password="TestPassword123!",
        )

    def test_user_can_create_skill(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="Python",
            proficiency=Skill.Proficiency.INTERMEDIATE,
        )

        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.owner, self.user)
        self.assertEqual(
            skill.proficiency,
            Skill.Proficiency.INTERMEDIATE,
        )

    def test_skill_name_is_trimmed(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="  Django  ",
        )

        self.assertEqual(skill.name, "Django")

    def test_different_users_can_have_same_skill(self):
        Skill.objects.create(
            owner=self.user,
            name="Python",
        )

        Skill.objects.create(
            owner=self.other_user,
            name="Python",
        )

        self.assertEqual(
            Skill.objects.filter(name="Python").count(),
            2,
        )

    def test_duplicate_skill_name_is_rejected_for_same_user(self):
        Skill.objects.create(
            owner=self.user,
            name="Python",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Skill.objects.create(
                    owner=self.user,
                    name="python",
                )

    def test_deleting_user_deletes_their_skills(self):
        skill = Skill.objects.create(
            owner=self.user,
            name="Docker",
        )

        self.user.delete()

        self.assertFalse(
            Skill.objects.filter(pk=skill.pk).exists()
        )
