from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    greeting = models.TextField()

    def __str__(self):
        return self.name
