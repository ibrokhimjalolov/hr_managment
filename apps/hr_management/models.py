from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class EmployeeType(models.TextChoices):
    EMPLOYEE = 'EMPLOYEE', 'Employee'
    INTERN = 'INTERN', 'Intern'


class EmployeeStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'


class Employee(models.Model):
    type = models.CharField(max_length=10, choices=EmployeeType.choices, default=EmployeeType.EMPLOYEE)
    status = models.CharField(max_length=10, choices=EmployeeStatus.choices, default=EmployeeStatus.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name + "|" + self.get_status_display() + "|" + self.get_type_display()

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["first_name", "last_name"]


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField()
    time_out = models.TimeField()

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name + " " + str(self.date)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ["-date"]
        unique_together = ('employee', 'date')
