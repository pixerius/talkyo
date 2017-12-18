import spacy

from django.db import models
from django.conf import settings

from .labels import NAMED_ENTITY_LABELS


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
    NAMED_ENTITY_LABEL_CHOICES = [(label, spacy.explain(label))
                                  for label in NAMED_ENTITY_LABELS]
    text = models.TextField()
    children = models.ManyToManyField('self', symmetrical=False, blank=True)
    named_entity_label = models.CharField(choices=NAMED_ENTITY_LABEL_CHOICES,
                                          max_length=16, default='',
                                          blank=True)

    def __str__(self):
        return self.text

    def get_next_node_and_answer(self, text):
        nlp_text = nlp(text)

        for node in self.children.exclude(named_entity_label=''):
            for ent in nlp_text.ents:
                if ent.label_ == node.named_entity_label:
                    entity = text[ent.start_char:ent.end_char]

                    try:
                        return node, node.text.format(entity)
                    except IndexError:
                        pass

        next_node_candidates = []

        for node in self.children.filter(named_entity_label=''):
            for sentence in node.sentences.all():
                nlp_sentence = nlp(sentence.text)
                similarity = nlp_sentence.similarity(nlp_text)

                if similarity > settings.SIMILARITY_THRESHOLD:
                    next_node_candidates.append((node, similarity))

        if next_node_candidates:
            next_node, _ = max(next_node_candidates, key=lambda pair: pair[1])
            return next_node, next_node.text

        return None, ''


class Sentence(models.Model):
    node = models.ForeignKey('Node', models.CASCADE, related_name='sentences')
    text = models.TextField()

    def __str__(self):
        return self.text
