import random
import string

from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    name = models.CharField(max_length=64, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, default='')
    is_private = models.BooleanField(default=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='creator_chat')
    subscribes = models.ManyToManyField(User, related_name='subscribes')

    def save(self, *args, **kwargs):
        self.slug = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        super(Chat, self).save(*args, **kwargs)
        self.subscribes.add(self.creator)


class Message(models.Model):
    text = models.TextField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='sender_message')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                                  related_name='hostchat')