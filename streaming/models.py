from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Videos(models.Model):
    
    video_id = models.AutoField(db_column='video_id', primary_key=True)
    video_name = models.CharField(max_length=100)
    location = models.FileField(upload_to='video/')
    fecha = models.CharField(max_length=50) 

    class Meta:
        db_table = 'video'
        
        
class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()