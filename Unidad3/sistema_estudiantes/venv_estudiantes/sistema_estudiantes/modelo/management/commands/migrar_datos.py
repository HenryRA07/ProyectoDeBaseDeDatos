import psycopg2
from django.core.management.base import BaseCommand
from django.utils.timezone import now
# Reemplaza 'estudiantes' por el nombre real de tu aplicación Django si es diferente
from modelo.models import Estudiante, Inscripcion

class Command(BaseCommand):
    help = 'Migra de forma limpia los datos de PostgreSQL a MongoDB usando Djongo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=== Iniciando Proceso de Migración ==='))

        # 1. Configuración de la conexión a PostgreSQL (Datos de origen)
        pg_config = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'bd_estudiantes',
            'user': 'henry_estudiantes',
            'password': '123456',
        }

        try:
            pg_conn = psycopg2.connect(**pg_config)
            cur_est = pg_conn.cursor()
            cur_insc = pg_conn.cursor()
            cur_asist = pg_conn.cursor()
            self.stdout.write(self.style.SUCCESS('✓ Conexión exitosa a PostgreSQL.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error al conectar a PostgreSQL: {e}'))
            return

        # 2. Limpiar datos existentes en MongoDB para evitar duplicados
        self.stdout.write('Limpiando colecciones en MongoDB...')
        Inscripcion.objects.all().delete()
        Estudiante.objects.all().delete()

        # 3. MIGRAR ESTUDIANTES
        self.stdout.write('Migrando estudiantes...')
        cur_est.execute("SELECT id_estudiante, nombre, apellido, correo, contrasenia FROM estudiante ORDER BY id_estudiante;") 
        
        for row in cur_est.fetchall():
            id_est, nombre, apellido, correo, contrasenia = row
            Estudiante.objects.create(
                id_estudiante=id_est,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contrasenia=contrasenia,
                activo=True
            )
        self.stdout.write(self.style.SUCCESS(f'✓ Estudiantes migrados correctamente.'))

        # 4. MIGRAR INSCRIPCIONES Y ASISTENCIAS EMBEBIDAS
        self.stdout.write('Migrando inscripciones con asistencias embebidas...')
        cur_insc.execute("SELECT id_inscripcion, estado, fecha, id_estudiante, id_clase FROM inscripcion ORDER BY id_inscripcion;")
        
        inscripciones_migradas = 0
        for row_insc in cur_insc.fetchall():
            id_insc, estado, fecha, id_estudiante, id_clase_externo = row_insc

            # Buscar el estudiante ya creado en MongoDB para mantener la consistencia
            try:
                estudiante_obj = Estudiante.objects.get(id_estudiante=id_estudiante)
            except Estudiante.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Estudiante {id_estudiante} no encontrado en MongoDB. Saltando inscripción.'))
                continue

            # Obtener las asistencias correspondientes de PostgreSQL para este ID de inscripción
            cur_asist.execute("SELECT fecha, estado, justificacion FROM asistencia WHERE id_inscripcion = %s ORDER BY fecha;", (id_insc,))
            
            # Construir la lista de diccionarios que Djongo guardará como un Array NoSQL
            lista_asistencias = []
            for row_asist in cur_asist.fetchall():
                f_asist, est_asist, just_asist = row_asist
                lista_asistencias.append({
                    'fecha': f_asist,
                    'estado': est_asist,
                    'justificacion': just_asist or ''
                })

            # Crear el documento raíz en MongoDB utilizando el ORM de Djongo
            Inscripcion.objects.create(
                id_inscripcion=id_insc,
                estudiante=estudiante_obj,
                id_clase_externo=id_clase_externo,
                estado=estado or 'Activo',
                fecha_inscripcion=fecha,
                asistencias=lista_asistencias, # Se guarda directamente como Array NoSQL
                clase_info=None # Se poblará dinámicamente o mediante el WS más adelante
            )
            inscripciones_migradas += 1

        # Cerrar conexiones
        cur_est.close()
        cur_insc.close()
        cur_asist.close()
        pg_conn.close()

        self.stdout.write(self.style.SUCCESS(f'✓ {inscripciones_migradas} Inscripciones migradas con sus respectivas listas de asistencias.'))
        self.stdout.write(self.style.SUCCESS('=== Migración Políglota Completada con Éxito ==='))