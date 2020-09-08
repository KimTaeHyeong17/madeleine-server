from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(default='/category_image/default.png', upload_to='category_image')

    def __str__(self):
        return self.name

class NewsLetter(models.Model):
    newsletter_name = models.CharField(max_length=30, unique=True)
    register_url = models.URLField(null=True)
    explain = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(default='/newsletter/default.png', upload_to='newsletter')
    followers = models.IntegerField(default=0)
    
    def __str__(self):
        return self.newsletter_name

class Episode(models.Model):
    newsletter = models.ForeignKey(to=NewsLetter, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    title = models.TextField(max_length=50)
    episode_url = models.URLField(null=True)
