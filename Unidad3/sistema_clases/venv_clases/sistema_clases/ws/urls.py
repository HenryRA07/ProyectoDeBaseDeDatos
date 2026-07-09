from django.urls import path
from .views import ClaseListView

urlpatterns = [
    path('clases/', ClaseListView.as_view(), name='clases'),
]
