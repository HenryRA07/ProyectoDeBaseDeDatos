import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from modelo.models import Estudiante, Inscripcion

def inscribir_estudiante(request):
    if request.method == 'GET':
        clases = []
        try:
            resp = requests.get('http://127.0.0.1:8000/ws/clases/')
            if resp.status_code == 200:
                clases = resp.json()
        except requests.ConnectionError:
            messages.error(request, 'No se pudo conectar con el servicio de clases')

        estudiantes = Estudiante.objects.all()

        return render(request, 'inscripciones.html', {
            'clases': clases,
            'estudiantes': estudiantes,
        })

    elif request.method == 'POST':
        id_estudiante = request.POST['id_estudiante']
        id_clase = request.POST['id_clase']
        estado = request.POST.get('estado', 'Activo')
        fecha = request.POST.get('fecha')

        try:
            Estudiante.objects.get(pk=id_estudiante)
        except Estudiante.DoesNotExist:
            messages.error(request, 'Estudiante no encontrado')
            return redirect('inscripciones')

        Inscripcion.objects.create(
            id_estudiante=id_estudiante,
            id_clase=id_clase,
            estado=estado,
            fecha=fecha,
        )
        messages.success(request, 'Inscripción creada exitosamente.')
        return redirect('inscripciones')
