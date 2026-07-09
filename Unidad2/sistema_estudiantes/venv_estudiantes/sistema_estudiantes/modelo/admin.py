from django.contrib import admin
from .models import Estudiante, Inscripcion, Asistencia

# ---------- Estudiante ----------
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id_estudiante', 'nombre', 'apellido', 'correo')
    search_fields = ('nombre', 'apellido', 'correo')

# ---------- Inscripcion ----------
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id_inscripcion', 'estado', 'fecha', 'id_estudiante', 'id_clase')
    search_fields = ('estado',)
    list_filter = ('estado', 'fecha')

# ---------- Asistencia ----------
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id_asistencia', 'fecha', 'estado', 'justificacion', 'id_inscripcion')
    search_fields = ('estado', 'justificacion')
    list_filter = ('estado', 'fecha')

# Registrar todos los modelos
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)