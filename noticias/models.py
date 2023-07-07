from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
User=get_user_model()


# Create your models here.
class Estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.estado)

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.categoria)

class Noticia(models.Model):
    idNoticia = models.AutoField(primary_key=True)
    noticia = models.CharField(max_length=255)
    cuerpo = models.TextField()
    imagen = models.CharField(max_length=255)
    comentario = models.TextField(default="")
    idUsuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE,default=1)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    ubicacion = models.CharField(max_length=255, null=True)
    destacada = models.BooleanField(default=False)

    def __str__(self):
        return str(self.noticia)