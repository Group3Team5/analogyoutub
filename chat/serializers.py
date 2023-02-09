from rest_framework import serializers

from chat.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = [
            'name',
            'is_private',
            'slug'
        ]

    def chat_list(self, chats):
        res = {}
        for number, chat in enumerate(chats):
            c = {}
            c['id'] = chat.id
            c['name'] = chat.name
            c['slug'] = chat.slug
            c['creator_id'] = chat.creator.username
            c['n_subscribes'] = len(chat.subscribes.all())
            res['chat_' + str(number+1)] = c
        return res

    def chat_info(self, chat):
        res = {}
        res['id'] = chat.id
        res['name'] = chat.name
        res['slug'] = chat.slug
        res['creator_id'] = chat.creator.username
        res['n_subscribes'] = [u.username for u in chat.subscribes.all()]
        return res


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            'text'
        ]

    def message_list(self, messages, st=0):
        res = {}
        for number, message in enumerate(messages):
            c = {}
            c['id'] = message.id
            c['text'] = message.text
            c['created_date'] = message.created_date
            c['sender'] = message.sender.username
            res['message_' + str(message.id)] = c
        return res




