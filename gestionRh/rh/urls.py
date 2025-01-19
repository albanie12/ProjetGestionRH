
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import employee_view, request_leave, view_payslip, custom_login, edit_profile, attendance_status, check_out, \
    check_in
from .views import employee_payslips
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import download_payslip
from .views import view_evaluations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', employee_view, name='employee'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page=''), name='logout'),
    path('employee/request-leave/', request_leave, name='request_leave'),
    path('employee/view-payslip/', view_payslip, name='view_payslip'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('employee/payslips/', employee_payslips, name='employee_payslips'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', login_required(admin.site.urls)),
    path('payslip/<int:payslip_id>/download/', download_payslip, name='download_payslip'),
    path('evaluations/', view_evaluations, name='view_evaluations'),
    path('check-in/', check_in, name='check_in'),
    path('check-out/', check_out, name='check_out'),
    path('attendance-status/', attendance_status, name='attendance_status'),
]

""""path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),"""

