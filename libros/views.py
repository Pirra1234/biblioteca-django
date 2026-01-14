from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q
from .models import Libro, Autor, Categoria, Editorial, Prestamo

def inicio(request):
    """Vista principal con estadísticas del sistema"""
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    total_categorias = Categoria.objects.filter(activa=True).count()
    libros_disponibles = Libro.objects.filter(estado='disponible').count()
    prestamos_activos = Prestamo.objects.filter(estado='activo').count()
    
    libros_destacados = Libro.objects.filter(
        calificacion__gte=4.0
    ).order_by('-calificacion')[:6]
    
    ultimos_libros = Libro.objects.order_by('-fecha_publicacion')[:6]
    
    context = {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'total_categorias': total_categorias,
        'libros_disponibles': libros_disponibles,
        'prestamos_activos': prestamos_activos,
        'libros_destacados': libros_destacados,
        'ultimos_libros': ultimos_libros,
    }
    return render(request, 'libros/inicio.html', context)

def lista_libros(request):
    """Listado de todos los libros con filtros"""
    libros = Libro.objects.select_related('autor', 'editorial').prefetch_related('categorias')
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    autor_id = request.GET.get('autor')
    estado = request.GET.get('estado')
    busqueda = request.GET.get('q')
    
    if categoria_id:
        libros = libros.filter(categorias__id=categoria_id)
    if autor_id:
        libros = libros.filter(autor__id=autor_id)
    if estado:
        libros = libros.filter(estado=estado)
    if busqueda:
        libros = libros.filter(
            Q(titulo__icontains=busqueda) |
            Q(isbn__icontains=busqueda) |
            Q(autor__nombre__icontains=busqueda)
        )
    
    # Para los selectores de filtro
    categorias = Categoria.objects.filter(activa=True)
    autores = Autor.objects.all().order_by('nombre')
    estados = Libro.ESTADO_CHOICES
    
    context = {
        'libros': libros,
        'categorias': categorias,
        'autores': autores,
        'estados': estados,
        'categoria_seleccionada': categoria_id,
        'autor_seleccionado': autor_id,
        'estado_seleccionado': estado,
        'busqueda': busqueda,
    }
    return render(request, 'libros/lista_libros.html', context)

def detalle_libro(request, id):
    """Detalles completos de un libro específico"""
    libro = get_object_or_404(
        Libro.objects.select_related('autor', 'editorial').prefetch_related('categorias'),
        id=id
    )
    
    # Libros relacionados (mismo autor o categorías similares)
    libros_relacionados = Libro.objects.filter(
        Q(autor=libro.autor) | Q(categorias__in=libro.categorias.all())
    ).exclude(id=libro.id).distinct()[:4]
    
    context = {
        'libro': libro,
        'libros_relacionados': libros_relacionados,
    }
    return render(request, 'libros/detalle_libro.html', context)

def lista_autores(request):
    """Listado de todos los autores con estadísticas"""
    autores = Autor.objects.annotate(
        total_libros=Count('libro'),
        calificacion_promedio=Avg('libro__calificacion')
    ).order_by('nombre')
    
    busqueda = request.GET.get('q')
    if busqueda:
        autores = autores.filter(
            Q(nombre__icontains=busqueda) |
            Q(pais_origen__icontains=busqueda)
        )
    
    context = {
        'autores': autores,
        'busqueda': busqueda,
    }
    return render(request, 'libros/lista_autores.html', context)

def detalle_autor(request, id):
    """Detalles de un autor y sus libros"""
    autor = get_object_or_404(Autor, id=id)
    libros = Libro.objects.filter(autor=autor).prefetch_related('categorias')
    
    # Estadísticas del autor
    total_libros = libros.count()
    calificacion_promedio = libros.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    
    context = {
        'autor': autor,
        'libros': libros,
        'total_libros': total_libros,
        'calificacion_promedio': round(calificacion_promedio, 1),
    }
    return render(request, 'libros/detalle_autor.html', context)

def busqueda_avanzada(request):
    """Búsqueda avanzada con múltiples filtros"""
    libros = Libro.objects.select_related('autor', 'editorial').prefetch_related('categorias')
    
    # Filtros avanzados
    titulo = request.GET.get('titulo')
    autor = request.GET.get('autor')
    categoria = request.GET.get('categoria')
    editorial = request.GET.get('editorial')
    año_desde = request.GET.get('año_desde')
    año_hasta = request.GET.get('año_hasta')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    calificacion_min = request.GET.get('calificacion_min')
    
    if titulo:
        libros = libros.filter(titulo__icontains=titulo)
    if autor:
        libros = libros.filter(autor__nombre__icontains=autor)
    if categoria:
        libros = libros.filter(categorias__id=categoria)
    if editorial:
        libros = libros.filter(editorial__id=editorial)
    if año_desde:
        libros = libros.filter(fecha_publicacion__year__gte=año_desde)
    if año_hasta:
        libros = libros.filter(fecha_publicacion__year__lte=año_hasta)
    if precio_min:
        libros = libros.filter(precio__gte=precio_min)
    if precio_max:
        libros = libros.filter(precio__lte=precio_max)
    if calificacion_min:
        libros = libros.filter(calificacion__gte=calificacion_min)
    
    categorias = Categoria.objects.filter(activa=True)
    editoriales = Editorial.objects.all().order_by('nombre')
    
    context = {
        'libros': libros,
        'categorias': categorias,
        'editoriales': editoriales,
        'filtros': request.GET,
    }
    return render(request, 'libros/busqueda_avanzada.html', context)

def estadisticas(request):
    """Dashboard con métricas y estadísticas del sistema"""
    # Estadísticas generales
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    total_categorias = Categoria.objects.count()
    total_editoriales = Editorial.objects.count()
    
    # Estadísticas de libros
    libros_por_estado = Libro.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Top 10 autores con más libros
    top_autores = Autor.objects.annotate(
        total_libros=Count('libro')
    ).order_by('-total_libros')[:10]
    
    # Top 10 categorías más populares
    top_categorias = Categoria.objects.annotate(
        total_libros=Count('libro')
    ).order_by('-total_libros')[:10]
    
    # Libros mejor calificados
    mejores_libros = Libro.objects.filter(
        calificacion__gte=4.0
    ).order_by('-calificacion')[:10]
    
    # Estadísticas de préstamos
    total_prestamos = Prestamo.objects.count()
    prestamos_activos = Prestamo.objects.filter(estado='activo').count()
    prestamos_retrasados = Prestamo.objects.filter(estado='retrasado').count()
    
    context = {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'total_categorias': total_categorias,
        'total_editoriales': total_editoriales,
        'libros_por_estado': libros_por_estado,
        'top_autores': top_autores,
        'top_categorias': top_categorias,
        'mejores_libros': mejores_libros,
        'total_prestamos': total_prestamos,
        'prestamos_activos': prestamos_activos,
        'prestamos_retrasados': prestamos_retrasados,
    }
    return render(request, 'libros/estadisticas.html', context)
