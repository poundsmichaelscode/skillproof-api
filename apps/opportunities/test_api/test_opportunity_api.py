from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.opportunities.models import Opportunity


User = get_user_model()


class OpportunityAPITests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="opportunity_owner",
            password="StrongTestPass#8492",
        )
        self.other = User.objects.create_user(
            username="opportunity_other",
            password="StrongTestPass#8492",
        )
        self.admin = User.objects.create_user(
            username="opportunity_admin",
            password="StrongTestPass#8492",
            is_staff=True,
        )

        self.opportunity = Opportunity.objects.create(
            owner=self.owner,
            title="Junior Backend Developer",
            organization="Example Technologies",
            application_url="https://example.com/jobs/1",
        )

        self.client = APIClient()
        self.list_url = reverse("opportunity-list")

    def authenticate(self, user):
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )

    def detail_url(self):
        return reverse(
            "opportunity-detail",
            args=[self.opportunity.pk],
        )

    def test_authenticated_user_can_list_opportunities(self):
        self.authenticate(self.other)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_authenticated_user_can_read_another_users_opportunity(self):
        self.authenticate(self.other)

        response = self.client.get(self.detail_url())

        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_create_opportunity(self):
        self.authenticate(self.other)

        response = self.client.post(
            self.list_url,
            {
                "title": "DevOps Engineer",
                "organization": "Tech Company",
                "application_url": "https://example.com/jobs/2",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        created = Opportunity.objects.get(title="DevOps Engineer")
        self.assertEqual(created.owner, self.other)

    def test_client_cannot_spoof_owner(self):
        self.authenticate(self.other)

        response = self.client.post(
            self.list_url,
            {
                "owner": self.owner.pk,
                "title": "Cloud Engineer",
                "organization": "Tech Company",
                "application_url": "https://example.com/jobs/3",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        created = Opportunity.objects.get(title="Cloud Engineer")
        self.assertEqual(created.owner, self.other)

    def test_owner_can_update_opportunity(self):
        self.authenticate(self.owner)

        response = self.client.patch(
            self.detail_url(),
            {"title": "Senior Backend Developer"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.opportunity.refresh_from_db()
        self.assertEqual(
            self.opportunity.title,
            "Senior Backend Developer",
        )

    def test_non_owner_cannot_update_opportunity(self):
        self.authenticate(self.other)

        response = self.client.patch(
            self.detail_url(),
            {"title": "Unauthorized Update"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

        self.opportunity.refresh_from_db()
        self.assertEqual(
            self.opportunity.title,
            "Junior Backend Developer",
        )

    def test_non_owner_cannot_delete_opportunity(self):
        self.authenticate(self.other)

        response = self.client.delete(self.detail_url())

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Opportunity.objects.filter(
                pk=self.opportunity.pk
            ).exists()
        )

    def test_owner_can_delete_opportunity(self):
        self.authenticate(self.owner)

        response = self.client.delete(self.detail_url())

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Opportunity.objects.filter(
                pk=self.opportunity.pk
            ).exists()
        )

    def test_staff_admin_can_update_opportunity(self):
        self.authenticate(self.admin)

        response = self.client.patch(
            self.detail_url(),
            {"title": "Admin Updated"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.opportunity.refresh_from_db()
        self.assertEqual(self.opportunity.title, "Admin Updated")

    def test_staff_admin_can_delete_opportunity(self):
        self.authenticate(self.admin)

        response = self.client.delete(self.detail_url())

        self.assertEqual(response.status_code, 204)

    def test_invalid_url_rejected(self):
        self.authenticate(self.owner)

        response = self.client.post(
            self.list_url,
            {
                "title": "Invalid Opportunity",
                "organization": "Tech Company",
                "application_url": "not-a-url",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_title_rejected(self):
        self.authenticate(self.owner)

        response = self.client.post(
            self.list_url,
            {
                "title": "   ",
                "organization": "Tech Company",
                "application_url": "https://example.com/job",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_user_rejected(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 401)
