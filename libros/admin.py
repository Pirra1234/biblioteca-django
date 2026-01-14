from django.contrib import admin
from .models import Autor, Categoria, Editorial, Libro, Prestamo

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais_origen', 'fecha_nacimiento']
    search_fields = ['nombre', 'pais_origen']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa']
    list_filter = ['activa']

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'email']
    search_fields = ['nombre']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'isbn', 'estado', 'precio', 'stock']
    list_filter = ['estado', 'editorial', 'categorias']
    search_fields = ['titulo', 'isbn', 'autor__nombre']
    filter_horizontal = ['categorias']

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'nombre_usuario', 'fecha_prestamo', 'fecha_devolucion_esperada', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre_usuario', 'email_usuario', 'libro__titulo']