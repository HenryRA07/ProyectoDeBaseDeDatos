# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    justificacion = models.TextField(blank=True, null=True)
    id_inscripcion = models.ForeignKey('Inscripcion', models.DO_NOTHING, db_column='id_inscripcion')

    class Meta:
        managed = False
        db_table = 'asistencia'


class Estudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contrasenia = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'estudiante'



class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    id_estudiante = models.IntegerField(blank=True, null=True)
    id_clase = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inscripcion'
