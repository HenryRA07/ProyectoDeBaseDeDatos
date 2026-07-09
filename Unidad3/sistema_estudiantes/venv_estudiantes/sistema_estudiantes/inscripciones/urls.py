from django.urls import path
from .views import inscribir_estudiante

urlpatterns = [
    path('', inscribir_estudiante, name='inscripciones'),
]
