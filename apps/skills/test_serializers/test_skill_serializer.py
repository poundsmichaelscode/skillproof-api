from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.skills.models import Skill
from apps.skills.serializers import SkillSerializer


User = get_user_model()


class SkillSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="serializerowner",
            password="TestPassword123!",
        )
        self.factory = APIRequestFactory()

    def get_request(self, user=None):
        request = self.factory.post("/api/v1/skills/")
        force_authenticate(request, user=user or self.user)

        from rest_framework.request import Request
        return Request(request)

    def test_valid_skill_data(self):
        serializer = SkillSerializer(
            data={
                "name": "Python",
                "proficiency": "intermediate",
            },
            context={"request": self.get_request()},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["name"],
            "Python",
        )

    def test_name_is_trimmed(self):
        serializer = SkillSerializer(
            data={"name": "  Docker  "},
            context={"request": self.get_request()},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["name"],
            "Docker",
        )

    def test_blank_name_is_rejected(self):
        serializer = SkillSerializer(
            data={"name": "   "},
            context={"request": self.get_request()},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_proficiency_is_rejected(self):
        serializer = SkillSerializer(
            data={
                "name": "Python",
                "proficiency": "expert",
            },
            context={"request": self.get_request()},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("proficiency", serializer.errors)

    def test_duplicate_name_is_rejected(self):
        Skill.objects.create(
            owner=self.user,
            name="Python",
        )

        serializer = SkillSerializer(
            data={"name": "python"},
            context={"request": self.get_request()},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_owner_field_cannot_be_assigned(self):
        other_user = User.objects.create_user(
            username="anotherowner",
            password="TestPassword123!",
        )

        serializer = SkillSerializer(
            data={
                "name": "Django",
                "owner": other_user.pk,
            },
            context={"request": self.get_request()},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("owner", serializer.validated_data)

    def test_serializer_requires_authenticated_user(self):
        request = self.factory.post("/api/v1/skills/")

        from rest_framework.request import Request
        request = Request(request)

        serializer = SkillSerializer(
            data={"name": "Django"},
            context={"request": request},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
