from rest_framework import serializers

from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = [
            'name',
            'is_private',
            'creator',
            'slug'
        ]

    def chat_list(self, chats):
        res = {}
        for number, chat in enumerate(chats):
            c = {}
            c['id'] = chat.id
            c['name'] = chat.name
            c['slug'] = chat.slug
            #chat['creator_id'] = chat.creator_id_id
            #chat['n_subscribes'] = chat.id
            res['chat_' + str(number+1)] = c
        res['length'] = len(chats)
        return res


