from django.conf.urls import url, include
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

        url(r'^(?P<id>\d+)/$',
            views.ConversationView.as_view(),
            name='conversation'),

    ]))

]
