import random
import string

from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=64, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, default='')

    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='creator_video')

    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def save(self, *args, **kwargs):
        self.slug = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        super(Video, self).save(*args, **kwargs)


class Comments(models.Model):
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='sender_comment')
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                                  related_name='hostvideo')


class Subscribes(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='creator')
    users = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='users')
