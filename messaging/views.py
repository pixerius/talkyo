from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.urls import reverse

from users.models import User
from bots.models import Bot
from .models import Conversation, Message


@method_decorator(login_required, name='dispatch')
class ConversationView(ListView):
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
        return context


@method_decorator(login_required, name='dispatch')
class ConversationStartView(View):
    def get(self, request, user_id=None, bot_id=None):

        if request.user.id == int(user_id):
            raise Http404()

        if user_id:
            user = get_object_or_404(User, id=user_id)

            conversation = Conversation()
            conversation.save()
            conversation.users.add(user, request.user)

        elif bot_id:
            bot = get_object_or_404(Bot, id=user_id)

            conversation = Conversation(bot=bot)
            conversation.save()
            conversation.users.add(request.user)

        return redirect(conversation)


@method_decorator(login_required, name='dispatch')
class ConversationAddUserView(View):
    def get(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if conversation not in request.user.conversations.all():
            raise Http404()

        user_id = self.request.GET.get('user_id')
        user = get_object_or_404(User, id=user_id)

        conversation.users.add(user)

        return redirect(conversation)


@method_decorator(login_required, name='dispatch')
class ConversationLeaveView(View):
    def get(self, request, conversation_id=None):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        request.user.conversations.remove(conversation)

        return redirect(reverse('messaging:conversation-list'))
