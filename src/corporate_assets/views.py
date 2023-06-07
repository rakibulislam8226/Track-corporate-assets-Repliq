from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .serializers import CompanySerializer, EmployeeSerializer, DeviceAssesmentSerializer,DeviceAssesmentReturnedSerializer


# Create your views here.
#TODO: all permission classes have to be customize based on further requirements.

# Start Company Views #
class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


class CompanyUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]  ## it can be different regarding requirements.
# End Company Views #


# Start Employee Views #
class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk=None):
        try:
            if pk:
                employees = Employee.objects.get(pk=pk)
                serializer = EmployeeSerializer(employees)
                return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


    def post(self, request, pk=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(EmployeeSerializer(employee).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Employee can edit only his personal data.
class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            if self.object.id != request.user.employee.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(self.object)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not match."}, status=status.HTTP_404_NOT_FOUND)

# End Employee Views #

# Start Device Assesment Views #
class DeviceAssesmentCreateView(generics.CreateAPIView):
    queryset = DeviceAssesment.objects.all()
    serializer_class = DeviceAssesmentSerializer
    permission_classes = [IsAuthenticated]


class DeviceAssesmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceAssesment.objects.all()
    serializer_class = DeviceAssesmentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeviceAssignmentsListView(generics.ListAPIView):
    serializer_class = DeviceAssesmentSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return DeviceAssesment.objects.all()


## To see the request user Device Assesment list.
class EmployeesDeviceAssignmentsListView(generics.ListAPIView):
    serializer_class = DeviceAssesmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user_emp_id = self.request.user.employee.id
            return DeviceAssesment.objects.filter(employee_id=user_emp_id)
        except ObjectDoesNotExist:
            return DeviceAssesment.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"error": "No device assignments found for you."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Extra class for only check device checkout and returned info.  
class DeviceStatusView(ModelViewSet):
    queryset = DeviceAssesment.objects.all()
    serializer_class = DeviceAssesmentReturnedSerializer
    permission_classes = [DjangoObjectPermissions]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)