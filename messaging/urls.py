from django.conf.urls import url, include
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^conversation/', include([

        url(r'^start/', include([

            url(r'^user/(?P<user_id>\d+)/$',
                views.ConversationStartView.as_view(),
                name='user-conversation-start'),

            url(r'^bot/(?P<bot_id>\d+)/$',
                views.ConversationStartView.as_view(),
                name='bot-conversation-start'),

        ])),

        url(r'^(?P<conversation_id>\d+)/', include([

            url(r'^add/$',
                views.ConversationAddUserView.as_view(),
                name='conversation-add-user'),

            url(r'^leave/$',
                views.ConversationLeaveView.as_view(),
                name='conversation-leave'),

            url(r'^$',
                views.ConversationView.as_view(),
                name='conversation'),

        ])),

        url(r'^$',
            TemplateView.as_view(template_name='messaging/conversation.html'),
            name='conversation-list'),

    ]))

]
