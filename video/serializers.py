from rest_framework import serializers

from video.models import Video, Subscribes, Comments


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = [
            'name',
            'creator'
        ]

    def video_list(self, videos):
        res = {}
        for number, video in enumerate(videos):
            c = {}
            c['id'] = video.id
            c['name'] = video.name
            c['slug'] = video.slug
            c['creator_id'] = video.creator.username
            c['likes'] = video.likes.count()
            c['dislikes'] = video.dislikes.count()
            res['video_' + str(video.id)] = c
        res['length'] = len(videos)
        return res

    def video_info(self, video):
        res = {}
        res['id'] = video.id
        res['name'] = video.name
        res['slug'] = video.slug
        res['creator_username'] = video.creator.username
        res['likes'] = video.likes.count()
        res['dislikes'] = video.dislikes.count()
        return res


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = [
            'text'
        ]

    def comment_list(self, comments, st=0):
        res = {}
        for number, comment in enumerate(comments):
            c = {}
            c['id'] = comment.id
            c['text'] = comment.text
            c['created_date'] = comment.created_date
            c['sender'] = comment.sender.username
            res['comment_' + str(comment.id)] = c
        res['length'] = len(comments)
        return res



