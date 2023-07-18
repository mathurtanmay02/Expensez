from django.db import models
from dashboard.models import Categories
from django.contrib.auth.models import User

# Create your models here.

class Expenses(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Amount = models.IntegerField()
    Date = models.DateField()
    Description = models.CharField(max_length=100)
    Category = models.ForeignKey(Categories, on_delete=models.CASCADE)
