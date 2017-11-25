from django.db import models


class Conversation(models.Model):
    users = models.ManyToManyField('users.User')


class Message(models.Model):
    class Meta:
        default_related_name = 'messages'

    author = models.ForeignKey('users.User', models.CASCADE,
                               related_name='messages')
    conversation = models.ForeignKey('Conversation', models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
