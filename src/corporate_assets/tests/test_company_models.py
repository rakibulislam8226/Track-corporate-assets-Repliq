from django.test import TestCase
from django.db import connection
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Company
from ..serializers import CompanySerializer


class TestCompanyModel(TestCase):

    def setUp(self):
        """Initial setup for testing."""
        self.client = APIClient()
        self.company = Company.objects.create(name='Example Company',location="Lalmatia", phone_number="01776068", website_url="https://docs.djangoproject.com/")
        self.company2 = Company.objects.create(name='Example Company 2',location="Lalmatia", phone_number="01776068 2", website_url="https://docs.djangoproject1.com/")
        self.create_company_url = reverse("create-company")
        self.update_company_url = reverse('update-company', kwargs={'pk': self.company.pk})
        self.list_company_url = reverse("view-all-company-list")

        self.payload = {
            'name': 'Example Company',
            'location': '123 Main St',
            'phone_number': '023943',
            'website_url': 'https://docs.djangoproject12.com/'
        }
        self.payload2 = {
            'name': 'Example Company',
            'location': '123 Main St',
            'phone_number': '023943',
            'website_url': 'https://docs.djangoproject124.com/'
        }


    def test_company_model_exists(self):
        """Check the Company models are exists in models"""
        self.assertTrue(hasattr(Company, '__name__')) # "__name__" attribute is a way to determine the model class exists.
        self.assertIn('corporate_assets_company', connection.introspection.table_names()) # The assertIn assertion checks if the table name is present in database


    def test_company_dunder_method(self):
        self.assertEqual(str(self.company), self.company.name)


    def test_create_company(self):
        # Create a user and authenticate as that user
        user = User.objects.create(username='testuser', password="abcd123")
        self.client.force_authenticate(user=user)

        response = self.client.post(self.create_company_url, self.payload2, format='json')

        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        company = Company.objects.first()
        self.assertEqual(company.name, 'Example Company')
        # add another fields to test. here tested name only.


    def test_update_company(self):

        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user) # Login the admin user

        updated_name = 'Updated Company'
        updated_location = '456 Updated St'

        payload = {
            'name': updated_name,
            'location': updated_location,
        }

        response = self.client.patch(self.update_company_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the company instance from the database
        self.company.refresh_from_db()

        self.assertEqual(self.company.name, updated_name)
        self.assertEqual(self.company.location, updated_location)


    def test_company_list(self):

        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user) # Login the admin user

        res = self.client.get(self.list_company_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)

        self.assertEqual(res.data, serializer.data)
