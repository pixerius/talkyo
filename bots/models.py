import spacy

from django.db import models
from django.conf import settings


nlp = spacy.load(settings.LANGUAGE_MODEL)


class Bot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_node = models.ForeignKey('Node', models.SET_NULL,
                                   related_name='bots', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def greeting(self):
        return self.start_node.text


class Node(models.Model):
    text = models.TextField()
    children = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.text

    def get_next_node(self, text):
        nlp_text = nlp(text)

        for node in self.children.all():
            for sentence in node.sentences.all():
                nlp_sentence = nlp(sentence.text)
                similarity = nlp_sentence.similarity(nlp_text)

                if similarity > settings.SIMILARITY_THRESHOLD:
                    return node


class Sentence(models.Model):
    node = models.ForeignKey('Node', models.CASCADE, related_name='sentences')
    text = models.TextField()

    def __str__(self):
        return self.text
