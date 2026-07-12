from djongo import models

# 1. Estructura Abstracta para Asistencia (Se embeberá como un array de objetos)
class Asistencia(models.Model):
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    justificacion = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True  # Evita que Djongo cree una colección independiente

# 2. Estructura Abstracta para desnormalizar datos desde el Web Service de la App 1
class ClaseInfo(models.Model):
    nombre_curso = models.CharField(max_length=100, blank=True, null=True)
    codigo_curso = models.CharField(max_length=50, blank=True, null=True)
    horario = models.CharField(max_length=100, blank=True, null=True)
    semestre = models.CharField(max_length=50, blank=True, null=True)
    profesor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

# 3. Modelo de Estudiante (Colección independiente)
class Estudiante(models.Model):
    # Usamos IntegerField para conservar exactamente los mismos IDs numéricos que ya tienes en Postgres
    id_estudiante = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contrasenia = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# 4. Modelo de Inscripción (Documento raíz NoSQL con todo embebido)
class Inscripcion(models.Model):
    id_inscripcion = models.IntegerField(primary_key=True) # Conserva el ID de Postgres
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    id_clase_externo = models.IntegerField(blank=True, null=True)  # Equivale a id_clase de Postgres
    estado = models.CharField(max_length=50, blank=True, null=True, default='Activo')
    fecha_inscripcion = models.DateField(blank=True, null=True)     # Equivale a fecha de Postgres

    # El array embebido NoSQL que guardará la lista de asistencias del alumno
    asistencias = models.ArrayField(
        model_container=Asistencia,
        blank=True,
        default=list
    )
    
    # El subdocumento embebido para almacenar la respuesta del Web Service posterior
    clase_info = models.EmbeddedField(
        model_container=ClaseInfo,
        blank=True,
        null=True
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - Estudiante: {self.estudiante.apellido}"