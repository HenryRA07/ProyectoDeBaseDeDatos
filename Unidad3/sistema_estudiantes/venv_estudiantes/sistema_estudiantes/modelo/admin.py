from django.contrib import admin
from .models import Estudiante, Inscripcion

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id_estudiante', 'nombre', 'apellido', 'correo', 'activo')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('activo',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id_inscripcion', 'estudiante', 'id_clase_externo', 'estado', 'fecha_inscripcion')
    search_fields = ('id_inscripcion', 'estudiante__apellido', 'estado')
    list_filter = ('estado',)
    
    # Nota: Las asistencias al estar embebidas como un Array NoSQL se renderizarán 
    # de forma automática dentro del formulario de edición de cada Inscripción.