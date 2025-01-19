from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username




class LeaveRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')  # Liaison avec l'utilisateur
    start_date = models.DateField()  # Date de début du congé
    end_date = models.DateField()  # Date de fin du congé
    reason = models.TextField()  # Raison du congé
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'En attente'), ('approved', 'Approuvé'), ('rejected', 'Rejeté')],
        default='pending'
    )  # Statut de la demande
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date} ({self.status})"
class Payslip(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payslips')
    month = models.DateField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%B %Y')}"


    def save(self, *args, **kwargs):
        self.total_salary = self.base_salary + self.bonus - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payslip for {self.employee.get_full_name()} - {self.month.strftime('%B %Y')}"


class Evaluation(models.Model):
        employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
        date = models.DateField(auto_now_add=True)
        rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note de 1 à 5
        feedback = models.TextField()  # Commentaires de l'admin

        def __str__(self):
            return f"Évaluation de {self.employee.get_full_name()} - {self.date}"

        class Meta:
            ordering = ['-date']

class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)  # Date de la présence (par défaut la date du jour)
    arrival_time = models.TimeField(null=True, blank=True)  # Heure d'arrivée
    departure_time = models.TimeField(null=True, blank=True)  # Heure de départ

    def __str__(self):
        return f"{self.employee.username} - {self.date}"

    class Meta:
        ordering = ['-date']  # Trier les présences par date décroissante
