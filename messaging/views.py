from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest

from users.models import User
from bots.models import Bot
from .models import Conversation, Message


class ConversationView(ListView):
    model = Message
    template_name = 'messaging/conversation.html'
    context_object_name = 'messages'

    def get_queryset(self):
        self.conversation = get_object_or_404(Conversation,
                                              id=self.kwargs['id'])
        return super().get_queryset().filter(conversation=self.conversation.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversation_id'] = self.conversation.id
        return context


@method_decorator(login_required, name='dispatch')
class ConversationStartView(View):
    def get(self, request, user_id=None, bot_id=None):

        if request.user.id == int(user_id):
            return HttpResponseBadRequest()

        conversations = Conversation.objects.annotate(
            users_count=Count('users'))

        if user_id:
            user = get_object_or_404(User, id=user_id)

            conversation = conversations.filter(
                users_count=2, users=request.user
            ).filter(users=user).first()

            if not conversation:
                conversation = Conversation()
                conversation.save()
                conversation.users.add(user, request.user)

        elif bot_id:
            bot = get_object_or_404(Bot, id=user_id)

            conversation = conversations.filter(
                users=request.user, users_count=1, bot=bot
            ).first()

            if not conversation:
                conversation = Conversation(bot=bot)
                conversation.save()
                conversation.users.add(request.user)

        return redirect(conversation)
