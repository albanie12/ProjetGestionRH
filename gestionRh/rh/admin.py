from django.contrib import admin
from .models import Department, Employee, LeaveRequest, Payslip


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
    queryset.update(status='Approved')

@admin.action(description='Rejeter les demandes sélectionnées')
def reject_requests(modeladmin, request, queryset):
    queryset.update(status='Rejected')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('employee__username', 'reason')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'base_salary', 'bonus', 'deductions', 'total_salary')
    search_fields = ('employee__user__username', 'month')
    list_filter = ('month',)

