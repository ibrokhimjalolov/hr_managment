from datetime import datetime

from celery import shared_task

from apps.hr_management.models import Employee, Attendance, EmployeeStatus


@shared_task(name="create_today_attendance")
def create_today_attendance():
    today = datetime.today()
    if today.weekday() == 6:
        # if today is sunday
        return
    for employee in Employee.objects.filter(status=EmployeeStatus.ACTIVE):
        Attendance.objects.get_or_create(
            employee=employee, date=today,
        )
