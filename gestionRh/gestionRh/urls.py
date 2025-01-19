from django.contrib import admin
from django.urls import path, include
from rh.views import home_page  # Importez la vue de la page principale

urlpatterns = [
    path('', home_page, name='home'),  # Page principale (choix entre employé et admin)
    path('admin/', admin.site.urls),  # Administration Django
    path('rh/', include('rh.urls')),  # Inclut toutes les URLs de l'application "rh"
]

