from django.contrib import admin
from .models import Department, Employee, LeaveRequest, Payslip
from .models import Evaluation
from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'arrival_time', 'departure_time')
    list_filter = ('date',)
    search_fields = ('employee__username',)



admin.site.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'rating')
    list_filter = ('date', 'rating')
    search_fields = ('employee__username', 'feedback')
# Enregistrement du modèle Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Enregistrement du modèle Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'hire_date', 'salary')
    search_fields = ('user__username', 'position')
    list_filter = ('department', 'hire_date')

# Action personnalisée pour LeaveRequestAdmin
@admin.action(description='Approuver les demandes sélectionnées')
def approve_requests(modeladmin, request, queryset):
    # Vérifiez que queryset est bien modifié
    updated_count = queryset.update(status='approved')
    modeladmin.message_user(request, f"{updated_count} demande(s) approuvée(s).")

@admin.action(description='Rejeter les demandes sélectionnées')
def reject_requests(modeladmin, request, queryset):
    updated_count = queryset.update(status='rejected')
    modeladmin.message_user(request, f"{updated_count} demande(s) rejetée(s).")

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('employee__username', 'reason')
    actions = [approve_requests, reject_requests]

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'base_salary', 'bonus', 'deductions')
    list_filter = ('month',)
    search_fields = ('employee__username',)

