import json

from channels import Group

from .models import Conversation, Message


def send_message(conversation_id, text, user=None, bot=None):
    try:
        Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return

    message = Message.objects.create(
        user=user,
        bot=bot,
        conversation_id=conversation_id,
        text=text,
    )

    Group(f'conversation_{conversation_id}').send({
        'text': json.dumps({'text': message.text,
                            'author': message.author})
    })
