from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like, Follow, User, Message
from .serializers import FollowSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, MessageSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddCommentAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user, post_id=self.kwargs['pk'])


class LikePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user, post=post
        )
        if not created:
            like.delete()
        return Response({'likes_count': post.likes.count()})


class AddFollowAPIView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        following_user = User.objects.get(pk=self.kwargs['pk'])
        serializer.save(follower=self.request.user, following=following_user)


class RemoveFollowAPIView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        following_user = get_object_or_404(User, pk=self.kwargs['pk'])
        follow = get_object_or_404(Follow, follower=self.request.user, following=following_user)
        return follow


class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'status': 'message sent', 'message': response.data})


class ChatUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        sent_messages = Message.objects.filter(sender=user).values_list('receiver', flat=True)
        received_messages = Message.objects.filter(receiver=user).values_list('sender', flat=True)
        chat_users_ids = set(sent_messages).union(set(received_messages))
        chat_users = User.objects.filter(id__in=chat_users_ids)

        chat_users_data = [
            {
                'id': chat_user.id,
                'username': chat_user.username,
                'profile_picture': chat_user.profile_picture.url
            }
            for chat_user in chat_users
        ]

        return Response({'chat_users': chat_users_data})


class ChatMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        selected_user = User.objects.get(id=user_id)
        messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=user))
        ).order_by('created_at')

        messages_data = [
            {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_username': message.sender.username,
                'text': message.text,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for message in messages
        ]

        return Response({'username': selected_user.username, 'messages': messages_data})