from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    total_seconds = models.IntegerField(null=True, blank=True, editable=False)

    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name + " " + str(self.date)

    def clean(self):
        if self.time_out and self.time_in and self.time_out < self.time_in:
            raise ValidationError("Time out must be greater than time in")

    def save(self, *args, **kwargs):
        if self.time_out and self.time_in:
            self.total_seconds = (
                self.time_out.hour * 60 * 60 + self.time_out.minute * 60 + self.time_out.second -
                self.time_in.hour * 60 * 60 - self.time_in.minute * 60 - self.time_in.second
            )

        super().save(*args, **kwargs)
        a, _ = AttendanceByMonth.objects.get_or_create(
            employee=self.employee, month=self.date.month, year=self.date.year
        )
        a.total_work_hours = Attendance.objects.filter(
            employee=self.employee, date__month=self.date.month, date__year=self.date.year
        ).aggregate(models.Sum('total_seconds'))['total_seconds__sum'] or 0
        a.total_work_hours = round(a.total_work_hours / 3600, 2)
        a.total_work_days = Attendance.objects.filter(
            employee=self.employee, date__month=self.date.month, date__year=self.date.year
        ).count()
        a.save()

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
        ordering = ["-date"]
        unique_together = ('employee', 'date')


class MonthChoices(models.IntegerChoices):
    JAN = 1, 'January'
    FEB = 2, 'February'
    MAR = 3, 'March'
    APR = 4, 'April'
    MAY = 5, 'May'
    JUN = 6, 'June'
    JUL = 7, 'July'
    AUG = 8, 'August'
    SEP = 9, 'September'
    OCT = 10, 'October'
    NOV = 11, 'November'
    DEC = 12, 'December'


class AttendanceByMonth(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MonthChoices.choices)
    year = models.IntegerField()
    total_work_days = models.IntegerField(default=0)
    total_work_hours = models.FloatField(default=0)

    def __str__(self):
        return self.get_month_display() + " " + str(self.year)
