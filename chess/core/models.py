from django.db import models

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=50)
    related = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')


    class Meta:#klasa odpowiadająca za wyświetlanie przedmiotów w panelu admina
        ordering = ('name',)

    def __str__(self):
        return self.name
    
