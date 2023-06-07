from django.contrib import admin
from .models import Employee, Company, DeviceInfo, DeviceAssesment


# Register your models here.
admin.site.register(Employee)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'website_url', 'location')
    search_fields = ('name', 'phone_number', 'location')
    list_filter = ('phone_number', 'location')


@admin.register(DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'device_code', 'checked_out')
    search_fields = ('name', 'device_code', 'company__name')
    list_filter = ('device_code', 'company', 'checked_out')
    list_editable = ('checked_out',)
    date_hierarchy = 'created_at'


@admin.register(DeviceAssesment)
class DeviceAssesmentAdmin(admin.ModelAdmin):
    list_display = ('device', 'employee', 'checkout_date', 'return_date')
    search_fields = ('company__name',)
    date_hierarchy = 'checkout_date'
