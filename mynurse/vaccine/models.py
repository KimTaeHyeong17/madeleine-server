from django.db import models

from account.models import User

# Create your models here.

class Vaccine(models.Model):
    owner = models.ForeignKey(User, related_name='vaccines', on_delete=models.CASCADE)
    vaccine = models.CharField(max_length=100)
    date = models.DateField()
    hospital = models.CharField(max_length=100)

    def __self__(self):
        return self.vaccine
    
    class Meta:
        ordering = ['date', ]