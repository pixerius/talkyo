from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_node = models.ForeignKey('Node', models.SET_NULL,
                                   related_name='bots', null=True, blank=True)

    def __str__(self):
        return self.name


class Node(models.Model):
    text = models.TextField()
    keywords = models.TextField()
    children = models.ManyToManyField('self', symmetrical=False, blank=True)
