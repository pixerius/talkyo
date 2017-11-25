from channels.generic.websockets import WebsocketConsumer


class ConversationConsumer(WebsocketConsumer):

    http_user = True

    def connection_groups(self, **kwargs):
        return []

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        self.send(text=text, bytes=bytes)

    def disconnect(self, message, **kwargs):
        pass
