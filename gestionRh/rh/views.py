from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeaveRequest


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('employee')  # Redirige vers la page employee
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Utilisez votre template de connexion
    redirect_authenticated_user = True  # Si l'utilisateur est déjà connecté, redirige-le automatiquement
    success_url = '/employee/'  # Redirection après connexion réussie

    def get_success_url(self):
        # Cette méthode garantit que l'utilisateur est toujours redirigé vers /employee/
        return self.success_url


def view_payslip(request):
    return render(request, 'view_payslip.html')  # Créez ce template plus tard


def request_leave(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Crée une nouvelle demande de congé
        LeaveRequest.objects.create(
            employee=request.user,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )

        messages.success(request, "Votre demande de congé a été soumise avec succès !")
        return redirect('employee')  # Redirige vers la page employé

    return render(request, 'request_leave.html')  # Créez ce template plus tard

def employee_view(request):
    return render(request, 'rh/employee.html')
