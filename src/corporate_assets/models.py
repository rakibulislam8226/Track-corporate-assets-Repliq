from django.db import models
from django.contrib.auth.models import User
from config.models.TimeStampMixin import TimeStampMixin


# Create your models here.
class Employee(TimeStampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    device = models.ManyToManyField("DeviceInfo", related_name='device_info')

    def __str__(self):
        return f'{self.user.username}'


class Company(TimeStampMixin):
    name = models.CharField(max_length=255, help_text = "Enter company name.")
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16, unique=True)
    website_url = models.URLField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'
    

class DeviceInfo(TimeStampMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text = "Enter device name.")
    device_code = models.CharField(max_length=255, unique=True)
    conditions = models.CharField(max_length=100, default='100%', help_text = "Tell about the conditions of this device.")
    checked_out = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    

    class Meta:
        verbose_name_plural = 'Device Informations'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'


class DeviceAssesment(TimeStampMixin):
    device = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Device Assesment'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.device.name} - '