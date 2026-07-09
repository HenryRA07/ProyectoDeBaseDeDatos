from rest_framework import serializers
from modelo.models import Clase

class ClaseSerializer(serializers.ModelSerializer):
    nombre_curso = serializers.CharField(source='id_curso.nombre_curso')
    codigo_curso = serializers.CharField(source='id_curso.codigo')
    profesor = serializers.SerializerMethodField()

    class Meta:
        model = Clase
        fields = ['id_clase', 'horario', 'semestre', 'nombre_curso', 'codigo_curso', 'profesor']

    def get_profesor(self, obj):
        return f"{obj.id_profesor.nombre} {obj.id_profesor.apellido}"
