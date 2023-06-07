from django.urls import path
from .views import CompanyCreateView, CompanyListView, CompanyUpdateView, \
                    EmployeeAPIView, EmployeeRetrieveUpdateDestroyView, \
                    EmployeesDeviceAssignmentsListView, DeviceAssesmentCreateView, \
                    DeviceAssesmentRetrieveUpdateDestroyView, DeviceStatusView, DeviceAssignmentsListView


urlpatterns = [
    path('create-company/', CompanyCreateView.as_view(), name='create-company'),
    path('update-company/<int:pk>/', CompanyUpdateView.as_view(), name='update-company'),
    path('company-list/', CompanyListView.as_view(), name='view-all-company-list'),

    path('employees-api/', EmployeeAPIView.as_view(), name='employee-list'),
    path('employees-api/<int:pk>/', EmployeeAPIView.as_view(), name='employee-detail'),

    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-rud'), # rud=RetrieveUpdateDestroy

    path('create-device-assesment/', DeviceAssesmentCreateView.as_view(), name='create-device-assesment'),
    path('device-assesment/<int:pk>/', DeviceAssesmentRetrieveUpdateDestroyView.as_view(), name='device-assesment-rud'),
    path('employees-devices/assignments/', EmployeesDeviceAssignmentsListView.as_view(), name='employee-assignments-list'),
    
    path('all-devices-assignments-list/', DeviceAssignmentsListView.as_view(), name='all-devices-assignments-list'),

    path('device-status/', DeviceStatusView.as_view({'get': 'list'}), name='device-status'),
]
