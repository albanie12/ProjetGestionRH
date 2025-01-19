from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeaveRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import Payslip
from .models import Evaluation

from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import Attendance
from django.contrib.auth.decorators import login_required

@login_required
def check_in(request):
    """Marquer l'arrivée de l'employé."""
    if request.method == 'POST':
        # Vérifiez si un enregistrement pour aujourd'hui existe déjà
        attendance, created = Attendance.objects.get_or_create(employee=request.user, date=now().date())
        if not attendance.arrival_time:  # Si l'arrivée n'a pas encore été marquée
            attendance.arrival_time = now().time()
            attendance.save()
        return redirect('attendance_status')  # Redirigez vers le statut des présences

@login_required
def check_out(request):
    """Marquer le départ de l'employé."""
    if request.method == 'POST':
        try:
            # Récupérez l'enregistrement de l'employé pour aujourd'hui
            attendance = Attendance.objects.get(employee=request.user, date=now().date())
            if not attendance.departure_time:  # Si le départ n'a pas encore été marqué
                attendance.departure_time = now().time()
                attendance.save()
        except Attendance.DoesNotExist:
            pass  # Aucun enregistrement trouvé pour aujourd'hui
        return redirect('attendance_status')  # Redirigez vers le statut des présences

@login_required
def attendance_status(request):
    """Afficher le statut actuel de présence de l'employé."""
    try:
        attendance = Attendance.objects.get(employee=request.user, date=now().date())
    except Attendance.DoesNotExist:
        attendance = None
    return render(request, 'attendance_status.html', {'attendance': attendance})


def view_evaluations(request):
    evaluations = Evaluation.objects.filter(employee=request.user)
    return render(request, 'employee_evaluations.html', {'evaluations': evaluations})

def download_payslip(request, payslip_id):
    try:
        payslip = Payslip.objects.get(id=payslip_id, employee=request.user)
    except Payslip.DoesNotExist:
        return HttpResponse("Fiche de paie introuvable.", status=404)

    # Récupérer l'employé et son département
    try:
        employee = payslip.employee.employee  # Accéder à l'objet Employee
        department = employee.department.name if employee.department else "Non assigné"
    except AttributeError:
        department = "Non assigné"  # Si aucun objet Employee n'est trouvé

    # Calcul du salaire total
    total_salary = payslip.base_salary + payslip.bonus - payslip.deductions

    # Rendu du template HTML
    html_content = render_to_string('rh/payslip_template.html', {
        'payslip': payslip,
        'total_salary': total_salary,
        'department': department,  # Ajouter le département au contexte
    })

    # Génération du PDF
    pdf_file = HTML(string=html_content).write_pdf()

    # Réponse HTTP avec le PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Payslip_{payslip.month.strftime("%B_%Y")}.pdf"'

    return response







def employee_payslips(request):
    # Récupère uniquement les fiches de paie de l'utilisateur connecté
    payslips = Payslip.objects.filter(employee=request.user)
    return render(request, 'employee_payslips.html', {'payslips': payslips})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('employee')
    return render(request, 'edit_profile.html')


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

def home_page(request):
    return render(request, 'home.html')
