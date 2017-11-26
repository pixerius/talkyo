from channels.generic.websockets import JsonWebsocketConsumer
from channels import Group

from .models import Conversation
from .utils import send_message


class ConversationConsumer(JsonWebsocketConsumer):

    http_user = True

    def connection_groups(self, **kwargs):
        return []

    def connect(self, message, **kwargs):
        conversation_id = kwargs['id']

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return self._close_connection(message)

        if message.user not in conversation.users.all():
            return self._close_connection(message)

        self.message.reply_channel.send({'accept': True})

        Group(f'conversation_{conversation_id}').add(message.reply_channel)

        message.channel_session['conversation_id'] = conversation_id

    def receive(self, content, **kwargs):
        conversation_id = kwargs['id']

        if 'text' not in content:
            return

        send_message(conversation_id, content['text'], user=self.message.user)

    def disconnect(self, message, **kwargs):
        conversation_id = kwargs['id']

        Group(f'conversation_{conversation_id}').discard(message.reply_channel)

    def _close_connection(self, message):
        message.reply_channel.send({'close': True})
