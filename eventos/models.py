from django.contrib.auth.models import AbstractUser
from django.db import models
from time import timezone

# Usuario autenticable
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Evento(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_creados')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(help_text="Descripcion de evento")
    fecha = models.DateField()
    publicacion = models.DateTimeField(auto_now_add=True)
    portada = models.ImageField(upload_to='portadas_eventos/', null=True, blank=True)
    participantes = models.ManyToManyField(Usuario, through='RegistroEvento', related_name='eventos_inscrito')

class RegistroEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
