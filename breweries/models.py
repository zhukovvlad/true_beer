from django.db import models

# Create your models here.
class Brewery(models.Model):
    name = models.CharField(max_length=140, verbose_name='Brewery\'s name')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '{}'.format(self.name)
