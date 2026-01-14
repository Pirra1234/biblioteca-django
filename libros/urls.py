from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libro/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autor/<int:id>/', views.detalle_autor, name='detalle_autor'),
    path('busqueda/', views.busqueda_avanzada, name='busqueda_avanzada'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]
