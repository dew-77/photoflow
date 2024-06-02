from django.urls import path
from . import api_views

urlpatterns = [
    path(
        'post/<int:pk>/',
        api_views.PostDetailAPIView.as_view(),
        name='post_detail_api'
    ),
    path(
        'post/<int:pk>/comment/',
        api_views.AddCommentAPIView.as_view(),
        name='add_comment_api'
    ),
    path(
        'post/<int:pk>/like/',
        api_views.LikePostAPIView.as_view(),
        name='like_post_api'
    ),
    path(
        'follow/<int:pk>/',
        api_views.AddFollowAPIView.as_view(),
        name='add_follow'
    ),
    path(
        'unfollow/<int:pk>/',
        api_views.RemoveFollowAPIView.as_view(),
        name='remove_follow'
    ),
    path(
        'send_message/',
        api_views.SendMessageAPIView.as_view(),
        name='send_message'
    ),
    path(
        'chat_users/',
        api_views.ChatUsersAPIView.as_view(),
        name='chat_users'
    ),
    path(
        'chat/<int:user_id>/',
        api_views.ChatMessagesAPIView.as_view(),
        name='chat_messages'
    ),
]
