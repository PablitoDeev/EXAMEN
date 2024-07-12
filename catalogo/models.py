from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    año_publicacion = models.IntegerField()
    descripcion_breve = models.TextField()

    def __str__(self):
        return self.titulo

class NavItem(models.Model):
    titulo = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.titulo
