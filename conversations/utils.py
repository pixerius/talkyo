from .models import Conversation, Message


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
    message.send()

    if conversation.bot and conversation.node and bot is None:
        next_node, answer = conversation.node.get_next_node_and_answer(text)

        if next_node:
            bot_message = Message.objects.create(
                bot=conversation.bot,
                conversation_id=conversation_id,
                text=answer,
            )

            conversation.node = next_node
            conversation.save()

            bot_message.send()
