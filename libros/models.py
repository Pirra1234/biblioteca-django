from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    pais_origen = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='autores/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    sitio_web = models.URLField(null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    isbn = models.CharField(max_length=13, unique=True)
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True)
    fecha_publicacion = models.DateField()
    numero_paginas = models.PositiveIntegerField()
    sinopsis = models.TextField()
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    calificacion = models.FloatField(default=0.0)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    ESTADO_PRESTAMO = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
    ]
    
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_usuario = models.CharField(max_length=150)
    email_usuario = models.EmailField()
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_PRESTAMO, default='activo')

    def __str__(self):
        return f"{self.libro.titulo} - {self.nombre_usuario}"