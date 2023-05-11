from django.contrib import admin
from .models import Employee, Attendance, AttendanceByMonth


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


class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 0


class AttendanceByMonthInline(admin.StackedInline):
    model = AttendanceByMonth
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [AttendanceByMonthInline, AttendanceInline]
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'type', 'status')
    list_display_links = ('id', 'first_name',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('type', 'status')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'time_in', 'time_out')
    list_display_links = ('id', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__email')
    list_filter = (DateFilter,)
    list_editable = ('time_out', 'time_in')
    list_per_page = 200
