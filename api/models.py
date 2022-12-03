from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author =models.CharField(max_length=100)
    year_published = models.CharField(max_length=10)
    review = models.PositiveIntegerField()

    def __str__(self):
        return self.title

