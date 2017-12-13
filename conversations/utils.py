import json

from channels import Group

from .models import Conversation, Message


def _send_to_group(conversation_id, text, author):
    Group(f'conversation_{conversation_id}').send({
        'text': json.dumps({'text': text,
                            'author': str(author)})
    })


def send_message(conversation_id, text, user=None, bot=None):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return

    message = Message.objects.create(
        user=user,
        bot=bot,
        conversation_id=conversation_id,
        text=text,
    )

    _send_to_group(conversation_id, message.text, message.author)

    if conversation.bot and conversation.node:
        next_node = conversation.node.get_next_node(text)

        if next_node:
            bot_message = Message.objects.create(
                bot=conversation.bot,
                conversation_id=conversation_id,
                text=next_node.text,
            )

        _send_to_group(conversation_id, bot_message.text, bot_message.author)
