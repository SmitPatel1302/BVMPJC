from django.db import models

class Login(models.Model):    
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='ID')
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

