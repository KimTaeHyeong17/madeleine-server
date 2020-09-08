from django.db import models

from newsletters.models import NewsLetter

# Create your models here.
class CurationPage(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    intro_title = models.CharField(max_length=50)
    intro_content = models.TextField()
    image = models.ImageField(upload_to='curation/', default='/curation/new_neek.png')

    def __str__(self):
        return self.title
        
class Curation(models.Model):
    title = models.CharField(max_length=50)
    explain = models.TextField(null=True)
    newsletter = models.ForeignKey(to=NewsLetter,on_delete=models.CASCADE, null=True)
    curation_page = models.ForeignKey(to=CurationPage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title





