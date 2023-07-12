from django.test import TestCase
from django.db import connection
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Employee, Company, DeviceInfo


class TestEmployeeAPI(TestCase):

    def setUp(self):
        
        self.client = APIClient()
        user1 = User.objects.create(username='testuser', password="abcd123")
        user2 = User.objects.create(username='testuser2', password="abcd123")
        self.user3 = User.objects.create(username='testuser3', password="abcd123")

        company1 = Company.objects.create(name='Example Company',location="Lalmatia", phone_number="01776068", website_url="https://docs.djangoproject.com/")
        company2 = Company.objects.create(name='Example Company 2',location="Lalmatia 2", phone_number="017760681", website_url="https://docs.djangoproject2.com/")

        device_info_1 = DeviceInfo.objects.create(company=company1, name="device info 1",device_code="5432", conditions="100%")
        self.device_info_2 = DeviceInfo.objects.create(company=company2, name="device info 1",device_code="54321", conditions="100%")

        self.employee1 = Employee.objects.create(user=user1, company=company1)
        self.employee1.device.set([device_info_1]) # reason many_to_many fields.

        self.employee2 = Employee.objects.create(user=user2, company=company1)
        self.employee2.device.set([device_info_1]) # many_to_many fields.

        self.create_employee_list = reverse("employee-list")

    def test_get_employees(self):
        
        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user) # Login the admin user

        res = self.client.get('/employees-api/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


    def test_get_employee(self):
        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user) # Login the admin user

        response = self.client.get("/employees-api/{}/".format(self.employee1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['user'], self.employee1.user.id)
        self.assertEqual(response.data["company"], self.employee1.company.id)


    def test_post_employee(self):
        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user)  # Login the admin user

        employee_data = {
            'user': self.user3.id,
            'company': self.employee1.company.id,
            'device': [self.device_info_2.id],
        }

        response = self.client.post(self.create_employee_list, data=employee_data)
        # if response.status_code != status.HTTP_201_CREATED:
        #     print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_put_employee(self):
        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user)  # Login the admin user

        update_employee_data = {
            'user': self.user3.id,
            'company': self.employee2.company.id,
            'device': [self.device_info_2.id],
        }
        response = self.client.put("/employees-api/{}/".format(self.employee1.id), data=update_employee_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_employee(self):
        # Create and authenticate an admin user
        admin_user = User.objects.create_user(username='admin', password='password')
        admin_user.is_staff = True
        admin_user.save()
        self.client.force_login(admin_user)  # Login the admin user

        response = self.client.delete(f"/employees-api/{self.employee1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee1.id).exists()) # check it is not exists



