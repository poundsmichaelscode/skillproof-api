from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.opportunities.models import Opportunity


User = get_user_model()


class OpportunityModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="opportunityowner",
            password="StrongTestPass#8492",
        )

    def create_opportunity(self, **overrides):
        data = {
            "owner": self.user,
            "title": "Junior Backend Developer",
            "organization": "Example Technologies",
            "application_url": "https://example.com/careers",
        }
        data.update(overrides)
        return Opportunity.objects.create(**data)

    def test_create_opportunity(self):
        opportunity = self.create_opportunity()

        self.assertEqual(opportunity.owner, self.user)
        self.assertEqual(
            opportunity.title,
            "Junior Backend Developer",
        )

    def test_title_and_organization_are_trimmed(self):
        opportunity = self.create_opportunity(
            title="  DevOps Engineer  ",
            organization="  Example Company  ",
        )

        self.assertEqual(opportunity.title, "DevOps Engineer")
        self.assertEqual(opportunity.organization, "Example Company")

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_opportunity(title="   ")

    def test_empty_organization_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_opportunity(organization="   ")

    def test_invalid_application_url_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.create_opportunity(
                application_url="not-a-valid-url"
            )

    def test_closing_date_is_optional(self):
        opportunity = self.create_opportunity()

        self.assertIsNone(opportunity.closing_date)

    def test_closing_date_can_be_saved(self):
        opportunity = self.create_opportunity(
            closing_date=date(2027, 1, 31)
        )

        self.assertEqual(
            opportunity.closing_date,
            date(2027, 1, 31),
        )

    def test_deleting_owner_deletes_opportunity(self):
        opportunity = self.create_opportunity()
        opportunity_id = opportunity.pk

        self.user.delete()

        self.assertFalse(
            Opportunity.objects.filter(pk=opportunity_id).exists()
        )

    def test_string_representation(self):
        opportunity = self.create_opportunity()

        self.assertEqual(
            str(opportunity),
            "Junior Backend Developer - Example Technologies",
        )
