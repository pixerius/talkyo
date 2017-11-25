from django.db import models
from django.urls import reverse


class Conversation(models.Model):
    class Meta:
        default_related_name = 'conversations'

    users = models.ManyToManyField('users.User')
    bot = models.ForeignKey('bots.Bot', models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('messaging:conversation', kwargs={'id': self.id})


class Message(models.Model):
    class Meta:
        default_related_name = 'messages'
        ordering = ['timestamp']

    author = models.ForeignKey('users.User', models.CASCADE,
                               related_name='messages')
    conversation = models.ForeignKey('Conversation', models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
