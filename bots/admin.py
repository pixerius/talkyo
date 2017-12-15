from django.contrib import admin

from .models import Bot, Node, Sentence


class SentenceInline(admin.TabularInline):
    model = Sentence
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    model = Node
    inlines = (SentenceInline,)


admin.site.register(Bot)
admin.site.register(Node, NodeAdmin)
