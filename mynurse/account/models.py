from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from newsletters.models import Tag, NewsLetter

# Create your models here.
class User(AbstractBaseUser):
    username = models.EmailField(unique=True, verbose_name='username')
    birth = models.DateField(default='1995-06-20')
    gender = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    like_tags = models.ManyToManyField(Tag)
    subscribes = models.ManyToManyField(NewsLetter)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)     

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class EmailCheck(models.Model):
    email = models.EmailField(unique=True)
    check_number = models.CharField(max_length=10)