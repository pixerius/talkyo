from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse

from users.models import User
from bots.models import Bot
from .models import Conversation, Message


class ConversationView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/conversation/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        self.conversation = get_object_or_404(
            Conversation,
            id=self.kwargs['conversation_id']
        )

        if self.conversation not in self.request.user.conversations.all():
            raise Http404()

        return super().get_queryset().filter(conversation=self.conversation.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversation'] = self.conversation
        context['users'] = User.objects.filter(
            friends=self.request.user
        ).exclude(
            id__in=self.conversation.users.all()
        )

        if self.conversation.bot:
            context['bots'] = Bot.objects.exclude(id=self.conversation.bot.id)
        else:
            context['bots'] = Bot.objects.all()

        return context


class ConversationStartView(LoginRequiredMixin, View):
    def get(self, request, user_id=None, bot_id=None):

        if user_id and request.user.id == int(user_id):
            raise Http404()

        if user_id:
            user = get_object_or_404(User, id=user_id)

            conversation = Conversation()
            conversation.save()
            conversation.users.add(user, request.user)

        elif bot_id:
            bot = get_object_or_404(Bot, id=bot_id)

            conversation = Conversation(bot=bot)
            conversation.save()
            conversation.users.add(request.user)

        return redirect(conversation)


class ConversationAddUserView(LoginRequiredMixin, View):
    def get(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if conversation not in request.user.conversations.all():
            raise Http404()

        user_id = self.request.GET.get('user_id')

        try:
            user = get_object_or_404(User, id=user_id)
        except ValueError:
            return redirect(conversation)

        conversation.users.add(user)

        return redirect(conversation)


class ConversationLeaveView(LoginRequiredMixin, View):
    def get(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        request.user.conversations.remove(conversation)

        if conversation.users.count() < 2:
            conversation.delete()

        return redirect(reverse('messaging:conversation-list'))


class ConversationBotView(LoginRequiredMixin, View):
    def get(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if conversation not in request.user.conversations.all():
            raise Http404()

        bot_id = request.GET.get('bot_id')

        try:
            bot = get_object_or_404(Bot, id=bot_id)
        except ValueError:
            return redirect(conversation)

        conversation.bot = bot
        conversation.save()

        return redirect(conversation)
