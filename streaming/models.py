from django.db import models

# Create your models here.
class Videos(models.Model):
    
    video_id = models.AutoField(db_column='video_id', primary_key=True)
    video_name = models.CharField(max_length=100)
    location = models.FileField(upload_to='video/')
    fecha = models.CharField(max_length=50) 

    class Meta:
        db_table = 'video'