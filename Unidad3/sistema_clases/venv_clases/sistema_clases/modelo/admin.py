from django.contrib import admin
from .models import Profesor, Curso, Clase

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('id_profesor', 'nombre', 'apellido', 'correo')
    search_fields = ('nombre', 'apellido', 'correo')

class CursoAdmin(admin.ModelAdmin):
    list_display = ('id_curso', 'codigo', 'nombre_curso')
    search_fields = ('codigo', 'nombre_curso')
    
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('id_clase', 'horario', 'semestre', 'id_profesor', 'id_curso')
    search_fields = ('horario', 'semestre')
    list_filter = ('semestre',)

# Registrar todos
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Clase, ClaseAdmin)