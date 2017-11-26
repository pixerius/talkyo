from django.views.generic.list import ListView

from .models import Bot


class BotListView(ListView):
    model = Bot
    template_name = 'bots/bots.html'
    context_object_name = 'bots'
