from django.contrib import admin
from .models import Post, Like, Comment, Follow, Message

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Message)

