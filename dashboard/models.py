from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    Category = models.CharField(max_length=100)
     
    def __str__(self):
        return self.Category    
