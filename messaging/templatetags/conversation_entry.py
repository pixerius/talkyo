from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def conversation_entry(context, conversation):
    users = conversation.users.exclude(id=context['request'].user.id)
    return ', '.join(str(user) for user in list(users))
