from django.views.generic.list import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bot


class BotListView(LoginRequiredMixin, ListView):
    model = Bot
    template_name = 'bots/bots.html'
    context_object_name = 'bots'
