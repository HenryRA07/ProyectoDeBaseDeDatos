# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    horario = models.CharField(max_length=100, blank=True, null=True)
    semestre = models.CharField(max_length=50, blank=True, null=True)
    id_profesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='id_profesor', blank=True, null=True)
    id_curso = models.ForeignKey('Curso', models.DO_NOTHING, db_column='id_curso', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clase'


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True) 
    codigo = models.CharField(unique=True, max_length=50)
    nombre_curso = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'curso'


class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=100)
    contrasenia = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'profesor'
