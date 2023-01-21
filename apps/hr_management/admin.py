from django.contrib import admin
from .models import Employee, Attendance


class DateFilter(admin.SimpleListFilter):
    parameter_name = 'date'
    title = 'Date'

    def lookups(self, request, model_admin):
        return [
            (i, i) for i in model_admin.model.objects.values_list('date', flat=True).distinct('date')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date=self.value())
        return queryset


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'email')
    list_display_links = ('id', 'first_name',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('type', 'status')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'time_in', 'time_out')
    list_display_links = ('id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__email')
    list_filter = (DateFilter,)
