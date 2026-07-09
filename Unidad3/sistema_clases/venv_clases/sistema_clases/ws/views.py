from rest_framework.generics import ListAPIView
from modelo.models import Clase
from .serializers import ClaseSerializer

class ClaseListView(ListAPIView):
    serializer_class = ClaseSerializer

    def get_queryset(self):
        return Clase.objects.select_related('id_curso', 'id_profesor').all()
