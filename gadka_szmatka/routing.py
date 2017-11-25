from messaging import consumers

channel_routing = [
    consumers.ConversationConsumer.as_route(
        path=r'^/conversation/(?P<id>\d+)/'),
]
